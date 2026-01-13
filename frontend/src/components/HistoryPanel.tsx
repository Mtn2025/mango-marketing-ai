import { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

interface Generation {
    id: string;
    product_id: string | null;
    platforms: string[] | null;
    quality_level: string | null;
    created_at: string;
}

export default function HistoryPanel() {
    const [generations, setGenerations] = useState<Generation[]>([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);

    const loadHistory = async () => {
        setLoading(true);
        setError(null);

        try {
            const response = await axios.get(`${API_BASE_URL}/api/history?limit=10`);
            setGenerations(response.data);
        } catch (err: any) {
            setError(err.message || 'Error cargando historial');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        loadHistory();
    }, []);

    const formatDate = (dateString: string) => {
        const date = new Date(dateString);
        return date.toLocaleDateString('es-MX', {
            day: '2-digit',
            month: 'short',
            hour: '2-digit',
            minute: '2-digit',
        });
    };

    const getPlatformEmoji = (platform: string) => {
        const emojis: Record<string, string> = {
            facebook: '📘',
            instagram: '📸',
            tiktok: '🎵',
            linkedin: '💼',
            whatsapp: '💬',
        };
        return emojis[platform] || '📱';
    };

    return (
        <div className="bg-white rounded-xl shadow-lg p-6">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-2xl font-bold text-gray-800">📜 Historial</h2>
                <button
                    onClick={loadHistory}
                    disabled={loading}
                    className="px-3 py-1 bg-mango-100 text-mango-700 rounded-lg text-sm font-semibold hover:bg-mango-200 transition-colors disabled:opacity-50"
                >
                    {loading ? '🔄' : '↻'} Actualizar
                </button>
            </div>

            {error && (
                <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700 text-sm">
                    ⚠️ {error}
                </div>
            )}

            {loading && generations.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                    <div className="animate-spin text-3xl mb-2">⏳</div>
                    <p>Cargando historial...</p>
                </div>
            ) : generations.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                    <div className="text-4xl mb-2">📭</div>
                    <p>No hay generaciones aún</p>
                    <p className="text-sm mt-1">Genera tu primer copy para ver el historial</p>
                </div>
            ) : (
                <div className="space-y-3 max-h-[500px] overflow-y-auto">
                    {generations.map((gen) => (
                        <div
                            key={gen.id}
                            className="p-4 bg-gradient-to-r from-gray-50 to-mango-50 rounded-lg border border-gray-200 hover:border-mango-300 transition-all cursor-pointer"
                        >
                            <div className="flex items-start justify-between">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-2">
                                        {gen.platforms && gen.platforms.map((platform, i) => (
                                            <span key={i} className="text-lg" title={platform}>
                                                {getPlatformEmoji(platform)}
                                            </span>
                                        ))}
                                        {gen.quality_level && (
                                            <span className="px-2 py-1 bg-mango-100 text-mango-700 rounded text-xs font-semibold">
                                                {gen.quality_level}
                                            </span>
                                        )}
                                    </div>
                                    <p className="text-xs text-gray-600">
                                        {formatDate(gen.created_at)}
                                    </p>
                                </div>
                                <button className="px-2 py-1 text-mango-600 hover:text-mango-800 font-semibold text-sm">
                                    Ver →
                                </button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            <div className="mt-4 pt-4 border-t border-gray-200">
                <p className="text-xs text-gray-500 text-center">
                    Mostrando últimas {generations.length} generaciones
                </p>
            </div>
        </div>
    );
}
