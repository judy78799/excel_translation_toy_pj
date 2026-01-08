import { MAX_FILE_SIZE, ALLOWED_EXTENSIONS } from '../constants/languages';

export const validateFile = (file) => {
    if (!file) {
        return 'No file selected';
    }

    // Check file size
    if (file.size > MAX_FILE_SIZE) {
        return `File size exceeds ${MAX_FILE_SIZE / (1024 * 1024)}MB limit`;
    }

    // Check file extension
    const fileName = file.name.toLowerCase();
    const isValidExtension = ALLOWED_EXTENSIONS.some(ext => fileName.endsWith(ext));

    if (!isValidExtension) {
        return `Invalid file type. Allowed: ${ALLOWED_EXTENSIONS.join(', ')}`;
    }

    return null; // No error
};
