import { useState } from 'react';
import { translateFile } from '../services/translationService';

export const useTranslation = () => {
    const [translating, setTranslating] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);

    const translate = async (fileId, columnIndex, sourceLang, targetLang, sheetName = null) => {
        setTranslating(true);
        setError(null);

        try {
            const response = await translateFile(fileId, columnIndex, sourceLang, targetLang, sheetName);
            setResults(response.data);
            return response.data;
        } catch (err) {
            setError(err.message || 'Translation failed');
            return null;
        } finally {
            setTranslating(false);
        }
    };

    const reset = () => {
        setResults(null);
        setError(null);
        setTranslating(false);
    };

    return {
        translating,
        results,
        error,
        translate,
        reset,
    };
};
