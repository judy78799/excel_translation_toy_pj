from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.translation_service import TranslationService
from app.services.external_api_service import ExternalAPIService
from app.services.file_service import FileService
from app.services.quality_service import QualityService
from app.services.dataset_service import DatasetService
import pandas as pd
import io

router = APIRouter()

@router.post("/generate")
async def generate_dataset(
    file: UploadFile = File(...),
    source_lang: str = Form("ko"),
    target_lang: str = Form("en"),
    text_column: str = Form("text"),
    db: Session = Depends(get_db)
):
    """
    Generate translation dataset:
    1. Parse Excel
    2. Translate (Source -> Target)
    3. Back Translate (Target -> Source)
    4. Calculate Quality Score
    5. Save to DB
    """
    # 1. Parse File
    contents = await file.read()
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(contents))
        else:
            df = pd.read_excel(io.BytesIO(contents))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"File parse error: {str(e)}")

    if text_column not in df.columns:
        raise HTTPException(status_code=400, detail=f"Column '{text_column}' not found")

    source_texts = df[text_column].dropna().astype(str).tolist()
    
    # Initialize Services
    ext_api = ExternalAPIService()
    trans_service = TranslationService(ext_api)
    quality_service = QualityService()
    dataset_service = DatasetService(db)

    results = []
    
    # 2. Batch Translation (Source -> Target)
    # Note: For large files, we should chunk this. For toy project, keeping it simple.
    translated_items = await trans_service.translate_texts(source_texts, source_lang, target_lang)
    translated_texts = [item.translated for item in translated_items]

    # 3. Batch Back-Translation (Target -> Source)
    back_translated_texts = await trans_service.perform_back_translation(
        translated_texts, source_lang, target_lang
    )

    # 4. Score & Save
    saved_count = 0
    response_data = []

    for src, trans, back_trans in zip(source_texts, translated_texts, back_translated_texts):
        # Calculate Quality
        quality = quality_service.calculate_quality(src, back_trans)
        
        # Save to DB
        dataset_service.save_record(
            source_text=src,
            translated_text=trans,
            back_translated_text=back_trans,
            source_lang=source_lang,
            target_lang=target_lang,
            quality_metrics=quality
        )
        saved_count += 1
        
        response_data.append({
            "source": src,
            "translated": trans,
            "back_translated": back_trans,
            "score": quality["final_score"],
            "failure_type": quality["failure_type"]
        })

    return {
        "total_processed": len(source_texts),
        "saved_to_db": saved_count,
        "sample_results": response_data[:5] # Return top 5 as sample
    }
