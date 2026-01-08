import styled from 'styled-components';

export const StyledButton = styled.button`
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-normal);
  font-family: 'Inter', sans-serif;
  position: relative;
  overflow: hidden;

  ${props => props.variant === 'primary' && `
    background: linear-gradient(135deg, var(--primary) 0%, var(--primary-light) 100%);
    color: white;
    box-shadow: var(--shadow-md);
    
    &:hover {
      transform: translateY(-2px);
      box-shadow: var(--shadow-lg), var(--shadow-glow);
    }
    
    &:active {
      transform: translateY(0);
    }
  `}

  ${props => props.variant === 'secondary' && `
    background: var(--bg-tertiary);
    color: var(--text-primary);
    border: 2px solid var(--border);
    
    &:hover {
      border-color: var(--primary);
      background: var(--bg-secondary);
    }
  `}

  ${props => props.disabled && `
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  `}

  ${props => props.loading && `
    color: transparent;
    
    &::after {
      content: '';
      position: absolute;
      width: 16px;
      height: 16px;
      top: 50%;
      left: 50%;
      margin-left: -8px;
      margin-top: -8px;
      border: 2px solid white;
      border-radius: 50%;
      border-top-color: transparent;
      animation: spin 0.6s linear infinite;
    }
    
    @keyframes spin {
      to { transform: rotate(360deg); }
    }
  `}
`;
