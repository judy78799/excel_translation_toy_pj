import styled from 'styled-components';

export const ResultContainer = styled.div`
  background: var(--bg-secondary);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  box-shadow: var(--shadow-md);
  margin-top: var(--space-lg);
`;

export const TableHeader = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-md);
`;

export const TableTitle = styled.h2`
  font-size: 1.5rem;
  color: var(--text-primary);
  margin: 0;
`;

export const TableWrapper = styled.div`
  overflow-x: auto;
  border-radius: var(--radius-md);
  
  &::-webkit-scrollbar {
    height: 8px;
  }
`;

export const Table = styled.table`
  width: 100%;
  border-collapse: collapse;
  font-size: 0.95rem;
`;

export const TableHead = styled.thead`
  background: var(--bg-tertiary);
  
  th {
    padding: 1rem;
    text-align: left;
    font-weight: 600;
    color: var(--primary-light);
    border-bottom: 2px solid var(--primary);
  }
`;

export const TableBody = styled.tbody`
  tr {
    border-bottom: 1px solid var(--border);
    transition: background var(--transition-fast);
    
    &:hover {
      background: var(--bg-tertiary);
    }
    
    &:last-child {
      border-bottom: none;
    }
  }
  
  td {
    padding: 1rem;
    color: var(--text-secondary);
    vertical-align: top;
    max-width: 400px;
    word-wrap: break-word;
  }
`;

export const RowNumber = styled.td`
  color: var(--text-tertiary);
  font-weight: 500;
  width: 60px;
`;

export const EmptyState = styled.div`
  text-align: center;
  padding: var(--space-xl);
  color: var(--text-tertiary);
  font-size: 1.1rem;
`;
