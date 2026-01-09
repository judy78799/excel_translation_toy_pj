from pydantic import BaseModel, Field
from typing import List, Optional

# 텍스트 리스트를 받아서 빈 칸 필터링 후, 외부 번역 API를 호출하여 번역된 결과를 받아옴.
# 이후 번역된 테스트를 원래 순서에 맞게 다시 끼워 맞츰
class TranslationRequest(BaseModel):
    """Request model for translation"""
    texts: List[str] = Field(..., description="List of texts to translate")
    source_lang: str = Field(default="ko", description="Source language code")
    target_lang: str = Field(default="en", description="Target language code")
    
    class Config:
        json_schema_extra = {
            "example": {
                "texts": ["안녕하세요", "감사합니다"],
                "source_lang": "ko",
                "target_lang": "en"
            }
        }


class TranslationItem(BaseModel):
    """Single translation item"""
    original: str
    translated: str
    source_lang: str
    target_lang: str


class TranslationResponse(BaseModel):
    """Response model for translation"""
    success: bool
    data: List[TranslationItem]
    total_count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "data": [
                    {
                        "original": "안녕하세요",
                        "translated": "Hello",
                        "source_lang": "ko",
                        "target_lang": "en"
                    }
                ],
                "total_count": 1
            }
        }


class ExcelTranslationRequest(BaseModel):
    """Request model for Excel file translation"""
    file_id: str = Field(..., description="Uploaded file ID")
    column_index: int = Field(default=0, description="Column index to translate (0-based)")
    source_lang: str = Field(default="ko", description="Source language code")
    target_lang: str = Field(default="en", description="Target language code")
    sheet_name: Optional[str] = Field(None, description="Sheet name (if None, use first sheet)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "file_id": "abc123",
                "column_index": 0,
                "source_lang": "ko",
                "target_lang": "en",
                "sheet_name": "Sheet1"
            }
        }
