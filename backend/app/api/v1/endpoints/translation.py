from fastapi import APIRouter, HTTPException
from app.models.translation import (
    TranslationRequest,
    TranslationResponse,
    ExcelTranslationRequest
)
from app.services.translation_service import TranslationService
from app.services.external_api_service import ExternalAPIService
from app.services.file_service import FileService
from app.utils.file_parser import ExcelParser
from app.core.config import settings

router = APIRouter()

# Create service instances
api_service = ExternalAPIService()
translation_service = TranslationService(api_service)
file_service = FileService()


@router.post("/", response_model=TranslationResponse)
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
        
        # Parse Excel file
        parser = ExcelParser(metadata.file_path)
        
        # Get column data
        column_data = parser.get_column_data(
            column_index=request.column_index,
            sheet_name=request.sheet_name
        )
        
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
