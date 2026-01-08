import { StyledButton } from '../common/Button';
import { exportToCSV } from '../../utils/csvExporter';
import {
    ResultContainer,
    TableHeader,
    TableTitle,
    TableWrapper,
    Table,
    TableHead,
    TableBody,
    RowNumber,
    EmptyState
} from './ResultTable.styles';

export const ResultTable = ({ results }) => {
    if (!results || results.length === 0) {
        return null;
    }

    const handleExport = () => {
        exportToCSV(results, 'translation_results.csv');
    };

    return (
        <ResultContainer className="fade-in">
            <TableHeader>
                <TableTitle>Translation Results ({results.length} items)</TableTitle>
                <StyledButton variant="secondary" onClick={handleExport}>
                    📥 Export CSV
                </StyledButton>
            </TableHeader>

            <TableWrapper>
                <Table>
                    <TableHead>
                        <tr>
                            <th>#</th>
                            <th>Original Text</th>
                            <th>Translated Text</th>
                            <th>Languages</th>
                        </tr>
                    </TableHead>
                    <TableBody>
                        {results.map((item, index) => (
                            <tr key={index}>
                                <RowNumber>{index + 1}</RowNumber>
                                <td>{item.original || '-'}</td>
                                <td>{item.translated || '-'}</td>
                                <td>
                                    {item.source_lang.toUpperCase()} → {item.target_lang.toUpperCase()}
                                </td>
                            </tr>
                        ))}
                    </TableBody>
                </Table>
            </TableWrapper>

            {results.length === 0 && (
                <EmptyState>No results to display</EmptyState>
            )}
        </ResultContainer>
    );
};
