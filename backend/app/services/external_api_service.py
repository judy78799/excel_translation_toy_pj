import httpx
import asyncio
from typing import List
import html
from app.core.config import settings


class ExternalAPIService:
    """Service for external translation API calls"""
    
    def __init__(self):
        self.api_key = settings.TRANSLATION_API_KEY
        self.api_url = settings.TRANSLATION_API_URL
        self.use_mock = settings.USE_MOCK_TRANSLATION
        self.timeout = settings.REQUEST_TIMEOUT
    
    async def translate_text(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str
    ) -> str:
        """Translate a single text"""
        if self.use_mock:
            return await self._mock_translate(text, source_lang, target_lang)
        else:
            return await self._real_translate(text, source_lang, target_lang)
    
    async def translate_batch(
        self, 
        texts: List[str], 
        source_lang: str, 
        target_lang: str
    ) -> List[str]:
        """Translate multiple texts in batch"""
        # Process in batches to avoid overwhelming the API
        batch_size = settings.MAX_BATCH_SIZE
        results = []
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i + batch_size]
            batch_results = await asyncio.gather(
                *[self.translate_text(text, source_lang, target_lang) for text in batch]
            )
            results.extend(batch_results)
        
        return results
    
    async def _mock_translate(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str
    ) -> str:
        """Mock translation for testing (adds a prefix)"""
        # Simulate API delay
        await asyncio.sleep(0.1)
        
        # Simple mock: add language code and reverse
        if not text or text.strip() == "":
            return ""
        
        return f"[{target_lang.upper()}] {text}"
    
    async def _real_translate(
        self, 
        text: str, 
        source_lang: str, 
        target_lang: str
    ) -> str:
        """Real translation using external API (Google Translate format)"""
        if not text or text.strip() == "":
            return ""
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                params = {
                    "q": text,
                    "source": source_lang,
                    "target": target_lang,
                    "key": self.api_key,
                }
                
                response = await client.post(self.api_url, params=params)
                response.raise_for_status()
                
                data = response.json()
                translated = data["data"]["translations"][0]["translatedText"]
                return html.unescape(translated)
        
        except httpx.HTTPError as e:
            # Fallback to mock if API fails
            print(f"Translation API error: {e}. Falling back to mock.")
            return await self._mock_translate(text, source_lang, target_lang)
        except Exception as e:
            print(f"Unexpected error: {e}. Falling back to mock.")
            return await self._mock_translate(text, source_lang, target_lang)
