from typing import List
from app.models.translation import TranslationItem
from app.services.external_api_service import ExternalAPIService


class TranslationService:
    """Service for translation business logic"""
    
    def __init__(self, api_service: ExternalAPIService):
        self.api_service = api_service
    
    async def translate_texts(
        self,
        texts: List[str],
        source_lang: str,
        target_lang: str
    ) -> List[TranslationItem]:
        """Translate a list of texts and return structured results"""
        
        # Filter out empty texts but preserve indices
        non_empty_texts = []
        non_empty_indices = []
        
        for i, text in enumerate(texts):
            if text and text.strip():
                non_empty_texts.append(text)
                non_empty_indices.append(i)
        
        # Translate non-empty texts
        if non_empty_texts:
            translated_texts = await self.api_service.translate_batch(
                non_empty_texts, source_lang, target_lang
            )
        else:
            translated_texts = []
        
        # Build results with proper ordering
        results = []
        translation_map = dict(zip(non_empty_indices, translated_texts))
        
        for i, original in enumerate(texts):
            translated = translation_map.get(i, "")
            results.append(
                TranslationItem(
                    original=original,
                    translated=translated,
                    source_lang=source_lang,
                    target_lang=target_lang
                )
            )
        
        return results
    
    async def translate_excel_column(
        self,
        column_data: List[str],
        source_lang: str,
        target_lang: str
    ) -> List[TranslationItem]:
        """Translate an Excel column"""
        return await self.translate_texts(column_data, source_lang, target_lang)

    async def perform_back_translation(
        self,
        translated_texts: List[str],
        source_lang: str,
        target_lang: str
    ) -> List[str]:
        """
        Perform back-translation (Target -> Source)
        Used for Quality Estimation
        """
        # Swap source/target
        back_translated = await self.api_service.translate_batch(
            translated_texts, 
            source_lang=target_lang,  
            target_lang=source_lang
        )
        return back_translated
