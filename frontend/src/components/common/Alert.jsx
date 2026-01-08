import styled from 'styled-components';

const AlertContainer = styled.div`
  padding: 1rem 1.25rem;
  border-radius: var(--radius-md);
  margin: 1rem 0;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  animation: fadeIn var(--transition-normal);

  ${props => props.type === 'error' && `
    background: rgba(239, 68, 68, 0.1);
    border: 1px solid var(--error);
    color: #fca5a5;
  `}

  ${props => props.type === 'success' && `
    background: rgba(34, 197, 94, 0.1);
    border: 1px solid var(--success);
    color: #86efac;
  `}

  ${props => props.type === 'info' && `
    background: rgba(124, 58, 237, 0.1);
    border: 1px solid var(--primary);
    color: var(--primary-light);
  `}
`;

const AlertIcon = styled.span`
  font-size: 1.25rem;
`;

const AlertMessage = styled.div`
  flex: 1;
  font-size: 0.95rem;
`;

export const Alert = ({ type = 'info', message, icon }) => {
    const defaultIcons = {
        error: '⚠️',
        success: '✓',
        info: 'ℹ️'
    };

    return (
        <AlertContainer type={type}>
            <AlertIcon>{icon || defaultIcons[type]}</AlertIcon>
            <AlertMessage>{message}</AlertMessage>
        </AlertContainer>
    );
};
