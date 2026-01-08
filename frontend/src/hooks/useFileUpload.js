import { useState } from 'react';
import { uploadFile } from '../services/translationService';
import { validateFile } from '../utils/fileValidator';

export const useFileUpload = () => {
    const [file, setFile] = useState(null);
    const [fileMetadata, setFileMetadata] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [error, setError] = useState(null);

    const handleFileSelect = (selectedFile) => {
        setError(null);

        // Validate file
        const validationError = validateFile(selectedFile);
        if (validationError) {
            setError(validationError);
            setFile(null);
            return false;
        }

        setFile(selectedFile);
        return true;
    };

    const handleUpload = async () => {
        if (!file) {
            setError('No file selected');
            return null;
        }

        setUploading(true);
        setError(null);

        try {
            const metadata = await uploadFile(file);
            setFileMetadata(metadata);
            return metadata;
        } catch (err) {
            setError(err.message || 'Upload failed');
            return null;
        } finally {
            setUploading(false);
        }
    };

    const reset = () => {
        setFile(null);
        setFileMetadata(null);
        setError(null);
        setUploading(false);
    };

    return {
        file,
        fileMetadata,
        uploading,
        error,
        handleFileSelect,
        handleUpload,
        reset,
    };
};
