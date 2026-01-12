from sentence_transformers import SentenceTransformer, util
import numpy as np
import re

class QualityService:
    _instance = None
    _model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(QualityService, cls).__new__(cls)
            # Load model once - usage of a lightweight model
            print("Loading Sentence-BERT model...")
            cls._model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')
            print("Sentence-BERT model loaded.")
        return cls._instance

    def calculate_quality(self, source_text: str, back_translated_text: str) -> dict:
        """
        Calculate quality score based on:
        1. Semantic Similarity (Sentence-BERT) - 60%
        2. Length Ratio - 20%
        3. Keyword Preservation (Heuristic) - 20%
        """
        if not source_text or not back_translated_text:
            return {"final_score": 0.0, "semantic_score": 0.0, "failure_type": "empty_text"}

        # 1. Semantic Score
        embeddings1 = self._model.encode(source_text, convert_to_tensor=True)
        embeddings2 = self._model.encode(back_translated_text, convert_to_tensor=True)
        
        # Determine score
        semantic_score = util.pytorch_cos_sim(embeddings1, embeddings2).item()
        semantic_score = max(0.0, min(1.0, semantic_score)) # Clip to 0-1

        # 2. Length Ratio Score
        len_source = len(source_text)
        len_back = len(back_translated_text)
        
        if len_source == 0:
            length_score = 0
        else:
            ratio = len_back / len_source
            # Perfect ratio is 1.0. Penalize deviation.
            # If ratio is 0.5 or 1.5, score drops.
            # Using Gaussian-like decay or simple linear penalty
            diff = abs(1.0 - ratio)
            length_score = max(0.0, 1.0 - diff)

        # 3. Keyword Check (Simple Numbers/Proper Noun Heuristic)
        # Check if numbers present in source are in back-translation
        source_numbers = set(re.findall(r'\d+', source_text))
        back_numbers = set(re.findall(r'\d+', back_translated_text))
        
        if not source_numbers:
            keyword_score = 1.0
        else:
            matches = source_numbers.intersection(back_numbers)
            keyword_score = len(matches) / len(source_numbers)

        # Final Weighted Score
        final_score = (0.6 * semantic_score) + (0.2 * length_score) + (0.2 * keyword_score)

        # Failure Classification Suggestion
        failure_type = None
        if final_score < 0.5:
            if semantic_score < 0.4:
                failure_type = "severe_semantic_mismatch"
            elif length_score < 0.3:
                failure_type = "length_mismatch_hallucination"
            elif keyword_score < 0.5:
                failure_type = "number_mismatch"
            else:
                failure_type = "general_low_quality"

        return {
            "final_score": round(final_score, 4),
            "semantic_score": round(semantic_score, 4),
            "length_score": round(length_score, 4),
            "keyword_score": round(keyword_score, 4),
            "failure_type": failure_type
        }
