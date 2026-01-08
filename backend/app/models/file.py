from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class FileUploadResponse(BaseModel):
    """Response model for file upload"""
    success: bool
    file_id: str
    filename: str
    file_size: int
    upload_time: str
    sheet_names: list[str]
    row_count: int
    column_count: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "file_id": "abc123",
                "filename": "sample.xlsx",
                "file_size": 12345,
                "upload_time": "2024-01-01T12:00:00",
                "sheet_names": ["Sheet1"],
                "row_count": 100,
                "column_count": 5
            }
        }


class FileMetadata(BaseModel):
    """File metadata storage"""
    file_id: str
    filename: str
    file_path: str
    file_size: int
    upload_time: datetime
    sheet_names: list[str]
    row_count: int
    column_count: int
