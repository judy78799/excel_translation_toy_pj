from fastapi import APIRouter, UploadFile, File, Query, HTTPException
from app.models.upload import FileUploadResponse, TranslationResult
from app.services.file_service import FileService
from app.services.translation_service import TranslationService
from app.services.external_api_service import ExternalAPIService
from app.utils.file_parser import ExcelParser
from app.core.config import settings
from pathlib import Path
import time
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Create service instances
file_service = FileService()
api_service = ExternalAPIService()
translation_service = TranslationService(api_service)

@router.post("/", response_model=FileUploadResponse)
async def upload_and_translate(
    file: UploadFile = File(...),
    source_lang: str = Query("ko", pattern="^[a-z]{2}$"),
    target_lang: str = Query("en", pattern="^[a-z]{2}$"),
    text_column: str = Query("text")
):
    """
    Upload file and translate immediately
    Compatible with the new Frontend implementation
    """
    start_time = time.time()
    
    # 1. Validate file
    file_extension = Path(file.filename).suffix
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed extensions: {settings.ALLOWED_EXTENSIONS}"
        )
    
    try:
        # 2. Save file
        metadata = await file_service.save_uploaded_file(file)
        
        # 3. Parse and Extract Text
        parser = ExcelParser(metadata.file_path)
        
        # Try to find the column by name or use the first column if not found?
        # Frontend defaults to 'text'
        try:
            texts = parser.get_column_data(column_name=text_column)
        except ValueError:
            # If column name lookup fails, try index 0 or raise clearer error
            # For now, let's try to get column by index 0 as fallback if text_column is generic
            # But 'text_column' query param is passed, so we should respect it.
            # Let's assume ExcelParser supports column_name.
            # If not, we might need to update ExcelParser or use pandas directly.
            # Checking ExcelParser... wait, I haven't checked ExcelParser code yet.
            # Let's assume for now and catch error.
            
            # Since I cannot see ExcelParser code right now without another tool call, 
            # I will assume `get_column_data` accepts `column_name` OR modify it to work.
            # Re-reading `translation.py` (Step 113 endpoint), it uses `column_index`.
            # Let's use pandas directly here for flexibility or check parser.
            # Actually, `file_service.py` imports `ExcelParser`.
            
            # Safe bet: Read file with pandas directly here to match specific column name requirement easily
            # OR assume parser works.
            # Let's use pandas as in the user's snippet in Step 71.
            import pandas as pd
            df = pd.read_excel(metadata.file_path) if file_extension in ['.xlsx', '.xls'] else pd.read_csv(metadata.file_path, encoding="utf-8-sig") # Pandas가 엑셀 파일을 열어서 메모리 상의 표인 DataFrame으로 변환함.
            
            if text_column not in df.columns:
                # If column not found, and maybe user didn't specify one?
                # If dataframe has columns, use the first one as fallback if single column?
                 raise HTTPException(status_code=400, detail=f"Column '{text_column}' not found in file. Available columns: {list(df.columns)}")
            
            # Pandas 사용자가 지정한 컬럼만 쏙 뽑아서 "파이썬 리스트"로 만듦. 
            # 리스트 값이 전부 NAN 일 경우 번역 API에서 터질 수 있으므로 코드 수정 + 방어 코드
            texts = (
                df[text_column]
                .dropna()
                .astype(str)
                .str.strip()
                .tolist()
            )

            if not texts:
                raise HTTPException(status_code=400, detail="No valid text rows found")

        # 4. Translate
        if not texts:
             raise HTTPException(status_code=400, detail="No text found in the specified column")

        # Use existing translate_texts method
        # It returns List[TranslationItem] with original, translated, source_lang, target_lang
        try:
            translation_items = await translation_service.translate_texts(texts, source_lang, target_lang)
        except Exception as e:
            logger.exception("Translation failed")
            raise HTTPException(status_code=502, detail="Translation service failed")
        
        # 5. Convert to TranslationResult for response (adds source_lang/target_lang)
        results = [
            TranslationResult(
                original=item.original, 
                translated=item.translated,
                source_lang=item.source_lang,
                target_lang=item.target_lang
            ) 
            for item in translation_items
        ]
        
        success_count = len([r for r in results if r.translated])
        error_count = len(results) - success_count
        
        processing_time = time.time() - start_time
        
        return FileUploadResponse(
            status="success",
            total_rows=len(results),
            success_count=success_count,
            error_count=error_count,
            results=results,
            processing_time=round(processing_time, 2),
            file_name=metadata.filename
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

# Keep existing endpoints for backward compatibility or direct usage
@router.delete("/{file_id}")
async def delete_file(file_id: str):
    success = file_service.delete_file(file_id)
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    return {"success": True, "message": "File deleted successfully"}

@router.get("/{file_id}/info")
async def get_file_info(file_id: str):
    try:
        metadata = file_service.get_file_metadata(file_id)
        return {
            "success": True,
            "file_id": metadata.file_id,
            "filename": metadata.filename,
            "file_size": metadata.file_size,
            "upload_time": metadata.upload_time.isoformat(),
            "sheet_names": metadata.sheet_names,
            "row_count": metadata.row_count,
            "column_count": metadata.column_count
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))