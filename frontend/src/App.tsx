import { useState } from 'react';
import ConfigPanel from './components/ConfigPanel';
import ProductForm from './components/ProductForm';
import CopyGenerator from './components/CopyGenerator';
import HistoryPanel from './components/HistoryPanel';
import TipsPanel from './components/TipsPanel';

type Tab = 'generator' | 'history';

function App() {
    const [activeTab, setActiveTab] = useState<Tab>('generator');

    return (
        <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-mango-50">
            {/* Header */}
            <header className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
                <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8">
                    <div className="flex items-center justify-between">
                        <div className="flex items-center gap-3">
                            <span className="text-4xl">🥭</span>
                            <div>
                                <h1 className="text-2xl font-bold text-gray-900">
                                    Mango Marketing AI
                                </h1>
                                <p className="text-sm text-gray-600">
                                    Generador de contenido con IA
                                </p>
                            </div>
                        </div>
                        <div className="flex items-center gap-3">
                            <a
                                href="https://creator.ubrokers.mx/docs"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="px-3 py-1 bg-gray-100 text-gray-700 rounded-lg text-sm font-semibold hover:bg-gray-200 transition-colors"
                            >
                                📚 API Docs
                            </a>
                            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
                                ✓ Online
                            </span>
                        </div>
                    </div>

                    {/* Tabs */}
                    <div className="mt-4 flex gap-2 border-b border-gray-200">
                        <button
                            onClick={() => setActiveTab('generator')}
                            className={`px-4 py-2 font-semibold transition-colors border-b-2 ${activeTab === 'generator'
                                    ? 'border-mango-500 text-mango-600'
                                    : 'border-transparent text-gray-600 hover:text-gray-800'
                                }`}
                        >
                            ✨ Generador
                        </button>
                        <button
                            onClick={() => setActiveTab('history')}
                            className={`px-4 py-2 font-semibold transition-colors border-b-2 ${activeTab === 'history'
                                    ? 'border-mango-500 text-mango-600'
                                    : 'border-transparent text-gray-600 hover:text-gray-800'
                                }`}
                        >
                            📜 Historial
                        </button>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
                {activeTab === 'generator' ? (
                    <div className="space-y-6">
                        {/* Tips Panel */}
                        <TipsPanel />

                        {/* Generator Grid */}
                        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                            {/* Left Column */}
                            <div className="space-y-6">
                                <ConfigPanel />
                                <ProductForm />
                            </div>

                            {/* Right Column */}
                            <div className="lg:sticky lg:top-24 h-fit">
                                <CopyGenerator />
                            </div>
                        </div>
                    </div>
                ) : (
                    /* History View */
                    <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                        <div className="lg:col-span-2">
                            <div className="bg-white rounded-xl shadow-lg p-6">
                                <h2 className="text-2xl font-bold text-gray-800 mb-4">
                                    📊 Análisis de Generaciones
                                </h2>
                                <div className="grid grid-cols-3 gap-4 mb-6">
                                    <div className="text-center p-4 bg-gradient-to-br from-mango-50 to-orange-50 rounded-lg">
                                        <div className="text-3xl font-bold text-mango-600">0</div>
                                        <div className="text-sm text-gray-600 mt-1">Total</div>
                                    </div>
                                    <div className="text-center p-4 bg-gradient-to-br from-blue-50 to-cyan-50 rounded-lg">
                                        <div className="text-3xl font-bold text-blue-600">0</div>
                                        <div className="text-sm text-gray-600 mt-1">Hoy</div>
                                    </div>
                                    <div className="text-center p-4 bg-gradient-to-br from-green-50 to-emerald-50 rounded-lg">
                                        <div className="text-3xl font-bold text-green-600">0</div>
                                        <div className="text-sm text-gray-600 mt-1">Esta semana</div>
                                    </div>
                                </div>
                                <p className="text-gray-600 text-center">
                                    Comienza a generar contenido para ver tus estadísticas 📈
                                </p>
                            </div>
                        </div>
                        <div>
                            <HistoryPanel />
                        </div>
                    </div>
                )}
            </main>

            {/* Footer */}
            <footer className="mt-12 py-6 border-t border-gray-200 bg-white">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center text-gray-500 text-sm">
                        <p className="mb-2">
                            Powered by{' '}
                            <a
                                href="https://groq.com"
                                target="_blank"
                                rel="noopener noreferrer"
                                className="text-mango-600 hover:underline font-semibold"
                            >
                                Groq
                            </a>
                            {' '}(Llama 4 Scout) • Alta velocidad • Bajo costo
                        </p>
                        <p className="text-xs text-gray-400">
                            v1.0.0 • Backend 100% • Frontend MVP
                        </p>
                    </div>
                </div>
            </footer>
        </div>
    );
}

export default App;
