import { useState } from 'react';
import { useShare } from '../hooks/useShare';

interface ShareButtonsProps {
    copyData: Record<string, string>; // {platform: copyText}
    productName: string;
    productUrl?: string;
    imageUrl?: string;
}

export default function ShareButtons({ copyData, productName, productUrl, imageUrl }: ShareButtonsProps) {
    const { shareNative, getShareUrls, shareViaPopup, copyToClipboard, supportsNativeShare } = useShare();
    const [copiedPlatform, setCopiedPlatform] = useState<string | null>(null);
    const [showInstructions, setShowInstructions] = useState(false);

    const handleNativeShare = async (platform: string) => {
        const copy = copyData[platform];
        if (!copy) return;

        // Intentar Web Share API primero
        const success = await shareNative({
            title: `${productName} - ${platform}`,
            text: copy,
            url: productUrl
        });

        if (!success) {
            // Fallback a URL específica
            handlePlatformShare(platform);
        }
    };

    const handlePlatformShare = (platform: string) => {
        const copy = copyData[platform];
        if (!copy) return;

        const urls = getShareUrls({
            title: productName,
            text: copy,
            url: productUrl,
            imageUrl
        });

        const url = urls[platform as keyof typeof urls];
        if (url) {
            shareViaPopup(url, platform);
        }
    };

    const handleCopyAndOpen = async (platform: string) => {
        const copy = copyData[platform];
        if (!copy) return;

        // 1. Copiar al portapapeles
        const copied = await copyToClipboard(copy);

        if (copied) {
            setCopiedPlatform(platform);
            setTimeout(() => setCopiedPlatform(null), 3000);

            // 2. Mostrar instrucciones
            setShowInstructions(true);
        }
    };

    const getPlatformIcon = (platform: string) => {
        const icons: Record<string, string> = {
            facebook: '📘',
            instagram: '📸',
            tiktok: '🎵',
            linkedin: '💼',
            whatsapp: '💬',
            twitter: '🐦'
        };
        return icons[platform] || '📱';
    };

    const getPlatformColor = (platform: string) => {
        const colors: Record<string, string> = {
            facebook: 'bg-blue-600 hover:bg-blue-700',
            instagram: 'bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700',
            tiktok: 'bg-black hover:bg-gray-900',
            linkedin: 'bg-blue-700 hover:bg-blue-800',
            whatsapp: 'bg-green-600 hover:bg-green-700',
            twitter: 'bg-sky-500 hover:bg-sky-600'
        };
        return colors[platform] || 'bg-gray-600 hover:bg-gray-700';
    };

    return (
        <div className="space-y-6">
            {/* Native Share (Si disponible) */}
            {supportsNativeShare && (
                <div className="bg-gradient-to-r from-mango-50 to-orange-50 border-2 border-mango-300 rounded-xl p-4">
                    <div className="flex items-center gap-3 mb-3">
                        <span className="text-2xl">✨</span>
                        <div>
                            <div className="font-bold text-gray-800">Compartir Rápido</div>
                            <div className="text-sm text-gray-600">Usa el botón nativo de tu dispositivo</div>
                        </div>
                    </div>

                    <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                        {Object.keys(copyData).map((platform) => (
                            <button
                                key={platform}
                                onClick={() => handleNativeShare(platform)}
                                className="px-4 py-3 bg-white border-2 border-mango-400 text-gray-800 rounded-lg font-semibold hover:bg-mango-50 transition-all"
                            >
                                {getPlatformIcon(platform)} {platform}
                            </button>
                        ))}
                    </div>
                </div>
            )}

            {/* Compartir por Plataforma */}
            <div>
                <h3 className="text-lg font-bold text-gray-800 mb-4">
                    🚀 Compartir Directamente
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {Object.keys(copyData).map((platform) => (
                        <div key={platform} className="bg-white border-2 border-gray-200 rounded-xl p-4">
                            {/* Info */}
                            <div className="flex items-center gap-2 mb-3">
                                <span className="text-2xl">{getPlatformIcon(platform)}</span>
                                <div>
                                    <div className="font-bold text-gray-800 capitalize">{platform}</div>
                                    <div className="text-xs text-gray-500">
                                        {copyData[platform].substring(0, 50)}...
                                    </div>
                                </div>
                            </div>

                            {/* Botones */}
                            <div className="flex gap-2">
                                {/* Abrir diálogo nativo */}
                                <button
                                    onClick={() => handlePlatformShare(platform)}
                                    className={`flex-1 px-4 py-2 text-white rounded-lg font-semibold transition-all ${getPlatformColor(platform)}`}
                                >
                                    Abrir {platform}
                                </button>

                                {/* Copiar + Instrucciones */}
                                <button
                                    onClick={() => handleCopyAndOpen(platform)}
                                    className="px-4 py-2 bg-gray-200 text-gray-800 rounded-lg font-semibold hover:bg-gray-300 transition-all"
                                    title="Copiar texto"
                                >
                                    {copiedPlatform === platform ? '✅' : '📋'}
                                </button>
                            </div>

                            {/* Confirmación copiado */}
                            {copiedPlatform === platform && (
                                <div className="mt-2 text-sm text-green-600 font-semibold animate-pulse">
                                    ✅ Texto copiado! Ahora pégalo en {platform}
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            </div>

            {/* Instrucciones Modal */}
            {showInstructions && (
                <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
                    <div className="bg-white rounded-2xl max-w-md w-full p-6">
                        <div className="flex justify-between items-start mb-4">
                            <div>
                                <h3 className="text-xl font-bold text-gray-800">📱 Cómo Publicar</h3>
                                <p className="text-sm text-gray-600">Texto copiado al portapapeles</p>
                            </div>
                            <button
                                onClick={() => setShowInstructions(false)}
                                className="text-gray-500 hover:text-gray-700 text-2xl"
                            >
                                ×
                            </button>
                        </div>

                        <div className="space-y-4">
                            <div className="bg-mango-50 border-l-4 border-mango-500 p-4 rounded">
                                <p className="text-sm text-gray-700 font-semibold mb-2">Pasos siguientes:</p>
                                <ol className="list-decimal list-inside text-sm text-gray-600 space-y-2">
                                    <li>Abre la app de la red social</li>
                                    <li>Crea un nuevo post</li>
                                    <li>Pega el texto (Ctrl+V o Cmd+V)</li>
                                    <li>Adjunta tu imagen si es necesario</li>
                                    <li>¡Publica!</li>
                                </ol>
                            </div>

                            <button
                                onClick={() => setShowInstructions(false)}
                                className="w-full px-4 py-3 bg-mango-600 text-white rounded-lg font-bold hover:bg-mango-700 transition-all"
                            >
                                Entendido
                            </button>
                        </div>
                    </div>
                </div>
            )}

            {/* Tips */}
            <div className="bg-blue-50 border-l-4 border-blue-500 p-4 rounded-lg">
                <p className="text-sm text-gray-700">
                    <span className="font-semibold">💡 Tip:</span> Los botones "Abrir" funcionan mejor en desktop. En móvil, usa "Compartir Rápido" para acceso directo a tus apps instaladas.
                </p>
            </div>
        </div>
    );
}
