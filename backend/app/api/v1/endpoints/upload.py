from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.file import FileUploadResponse
from app.services.file_service import FileService
from app.core.config import settings
from pathlib import Path

router = APIRouter()

# Create file service instance
file_service = FileService()


@router.post("/", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """
    Upload an Excel file for translation processing
    
    - **file**: Excel file (.xlsx or .xls)
    
    Returns file metadata including file_id for subsequent translation requests
    """
    
    # Check file extension
    file_extension = Path(file.filename).suffix
    if file_extension not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed extensions: {settings.ALLOWED_EXTENSIONS}"
        )
    
    # Check file size
    file.file.seek(0, 2)  # Seek to end
    file_size = file.file.tell()
    file.file.seek(0)  # Reset to beginning
    
    if file_size > settings.MAX_FILE_SIZE:
        raise HTTPException(
            status_code=400,
            detail=f"File too large. Max size: {settings.MAX_FILE_SIZE / (1024*1024)}MB"
        )
    
    try:
        # Save file and get metadata
        metadata = await file_service.save_uploaded_file(file)
        
        # Return response
        return FileUploadResponse(
            success=True,
            file_id=metadata.file_id,
            filename=metadata.filename,
            file_size=metadata.file_size,
            upload_time=metadata.upload_time.isoformat(),
            sheet_names=metadata.sheet_names,
            row_count=metadata.row_count,
            column_count=metadata.column_count
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading file: {str(e)}")


@router.delete("/{file_id}")
async def delete_file(file_id: str):
    """
    Delete an uploaded file
    
    - **file_id**: ID of the file to delete
    """
    
    success = file_service.delete_file(file_id)
    
    if not success:
        raise HTTPException(status_code=404, detail="File not found")
    
    return {"success": True, "message": "File deleted successfully"}


@router.get("/{file_id}/info")
async def get_file_info(file_id: str):
    """
    Get metadata for an uploaded file
    
    - **file_id**: ID of the file
    """
    
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
