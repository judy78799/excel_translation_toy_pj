import os
import uuid
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict
from fastapi import UploadFile
from app.core.config import settings
from app.models.file import FileMetadata
from app.models.file import FileMetadata
import pandas as pd


class FileService:
    """Service for file upload and management"""
    
    def __init__(self):
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.upload_dir.mkdir(exist_ok=True)
        self.file_metadata: Dict[str, FileMetadata] = {}
    
    async def save_uploaded_file(self, file: UploadFile) -> FileMetadata:
        """Save uploaded file and return metadata"""
        
        # Generate unique file ID
        file_id = str(uuid.uuid4())
        
        # Create file path
        file_extension = Path(file.filename).suffix
        file_path = self.upload_dir / f"{file_id}{file_extension}"
        
        # Save file
        with open(file_path, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        
        # Parse File to get metadata using Pandas
        try:
            if file_extension in ['.xlsx', '.xls']:
                xl = pd.ExcelFile(file_path)
                sheet_names = xl.sheet_names
                df = pd.read_excel(file_path)
            else:
                sheet_names = ['Sheet1']
                try:
                    df = pd.read_csv(file_path, encoding='utf-8-sig')
                except UnicodeDecodeError:
                    df = pd.read_csv(file_path, encoding='cp949')
            
            row_count = len(df)
            column_count = len(df.columns)
        except Exception as e:
            # If parsing fails, we might want to log it and raise proper error
            # For now, let's ensure we don't return partial invalid metadata
            # But the file is already saved.
            # Let's raise value error as in the usages
            raise ValueError(f"Failed to parse file: {str(e)}")
        
        # Create metadata
        metadata = FileMetadata(
            file_id=file_id,
            filename=file.filename,
            file_path=str(file_path),
            file_size=len(content),
            upload_time=datetime.now(),
            sheet_names=sheet_names,
            row_count=row_count,
            column_count=column_count
        )
        
        # Store metadata
        self.file_metadata[file_id] = metadata
        
        return metadata
    
    def get_file_metadata(self, file_id: str) -> FileMetadata:
        """Get file metadata by ID"""
        if file_id not in self.file_metadata:
            raise ValueError(f"File not found: {file_id}")
        return self.file_metadata[file_id]
    
    def delete_file(self, file_id: str) -> bool:
        """Delete uploaded file"""
        if file_id not in self.file_metadata:
            return False
        
        metadata = self.file_metadata[file_id]
        file_path = Path(metadata.file_path)
        
        if file_path.exists():
            file_path.unlink()
        
        del self.file_metadata[file_id]
        return True
    
    def cleanup_old_files(self, max_age_hours: int = 24):
        """Clean up files older than specified hours"""
        current_time = datetime.now()
        to_delete = []
        
        for file_id, metadata in self.file_metadata.items():
            age = current_time - metadata.upload_time
            if age.total_seconds() > max_age_hours * 3600:
                to_delete.append(file_id)
        
        for file_id in to_delete:
            self.delete_file(file_id)
