from sqlalchemy.orm import Session
from app.models.dataset import TranslationDataset
from typing import Optional

class DatasetService:
    def __init__(self, db: Session):
        self.db = db

    def save_record(
        self,
        source_text: str,
        translated_text: str,
        back_translated_text: str,
        source_lang: str,
        target_lang: str,
        quality_metrics: dict
    ) -> TranslationDataset:
        """
        Save a single translation record to the dataset table.
        """
        record = TranslationDataset(
            source_text=source_text,
            translated_text=translated_text,
            back_translated_text=back_translated_text,
            source_lang=source_lang,
            target_lang=target_lang,
            semantic_score=quality_metrics.get("semantic_score"),
            final_score=quality_metrics.get("final_score"),
            failure_type=quality_metrics.get("failure_type"),
            is_trained=False
        )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record
