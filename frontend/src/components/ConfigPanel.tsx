import { useStore } from '../store/useStore';

export default function ConfigPanel() {
    const { apiKey, setApiKey, language, setLanguage, qualityLevel, setQualityLevel } = useStore();

    return (
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">⚙️ Configuración</h2>

            <div className="space-y-4">
                {/* API Key */}
                <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                        🔑 Groq API Key
                    </label>
                    <input
                        type="password"
                        value={apiKey}
                        onChange={(e) => setApiKey(e.target.value)}
                        placeholder="gsk_..."
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-mango-500 focus:border-transparent"
                    />
                    <p className="text-xs text-gray-500 mt-1">
                        Obtén tu clave en{' '}
                        <a
                            href="https://console.groq.com/"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="text-mango-600 hover:underline"
                        >
                            console.groq.com
                        </a>
                    </p>
                </div>

                {/* Language */}
                <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                        🌎 Idioma
                    </label>
                    <select
                        value={language}
                        onChange={(e) => setLanguage(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-mango-500 focus:border-transparent"
                    >
                        <option value="es-MX">Español (México)</option>
                        <option value="en">English</option>
                    </select>
                </div>

                {/* Quality Level */}
                <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                        ⚡ Nivel de Calidad
                    </label>
                    <div className="grid grid-cols-3 gap-2">
                        <button
                            onClick={() => setQualityLevel('rapido')}
                            className={`px-4 py-3 rounded-lg font-semibold transition-all ${qualityLevel === 'rapido'
                                    ? 'bg-mango-500 text-white shadow-lg'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            ⚡ Rápido
                        </button>
                        <button
                            onClick={() => setQualityLevel('profesional')}
                            className={`px-4 py-3 rounded-lg font-semibold transition-all ${qualityLevel === 'profesional'
                                    ? 'bg-mango-500 text-white shadow-lg'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            💼 Profesional
                        </button>
                        <button
                            onClick={() => setQualityLevel('elite')}
                            className={`px-4 py-3 rounded-lg font-semibold transition-all ${qualityLevel === 'elite'
                                    ? 'bg-mango-500 text-white shadow-lg'
                                    : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                }`}
                        >
                            🏆 Elite
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}
