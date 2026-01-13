import { useState } from 'react'

function App() {
    const [count, setCount] = useState(0)

    return (
        <div className="min-h-screen bg-gradient-to-br from-mango-500 to-orange-600 flex items-center justify-center p-4">
            <div className="max-w-4xl w-full bg-white rounded-2xl shadow-2xl p-8">
                <div className="text-center mb-8">
                    <h1 className="text-5xl font-bold text-mango-600 mb-2">
                        🥭 Mango Marketing AI
                    </h1>
                    <p className="text-gray-600 text-lg">
                        Sistema de automatización de marketing con IA
                    </p>
                </div>

                <div className="bg-gradient-to-r from-mango-50 to-orange-50 rounded-xl p-6 mb-6">
                    <h2 className="text-2xl font-semibold text-gray-800 mb-4">
                        🚀 Estado del Proyecto
                    </h2>
                    <ul className="space-y-2 text-gray-700">
                        <li className="flex items-center">
                            <span className="text-green-500 mr-2">✅</span>
                            Estructura del proyecto creada
                        </li>
                        <li className="flex items-center">
                            <span className="text-green-500 mr-2">✅</span>
                            Backend FastAPI configurado
                        </li>
                        <li className="flex items-center">
                            <span className="text-green-500 mr-2">✅</span>
                            Frontend React + Vite + TypeScript
                        </li>
                        <li className="flex items-center">
                            <span className="text-green-500 mr-2">✅</span>
                            Docker Compose listo
                        </li>
                        <li className="flex items-center">
                            <span className="text-yellow-500 mr-2">⏳</span>
                            Próximo: Modelos de base de datos
                        </li>
                    </ul>
                </div>

                <div className="text-center">
                    <button
                        onClick={() => setCount((count) => count + 1)}
                        className="bg-mango-500 hover:bg-mango-600 text-white font-bold py-3 px-8 rounded-lg transition-colors duration-200 shadow-lg hover:shadow-xl"
                    >
                        Clicks: {count}
                    </button>
                    <p className="mt-4 text-gray-500 text-sm">
                        Frontend funcionando correctamente ✨
                    </p>
                </div>

                <div className="mt-8 pt-6 border-t border-gray-200">
                    <h3 className="text-lg font-semibold text-gray-800 mb-2">
                        📊 Modelos Disponibles (Planificados)
                    </h3>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-blue-50 p-4 rounded-lg">
                            <h4 className="font-semibold text-blue-900">Cerebros (Copy)</h4>
                            <ul className="text-sm text-blue-700 mt-2 space-y-1">
                                <li>• Gemini 2.0/2.5 Flash</li>
                                <li>• GPT-5-mini (Azure)</li>
                                <li>• Llama 4 Scout (Groq)</li>
                            </ul>
                        </div>
                        <div className="bg-purple-50 p-4 rounded-lg">
                            <h4 className="font-semibold text-purple-900">Artistas (Imágenes)</h4>
                            <ul className="text-sm text-purple-700 mt-2 space-y-1">
                                <li>• Imagen 3/4 (Google)</li>
                                <li>• Flux-1.1-Pro (Azure)</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    )
}

export default App
