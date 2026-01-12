from sqlalchemy import Column, String, Float, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime
from app.core.database import Base

class TranslationDataset(Base):
    __tablename__ = "translation_dataset"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    
    # Core Translation Data (Log Features)
    source_text = Column(Text, nullable=False)
    translated_text = Column(Text, nullable=False)
    back_translated_text = Column(Text, nullable=True)
    
    # Metadata
    source_lang = Column(String(10), nullable=False)
    target_lang = Column(String(10), nullable=False)
    
    # Quality Metrics (Labels/Features)
    semantic_score = Column(Float, nullable=True)  # From Sentence-BERT
    final_score = Column(Float, nullable=True)     # Weighted Sum
    
    # ML Target Labels
    failure_type = Column(String(50), nullable=True)  # e.g., "semantic_loss", "length_mismatch"
    
    # System Metadata
    is_trained = Column(Boolean, default=False)
    model_version = Column(String(50), nullable=True)  # Allows tracking which model generated this
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<TranslationDataset(id={self.id}, score={self.final_score})>"
