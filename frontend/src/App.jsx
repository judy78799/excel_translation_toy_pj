import React, { useState } from 'react';
import { Upload, FileText, Download, AlertCircle, CheckCircle, Loader } from 'lucide-react';

const LANGUAGES = [
    { code: 'ko', name: '한국어' },
    { code: 'en', name: 'English' },
    { code: 'ja', name: '日本語' },
    { code: 'zh', name: '中文' },
    { code: 'es', name: 'Español' },
    { code: 'fr', name: 'Français' },
];

export default function App() {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [results, setResults] = useState(null);
    const [error, setError] = useState(null);
    const [sourceLang, setSourceLang] = useState('ko');
    const [targetLang, setTargetLang] = useState('en');
    const [columnName, setColumnName] = useState('text');

    const handleFileChange = (e) => {
        const selectedFile = e.target.files[0];
        if (selectedFile) {
            setFile(selectedFile);
            setError(null);
            setResults(null);   //이 모든 지옥의 시작
        }
    };

    const handleUpload = async () => {
        if (!file) {
            setError('파일을 선택해주세요');
            return;
        }

        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append('file', file);

        console.log('📤 업로드 시작:', {
            fileName: file.name,
            fileSize: file.size,
            sourceLang,
            targetLang,
            columnName
        });

        try {
            const apiUrl = `http://localhost:8000/api/v1/upload?source_lang=${sourceLang}&target_lang=${targetLang}&text_column=${columnName}`;
            console.log('🌐 API URL:', apiUrl);

            const response = await fetch(apiUrl, {
                method: 'POST',
                body: formData,
            });

            console.log('📥 응답 상태:', response.status);

            if (!response.ok) {
                const errorData = await response.json();
                console.error('❌ 에러 응답:', errorData);
                throw new Error(errorData.detail || '업로드 실패');
            }

            const data = await response.json();
            console.log('✅ 번역 완료:', data);
            setResults(data);
        } catch (err) {
            console.error('❌ 에러 발생:', err);
            setError(`에러: ${err.message}`);

            if (err.message.includes('Failed to fetch')) {
                setError('백엔드 서버에 연결할 수 없습니다. http://localhost:8000 이 실행 중인지 확인하세요.');
            }
        } finally {
            setLoading(false);
        }
    };

    const downloadCSV = () => {
        if (!results || !results.results || results.results.length === 0) {
            alert('다운로드 할 데이터가 없습니다.');
            return;
        }

        const csvContent = [
            ['원문', '번역문', '소스 언어', '타겟 언어'],
            ...results.results.map(r => [
                r.original,
                r.translated,
                r.source_lang,
                r.target_lang
            ])
        ]
            .map(row => row.map(cell => `"${cell}"`).join(','))
            .join('\n');

        const blob = new Blob(['\ufeff' + csvContent], {
            type: 'text/csv;charset=utf-8;',
        });

        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `translation_results_${Date.now()}.csv`;
        link.click();
    };


    return (
        <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8">
            <div className="max-w-6xl mx-auto">
                <div className="text-center mb-8">
                    <h1 className="text-4xl font-bold text-gray-800 mb-2">
                        📝 엑셀 번역 서비스
                    </h1>
                    <p className="text-gray-600">
                        FastAPI + Pandas + React 18로 만든 번역 토이 프로젝트
                    </p>
                </div>

                <div className="bg-white rounded-lg shadow-lg p-6 mb-6">
                    <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                        <Upload className="w-5 h-5" />
                        파일 업로드
                    </h2>

                    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                소스 언어
                            </label>
                            <select
                                value={sourceLang}
                                onChange={(e) => setSourceLang(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            >
                                {LANGUAGES.map(lang => (
                                    <option key={lang.code} value={lang.code}>{lang.name}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                타겟 언어
                            </label>
                            <select
                                value={targetLang}
                                onChange={(e) => setTargetLang(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            >
                                {LANGUAGES.map(lang => (
                                    <option key={lang.code} value={lang.code}>{lang.name}</option>
                                ))}
                            </select>
                        </div>

                        <div>
                            <label className="block text-sm font-medium text-gray-700 mb-1">
                                텍스트 컬럼명
                            </label>
                            <input
                                type="text"
                                value={columnName}
                                onChange={(e) => setColumnName(e.target.value)}
                                placeholder="text"
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            />
                        </div>
                    </div>

                    <div className="flex items-center gap-4">
                        <label className="flex-1 cursor-pointer">
                            <div className="border-2 border-dashed border-gray-300 rounded-lg p-6 text-center hover:border-indigo-500 transition">
                                <FileText className="w-12 h-12 mx-auto mb-2 text-gray-400" />
                                <p className="text-sm text-gray-600">
                                    {file ? file.name : '엑셀 또는 CSV 파일을 선택하세요'}
                                </p>
                                <input
                                    type="file"
                                    accept=".xlsx,.xls,.csv"
                                    onChange={handleFileChange}
                                    className="hidden"
                                />
                            </div>
                        </label>

                        <button
                            onClick={handleUpload}
                            disabled={!file || loading}
                            className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-400 disabled:cursor-not-allowed transition flex items-center gap-2"
                        >
                            {loading ? (
                                <>
                                    <Loader className="w-5 h-5 animate-spin" />
                                    처리중...
                                </>
                            ) : (
                                <>
                                    <Upload className="w-5 h-5" />
                                    번역 시작
                                </>
                            )}
                        </button>
                    </div>
                </div>

                {error && (
                    <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6 flex items-start gap-3">
                        <AlertCircle className="w-5 h-5 text-red-500 flex-shrink-0 mt-0.5" />
                        <div>
                            <p className="font-medium text-red-800">오류 발생</p>
                            <p className="text-sm text-red-600">{error}</p>
                        </div>
                    </div>
                )}

                {results && (
                    <div className="bg-green-50 border border-green-200 rounded-lg p-4 mb-6 flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <CheckCircle className="w-5 h-5 text-green-500" />
                            <div>
                                <p className="font-medium text-green-800">
                                    번역 완료! 총 {results.total_rows}개 (성공: {results.success_count}, 실패: {results.error_count})
                                </p>
                                <p className="text-sm text-green-600">
                                    처리 시간: {results.processing_time}초
                                </p>
                            </div>
                        </div>
                        <button
                            onClick={downloadCSV}
                            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition flex items-center gap-2"
                        >
                            <Download className="w-4 h-4" />
                            CSV 다운로드
                        </button>
                    </div>
                )}

                {results && results.results && (
                    <div className="bg-white rounded-lg shadow-lg overflow-hidden">
                        <div className="p-4 bg-gray-50 border-b">
                            <h2 className="text-xl font-semibold">번역 결과</h2>
                        </div>
                        <div className="overflow-x-auto max-h-96 overflow-y-auto">
                            <table className="w-full">
                                <thead className="bg-gray-100 sticky top-0">
                                    <tr>
                                        <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700 w-12">
                                            #
                                        </th>
                                        <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">
                                            원문 ({results.results[0]?.source_lang})
                                        </th>
                                        <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">
                                            번역문 ({results.results[0]?.target_lang})
                                        </th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-gray-200">
                                    {results.results.map((item, idx) => (
                                        <tr key={idx} className="hover:bg-gray-50">
                                            <td className="px-4 py-3 text-sm text-gray-500">
                                                {idx + 1}
                                            </td>
                                            <td className="px-4 py-3 text-sm text-gray-800">
                                                {item.original}
                                            </td>
                                            <td className="px-4 py-3 text-sm text-gray-600">
                                                {item.translated}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    </div>
                )}

                {!results && !error && !loading && (
                    <div className="bg-white rounded-lg shadow-lg p-12 text-center">
                        <FileText className="w-16 h-16 mx-auto mb-4 text-gray-300" />
                        <p className="text-gray-500">
                            파일을 업로드하면 번역 결과가 여기에 표시됩니다
                        </p>
                    </div>
                )}
            </div>
        </div>
    );
}