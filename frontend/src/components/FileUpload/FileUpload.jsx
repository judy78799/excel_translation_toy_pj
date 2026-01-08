import { useState, useRef } from 'react';
import { StyledButton } from '../common/Button';
import { Select } from '../common/Input';
import { Alert } from '../common/Alert';
import { SUPPORTED_LANGUAGES, DEFAULT_SOURCE_LANG, DEFAULT_TARGET_LANG } from '../../constants/languages';
import {
    FileUploadContainer,
    DropZone,
    DropZoneIcon,
    DropZoneText,
    FileInfo,
    FileInfoItem,
    ControlsContainer,
    ControlGroup,
    Label
} from './FileUpload.styles';

export const FileUpload = ({
    onFileSelect,
    onUpload,
    file,
    fileMetadata,
    uploading,
    error
}) => {
    const [isDragActive, setIsDragActive] = useState(false);
    const [sourceLang, setSourceLang] = useState(DEFAULT_SOURCE_LANG);
    const [targetLang, setTargetLang] = useState(DEFAULT_TARGET_LANG);
    const [columnIndex, setColumnIndex] = useState(0);
    const fileInputRef = useRef(null);

    const handleDragEnter = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(true);
    };

    const handleDragLeave = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);
    };

    const handleDragOver = (e) => {
        e.preventDefault();
        e.stopPropagation();
    };

    const handleDrop = (e) => {
        e.preventDefault();
        e.stopPropagation();
        setIsDragActive(false);

        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile) {
            onFileSelect(droppedFile);
        }
    };

    const handleFileInputChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            onFileSelect(selectedFile);
        }
    };

    const handleUploadClick = async () => {
        await onUpload({ sourceLang, targetLang, columnIndex });
    };

    return (
        <FileUploadContainer className="fade-in">
            <DropZone
                isDragActive={isDragActive}
                onDragEnter={handleDragEnter}
                onDragLeave={handleDragLeave}
                onDragOver={handleDragOver}
                onDrop={handleDrop}
                onClick={() => fileInputRef.current?.click()}
            >
                <DropZoneIcon>📄</DropZoneIcon>
                <DropZoneText>
                    <strong>Click to upload</strong> or drag and drop
                </DropZoneText>
                <DropZoneText style={{ fontSize: '0.85rem' }}>
                    Excel files (.xlsx, .xls) up to 10MB
                </DropZoneText>
                <input
                    ref={fileInputRef}
                    type="file"
                    accept=".xlsx,.xls"
                    onChange={handleFileInputChange}
                    style={{ display: 'none' }}
                />
            </DropZone>

            {file && (
                <FileInfo>
                    <FileInfoItem><strong>File:</strong> {file.name}</FileInfoItem>
                    <FileInfoItem><strong>Size:</strong> {(file.size / 1024).toFixed(2)} KB</FileInfoItem>
                    {fileMetadata && (
                        <>
                            <FileInfoItem><strong>Sheets:</strong> {fileMetadata.sheet_names.join(', ')}</FileInfoItem>
                            <FileInfoItem><strong>Rows:</strong> {fileMetadata.row_count}</FileInfoItem>
                            <FileInfoItem><strong>Columns:</strong> {fileMetadata.column_count}</FileInfoItem>
                        </>
                    )}
                </FileInfo>
            )}

            {fileMetadata && (
                <ControlsContainer>
                    <ControlGroup>
                        <div>
                            <Label>Column Index</Label>
                            <Select
                                value={columnIndex}
                                onChange={(e) => setColumnIndex(parseInt(e.target.value))}
                            >
                                {Array.from({ length: fileMetadata.column_count }, (_, i) => (
                                    <option key={i} value={i}>Column {i}</option>
                                ))}
                            </Select>
                        </div>
                        <div>
                            <Label>Source Language</Label>
                            <Select
                                value={sourceLang}
                                onChange={(e) => setSourceLang(e.target.value)}
                            >
                                {SUPPORTED_LANGUAGES.map(lang => (
                                    <option key={lang.code} value={lang.code}>{lang.name}</option>
                                ))}
                            </Select>
                        </div>
                        <div>
                            <Label>Target Language</Label>
                            <Select
                                value={targetLang}
                                onChange={(e) => setTargetLang(e.target.value)}
                            >
                                {SUPPORTED_LANGUAGES.map(lang => (
                                    <option key={lang.code} value={lang.code}>{lang.name}</option>
                                ))}
                            </Select>
                        </div>
                    </ControlGroup>
                    <StyledButton
                        variant="primary"
                        onClick={handleUploadClick}
                        disabled={uploading}
                        loading={uploading}
                    >
                        {uploading ? 'Translating...' : 'Start Translation'}
                    </StyledButton>
                </ControlsContainer>
            )}

            {error && <Alert type="error" message={error} />}
        </FileUploadContainer>
    );
};
