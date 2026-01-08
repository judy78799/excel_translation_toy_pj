export const exportToCSV = (data, filename = 'translation_results.csv') => {
    if (!data || data.length === 0) {
        return;
    }

    // Create CSV content
    const headers = ['Original', 'Translated', 'Source Language', 'Target Language'];
    const csvRows = [headers.join(',')];

    data.forEach(item => {
        const row = [
            `"${item.original.replace(/"/g, '""')}"`,
            `"${item.translated.replace(/"/g, '""')}"`,
            item.source_lang,
            item.target_lang
        ];
        csvRows.push(row.join(','));
    });

    const csvContent = csvRows.join('\n');

    // Create and trigger download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const link = document.createElement('a');
    const url = URL.createObjectURL(blob);

    link.setAttribute('href', url);
    link.setAttribute('download', filename);
    link.style.visibility = 'hidden';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
};
