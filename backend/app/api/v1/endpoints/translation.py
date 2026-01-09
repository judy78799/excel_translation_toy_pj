from fastapi import APIRouter, HTTPException
from app.models.translation import (
    TranslationRequest,
    TranslationResponse,
    ExcelTranslationRequest
)
from app.services.translation_service import TranslationService
from app.services.external_api_service import ExternalAPIService
from app.services.file_service import FileService
from app.core.config import settings
from pathlib import Path
import pandas as pd

router = APIRouter()

# Create service instances
api_service = ExternalAPIService()
translation_service = TranslationService(api_service)
file_service = FileService()


@router.post("", response_model=TranslationResponse)
async def translate_texts(request: TranslationRequest):
    """
    Translate a list of texts
    
    - **texts**: List of texts to translate
    - **source_lang**: Source language code (default: ko)
    - **target_lang**: Target language code (default: en)
    """
    
    # Validate languages
    if request.source_lang not in settings.SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported source language. Supported: {settings.SUPPORTED_LANGUAGES}"
        )
    
    if request.target_lang not in settings.SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported target language. Supported: {settings.SUPPORTED_LANGUAGES}"
        )
    
    # Check batch size
    if len(request.texts) > settings.MAX_BATCH_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"Too many texts. Maximum batch size: {settings.MAX_BATCH_SIZE}"
        )
    
    try:
        # Translate texts
        results = await translation_service.translate_texts(
            request.texts,
            request.source_lang,
            request.target_lang
        )
        
        return TranslationResponse(
            success=True,
            data=results,
            total_count=len(results)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


@router.post("/excel", response_model=TranslationResponse)
async def translate_excel_column(request: ExcelTranslationRequest):
    """
    Translate a column from an uploaded Excel file
    
    - **file_id**: ID of the uploaded file
    - **column_index**: Column index to translate (0-based)
    - **source_lang**: Source language code (default: ko)
    - **target_lang**: Target language code (default: en)
    - **sheet_name**: Sheet name (optional, uses first sheet if not specified)
    """
    
    # Validate languages
    if request.source_lang not in settings.SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported source language. Supported: {settings.SUPPORTED_LANGUAGES}"
        )
    
    if request.target_lang not in settings.SUPPORTED_LANGUAGES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported target language. Supported: {settings.SUPPORTED_LANGUAGES}"
        )
    
    try:
        # Get file metadata
        metadata = file_service.get_file_metadata(request.file_id)
        
        # Parse Excel/CSV file using Pandas
        file_path = metadata.file_path
        file_extension = Path(file_path).suffix
        
        if file_extension in ['.xlsx', '.xls']:
            # Load specific sheet if requested, otherwise first sheet (default)
            sheet_name = request.sheet_name if request.sheet_name else 0 
            df = pd.read_excel(file_path, sheet_name=sheet_name)
        else:
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except UnicodeDecodeError:
                df = pd.read_csv(file_path, encoding='cp949')
        
        # Get column data by index
        if request.column_index < 0 or request.column_index >= len(df.columns):
             raise HTTPException(status_code=400, detail=f"Column index {request.column_index} out of range. Max index: {len(df.columns) - 1}")

        # Extract column data, handling NaN/empty values
        column_data = (
            df.iloc[:, request.column_index]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )
        
        if not column_data:
             raise HTTPException(status_code=400, detail="Selected column is empty")
        
        # Translate column
        results = await translation_service.translate_excel_column(
            column_data,
            request.source_lang,
            request.target_lang
        )
        
        return TranslationResponse(
            success=True,
            data=results,
            total_count=len(results)
        )
    
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Translation error: {str(e)}")


@router.get("/languages")
async def get_supported_languages():
    """
    Get list of supported languages
    """
    
    return {
        "success": True,
        "languages": settings.SUPPORTED_LANGUAGES,
        "default_source": settings.DEFAULT_SOURCE_LANG,
        "default_target": settings.DEFAULT_TARGET_LANG
    }