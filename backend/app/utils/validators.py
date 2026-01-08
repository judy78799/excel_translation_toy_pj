from pathlib import Path
from fastapi import UploadFile, HTTPException
from app.core.config import settings


def validate_file_size(file: UploadFile) -> bool:
    """Validate file size"""
    # Note: file.size might not be available in all cases
    # We'll check during actual reading
    return True


def validate_file_extension(filename: str) -> bool:
    """Validate file extension"""
    file_ext = Path(filename).suffix.lower()
    return file_ext in settings.ALLOWED_EXTENSIONS


async def validate_uploaded_file(file: UploadFile) -> None:
    """Validate uploaded file"""
    
    # Check if file is present
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    # Check file extension
    if not validate_file_extension(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )
    
    # Check file size
    content = await file.read()
    if len(content) > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    # Reset file pointer
    await file.seek(0)


def validate_language_code(lang_code: str) -> bool:
    """Validate language code"""
    return lang_code in settings.SUPPORTED_LANGUAGES


def validate_column_index(column_index: int, max_columns: int) -> None:
    """Validate column index"""
    if column_index < 0 or column_index >= max_columns:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid column index. Must be between 0 and {max_columns - 1}"
        )
