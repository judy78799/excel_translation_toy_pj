from fastapi import Depends
from app.services.translation_service import TranslationService
from app.services.file_service import FileService
from app.services.external_api_service import ExternalAPIService


def get_external_api_service() -> ExternalAPIService:
    """Dependency for external API service"""
    return ExternalAPIService()


def get_translation_service(
    api_service: ExternalAPIService = Depends(get_external_api_service)
) -> TranslationService:
    """Dependency for translation service"""
    return TranslationService(api_service)


def get_file_service() -> FileService:
    """Dependency for file service"""
    return FileService()
