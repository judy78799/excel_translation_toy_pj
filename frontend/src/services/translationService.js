import api from './api';

export const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await api.post('/api/v1/upload', formData, {
        headers: {
            'Content-Type': 'multipart/form-data',
        },
    });

    return response.data;
};

export const translateFile = async (fileId, columnIndex, sourceLang, targetLang, sheetName = null) => {
    const response = await api.post('/api/v1/translate', {
        file_id: fileId,
        column_index: columnIndex,
        source_lang: sourceLang,
        target_lang: targetLang,
        sheet_name: sheetName,
    });

    return response.data;
};
