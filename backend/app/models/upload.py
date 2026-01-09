from pydantic import BaseModel
from typing import List

class TranslationResult(BaseModel):
    """번역 결과 항목"""
    original: str
    translated: str
    source_lang: str
    target_lang: str
    
class FileUploadResponse(BaseModel):
    """파일 업로드 및 번역 응답"""
    status: str
    total_rows: int
    success_count: int
    error_count: int
    results: List[TranslationResult]
    processing_time: float
    file_name: str
