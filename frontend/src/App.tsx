import ConfigPanel from './components/ConfigPanel'
import ProductForm from './components/ProductForm'
import CopyGenerator from './components/CopyGenerator'

function App() {
    return (
        <div className="min-h-screen bg-gradient-to-br from-orange-50 via-white to-mango-50">
            {/* Header */}
            <header className="bg-white shadow-sm border-b border-gray-200">
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
                        <div className="flex items-center gap-2">
                            <span className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm font-semibold">
                                ✓ Online
                            </span>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 py-8 sm:px-6 lg:px-8">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Left Column */}
                    <div className="space-y-6">
                        <ConfigPanel />
                        <ProductForm />
                    </div>

                    {/* Right Column */}
                    <div className="lg:sticky lg:top-8 h-fit">
                        <CopyGenerator />
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="mt-12 py-6 text-center text-gray-500 text-sm">
                <p>
                    Powered by{' '}
                    <a
                        href="https://groq.com"
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-mango-600 hover:underline font-semibold"
                    >
                        Groq
                    </a>
                    {' '}(Llama 4 Scout)
                </p>
            </footer>
        </div>
    )
}

export default App
