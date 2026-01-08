import styled from 'styled-components';

export const FileUploadContainer = styled.div`
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-md);
`;

export const DropZone = styled.div`
  border: 2px dashed ${props => props.isDragActive ? 'var(--primary)' : 'var(--border)'};
  border-radius: var(--radius-md);
  padding: var(--space-xl);
  text-align: center;
  cursor: pointer;
  transition: all var(--transition-normal);
  background: ${props => props.isDragActive ? 'rgba(124, 58, 237, 0.05)' : 'var(--bg-tertiary)'};

  &:hover {
    border-color: var(--primary);
    background: rgba(124, 58, 237, 0.05);
  }
`;

export const DropZoneIcon = styled.div`
  font-size: 3rem;
  margin-bottom: var(--space-sm);
`;

export const DropZoneText = styled.p`
  color: var(--text-secondary);
  margin: 0.5rem 0;
  
  strong {
    color: var(--primary);
  }
`;

export const FileInfo = styled.div`
  margin-top: var(--space-md);
  padding: var(--space-md);
  background: var(--bg-tertiary);
  border-radius: var(--radius-md);
  border-left: 4px solid var(--primary);
`;

export const FileInfoItem = styled.p`
  margin: 0.5rem 0;
  color: var(--text-secondary);
  font-size: 0.9rem;
  
  strong {
    color: var(--text-primary);
  }
`;

export const ControlsContainer = styled.div`
  margin-top: var(--space-md);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
`;

export const ControlGroup = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--space-sm);
`;

export const Label = styled.label`
  display: block;
  margin-bottom: 0.5rem;
  color: var(--text-primary);
  font-weight: 500;
  font-size: 0.9rem;
`;
