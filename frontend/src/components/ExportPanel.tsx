import { useState } from 'react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface ExportPanelProps {
    copyData: Record<string, string>;
    productName: string;
    platforms: string[];
    hashtags?: string[];
}

export default function ExportPanel({ copyData, productName, platforms, hashtags }: ExportPanelProps) {
    const [isExporting, setIsExporting] = useState(false);
    const [exportStatus, setExportStatus] = useState<string>('');

    const downloadZIP = async () => {
        setIsExporting(true);
        setExportStatus('Generando paquete ZIP...');

        try {
            const response = await axios.post(
                `${API_BASE_URL}/api/export/zip`,
                {
                    copy_data: copyData,
                    product_name: productName,
                    platforms: platforms,
                    include_hashtags: true,
                    hashtags: hashtags || []
                },
                {
                    responseType: 'blob'
                }
            );

            // Crear enlace de descarga
            const url = window.URL.createObjectURL(new Blob([response.data]));
            const link = document.createElement('a');
            link.href = url;
            link.setAttribute('download', `${productName.replace(/\s+/g, '_')}_mango_export.zip`);
            document.body.appendChild(link);
            link.click();
            link.remove();

            setExportStatus('¡ZIP descargado exitosamente!');
            setTimeout(() => setExportStatus(''), 3000);
        } catch (error) {
            console.error('Error downloading ZIP:', error);
            setExportStatus('Error al descargar ZIP');
            setTimeout(() => setExportStatus(''), 3000);
        } finally {
            setIsExporting(false);
        }
    };

    const copyAllToClipboard = () => {
        const allCopy = Object.entries(copyData)
            .map(([platform, copy]) => `=== ${platform.toUpperCase()} ===\n\n${copy}\n`)
            .join('\n---\n\n');

        navigator.clipboard.writeText(allCopy);
        setExportStatus('¡Todo copiado al portapapeles!');
        setTimeout(() => setExportStatus(''), 3000);
    };

    const copySinglePlatform = (platform: string) => {
        const copy = copyData[platform];
        if (!copy) return;

        navigator.clipboard.writeText(copy);
        setExportStatus(`¡${platform} copiado!`);
        setTimeout(() => setExportStatus(''), 2000);
    };

    const getShareURL = async (platform: string) => {
        try {
            const copy = copyData[platform];
            if (!copy) return;

            const response = await axios.post(`${API_BASE_URL}/api/export/share-urls`, null, {
                params: {
                    platform,
                    copy_text: copy
                }
            });

            const url = response.data.urls[platform];
            if (url) {
                window.open(url, '_blank');
            }
        } catch (error) {
            console.error('Error generating share URL:', error);
        }
    };

    if (Object.keys(copyData).length === 0) {
        return (
            <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-xl p-8 text-center">
                <div className="text-4xl mb-2">📦</div>
                <p className="text-gray-600 font-semibold mb-1">
                    Panel de exportación
                </p>
                <p className="text-gray-500 text-sm">
                    Genera contenido primero para exportar
                </p>
            </div>
        );
    }

    return (
        <div className="bg-white rounded-xl shadow-lg p-6 space-y-6">
            {/* Header */}
            <div className="flex items-center justify-between">
                <h2 className="text-2xl font-bold text-gray-800">📦 Exportar</h2>
                {exportStatus && (
                    <div className="px-3 py-1 bg-green-100 text-green-700 rounded-lg text-sm font-semibold animate-pulse">
                        {exportStatus}
                    </div>
                )}
            </div>

            {/* Main Actions */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <button
                    onClick={downloadZIP}
                    disabled={isExporting}
                    className="px-6 py-4 bg-gradient-to-r from-mango-600 to-orange-600 text-white rounded-xl font-bold text-lg hover:from-mango-700 hover:to-orange-700 transition-all disabled:opacity-50 disabled:cursor-not-allowed shadow-lg hover:shadow-xl"
                >
                    {isExporting ? (
                        <>⏳ Generando...</>
                    ) : (
                        <>📥 Descargar ZIP Completo</>
                    )}
                </button>

                <button
                    onClick={copyAllToClipboard}
                    className="px-6 py-4 bg-gray-800 text-white rounded-xl font-bold text-lg hover:bg-gray-900 transition-all shadow-lg hover:shadow-xl"
                >
                    📋 Copiar Todo
                </button>
            </div>

            {/* Per Platform Actions */}
            <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-3">
                    Copiar por plataforma:
                </h3>
                <div className="grid grid-cols-2 gap-3">
                    {Object.keys(copyData).map((platform) => (
                        <button
                            key={platform}
                            onClick={() => copySinglePlatform(platform)}
                            className="px-4 py-3 bg-mango-50 border-2 border-mango-200 text-mango-700 rounded-lg font-semibold hover:bg-mango-100 hover:border-mango-300 transition-all text-sm"
                        >
                            {getPlatformEmoji(platform)} {platform}
                        </button>
                    ))}
                </div>
            </div>

            {/* Share Links */}
            <div>
                <h3 className="text-lg font-semibold text-gray-800 mb-3">
                    Compartir directo:
                </h3>
                <div className="grid grid-cols-2 gap-3">
                    {platforms.filter(p => ['facebook', 'whatsapp', 'linkedin'].includes(p)).map((platform) => (
                        <button
                            key={platform}
                            onClick={() => getShareURL(platform)}
                            className="px-4 py-3 bg-blue-50 border-2 border-blue-200 text-blue-700 rounded-lg font-semibold hover:bg-blue-100 hover:border-blue-300 transition-all text-sm"
                        >
                            🔗 Abrir {platform}
                        </button>
                    ))}
                </div>
            </div>

            {/* Info */}
            <div className="bg-mango-50 border-l-4 border-mango-500 p-4 rounded-lg">
                <p className="text-sm text-gray-700">
                    <span className="font-semibold">💡 Tip:</span> El ZIP incluye todos los textos organizados por plataforma, imágenes optimizadas y un README con instrucciones.
                </p>
            </div>
        </div>
    );
}

function getPlatformEmoji(platform: string): string {
    const emojis: Record<string, string> = {
        facebook: '📘',
        instagram: '📸',
        tiktok: '🎵',
        linkedin: '💼',
        whatsapp: '💬'
    };
    return emojis[platform] || '📱';
}
