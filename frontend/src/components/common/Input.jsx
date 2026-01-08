import styled from 'styled-components';

const StyledInput = styled.input`
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  background: var(--bg-tertiary);
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-family: 'Inter', sans-serif;
  transition: all var(--transition-normal);

  &:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
  }

  &::placeholder {
    color: var(--text-tertiary);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

const StyledSelect = styled.select`
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  background: var(--bg-tertiary);
  border: 2px solid var(--border);
  border-radius: var(--radius-md);
  color: var(--text-primary);
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all var(--transition-normal);

  &:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 3px rgba(124, 58, 237, 0.1);
  }

  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
`;

export const Input = (props) => <StyledInput {...props} />;
export const Select = (props) => <StyledSelect {...props} />;
