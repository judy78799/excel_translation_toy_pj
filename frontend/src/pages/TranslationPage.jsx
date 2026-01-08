import { useState } from 'react';
import styled from 'styled-components';
import { FileUpload } from '../components/FileUpload/FileUpload';
import { ResultTable } from '../components/ResultTable/ResultTable';
import { Alert } from '../components/Alert';
import { useFileUpload } from '../hooks/useFileUpload';
import { useTranslation } from '../hooks/useTranslation';

const PageContainer = styled.div`
  min-height: 100vh;
  padding: var(--space-xl) var(--space-md);
`;

const PageHeader = styled.div`
  max-width: 1200px;
  margin: 0 auto var(--space-xl);
  text-align: center;
`;

const PageTitle = styled.h1`
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: var(--space-sm);
  background: linear-gradient(135deg, var(--primary-light) 0%, var(--secondary) 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
`;

const PageDescription = styled.p`
  font-size: 1.1rem;
  color: var(--text-secondary);
`;

const ContentContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
`;

export const TranslationPage = () => {
    const {
        file,
        fileMetadata,
        uploading,
        error: uploadError,
        handleFileSelect,
        handleUpload: uploadFile,
        reset: resetUpload
    } = useFileUpload();

    const {
        translating,
        results,
        error: translationError,
        translate,
        reset: resetTranslation
    } = useTranslation();

    const handleFileSelection = (selectedFile) => {
        const success = handleFileSelect(selectedFile);
        if (success) {
            resetTranslation();
        }
        return success;
    };

    const handleUploadAndTranslate = async ({ sourceLang, targetLang, columnIndex }) => {
        // Upload file if not uploaded yet
        let metadata = fileMetadata;
        if (!metadata) {
            metadata = await uploadFile();
            if (!metadata) return;
        }

        // Translate
        await translate(metadata.file_id, columnIndex, sourceLang, targetLang);
    };

    return (
        <PageContainer>
            <PageHeader>
                <PageTitle>Translate Excel Files</PageTitle>
                <PageDescription>
                    Upload your Excel file and select the column you want to translate
                </PageDescription>
            </PageHeader>

            <ContentContainer>
                <FileUpload
                    onFileSelect={handleFileSelection}
                    onUpload={handleUploadAndTranslate}
                    file={file}
                    fileMetadata={fileMetadata}
                    uploading={uploading || translating}
                    error={uploadError || translationError}
                />

                {results && <ResultTable results={results} />}
            </ContentContainer>
        </PageContainer>
    );
};
