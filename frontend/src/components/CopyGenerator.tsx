import { useState } from 'react';
import { useStore } from '../store/useStore';
import { generateCopy } from '../services/api';

export default function CopyGenerator() {
    const {
        apiKey,
        language,
        productName,
        description,
        platform,
        tone,
        length,
        useEmojis,
        benefits,
        generatedCopy,
        setGeneratedCopy,
        isGenerating,
        setIsGenerating,
    } = useStore();

    const [error, setError] = useState<string | null>(null);

    const handleGenerate = async () => {
        // Validation
        if (!apiKey) {
            setError('Por favor ingresa tu API key de Groq');
            return;
        }
        if (!productName || !description) {
            setError('Por favor completa el nombre y descripción del producto');
            return;
        }

        setError(null);
        setIsGenerating(true);
        setGeneratedCopy(null);

        try {
            const response = await generateCopy({
                product_name: productName,
                description,
                platform,
                language,
                api_key: apiKey,
                llm_provider: 'groq',
                llm_model: 'llama-4-scout',
                tone,
                length,
                use_emojis: useEmojis,
                benefits: benefits.length > 0 ? benefits : undefined,
            });

            setGeneratedCopy(response.copy_text);
        } catch (err: any) {
            setError(err.response?.data?.detail || err.message || 'Error generando copy');
        } finally {
            setIsGenerating(false);
        }
    };

    const copyToClipboard = () => {
        if (generatedCopy) {
            navigator.clipboard.writeText(generatedCopy);
            alert('¡Copy copiado al portapapeles!');
        }
    };

    return (
        <div className="bg-white rounded-xl shadow-lg p-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">✨ Generador de Copy</h2>

            {/* Generate Button */}
            <button
                onClick={handleGenerate}
                disabled={isGenerating || !apiKey || !productName || !description}
                className="w-full mb-4 px-6 py-3 bg-gradient-to-r from-mango-500 to-orange-600 text-white font-bold rounded-lg shadow-lg hover:shadow-xl transition-all disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {isGenerating ? (
                    <span className="flex items-center justify-center gap-2">
                        <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
                            <circle
                                className="opacity-25"
                                cx="12"
                                cy="12"
                                r="10"
                                stroke="currentColor"
                                strokeWidth="4"
                                fill="none"
                            />
                            <path
                                className="opacity-75"
                                fill="currentColor"
                                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
                            />
                        </svg>
                        Generando...
                    </span>
                ) : (
                    <span>🚀 Generar Copy con IA</span>
                )}
            </button>

            {/* Error */}
            {error && (
                <div className="mb-4 p-4 bg-red-50 border border-red-200 rounded-lg text-red-700">
                    ⚠️ {error}
                </div>
            )}

            {/* Generated Copy */}
            {generatedCopy && (
                <div className="space-y-3">
                    <div className="flex items-center justify-between">
                        <h3 className="font-semibold text-gray-800">📝 Copy Generado:</h3>
                        <button
                            onClick={copyToClipboard}
                            className="px-3 py-1 bg-mango-100 text-mango-700 rounded-lg text-sm font-semibold hover:bg-mango-200 transition-colors"
                        >
                            📋 Copiar
                        </button>
                    </div>
                    <div className="p-4 bg-gradient-to-br from-mango-50 to-orange-50 rounded-lg border border-mango-200">
                        <p className="whitespace-pre-wrap text-gray-800 leading-relaxed">
                            {generatedCopy}
                        </p>
                    </div>
                    <div className="text-xs text-gray-500 text-center">
                        Generado con Llama 4 Scout (Groq) • {language} • {platform}
                    </div>
                </div>
            )}
        </div>
    );
}
