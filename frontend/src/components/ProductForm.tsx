import { useState } from 'react';
import { useStore } from '../store/useStore';

export default function ProductForm() {
    const {
        productName,
        setProductName,
        description,
        setDescription,
        platform,
        setPlatform,
        tone,
        setTone,
        length,
        setLength,
        useEmojis,
        setUseEmojis,
        benefits,
        setBenefits,
    } = useStore();

    const [benefitInput, setBenefitInput] = useState('');

    const addBenefit = () => {
        if (benefitInput.trim() && benefits.length < 3) {
            setBenefits([...benefits, benefitInput.trim()]);
            setBenefitInput('');
        }
    };

    const removeBenefit = (index: number) => {
        setBenefits(benefits.filter((_, i) => i !== index));
    };

    return (
        <div className="bg-white rounded-xl shadow-lg p-6 mb-6">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">📦 Información del Producto</h2>

            <div className="space-y-4">
                {/* Product Name */}
                <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                        Nombre del Producto *
                    </label>
                    <input
                        type="text"
                        value={productName}
                        onChange={(e) => setProductName(e.target.value)}
                        placeholder="Ej: Café Artesanal Oaxaqueño"
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-mango-500 focus:border-transparent"
                    />
                </div>

                {/* Description */}
                <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                        Descripción *
                    </label>
                    <textarea
                        value={description}
                        onChange={(e) => setDescription(e.target.value)}
                        placeholder="Describe tu producto con detalle..."
                        rows={3}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-mango-500 focus:border-transparent"
                    />
                </div>

                {/* Platform */}
                <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                        📱 Plataforma
                    </label>
                    <select
                        value={platform}
                        onChange={(e) => setPlatform(e.target.value)}
                        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-mango-500 focus:border-transparent"
                    >
                        <option value="facebook">Facebook</option>
                        <option value="instagram">Instagram</option>
                        <option value="tiktok">TikTok</option>
                        <option value="linkedin">LinkedIn</option>
                        <option value="whatsapp">WhatsApp</option>
                    </select>
                </div>

                <div className="grid grid-cols-2 gap-4">
                    {/* Tone */}
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                            🎭 Tono
                        </label>
                        <select
                            value={tone}
                            onChange={(e) => setTone(e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-mango-500 focus:border-transparent"
                        >
                            <option value="casual">Casual</option>
                            <option value="formal">Formal</option>
                            <option value="juvenil">Juvenil</option>
                            <option value="profesional">Profesional</option>
                        </select>
                    </div>

                    {/* Length */}
                    <div>
                        <label className="block text-sm font-semibold text-gray-700 mb-2">
                            📏 Longitud
                        </label>
                        <select
                            value={length}
                            onChange={(e) => setLength(e.target.value)}
                            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-mango-500 focus:border-transparent"
                        >
                            <option value="corto">Corto</option>
                            <option value="medio">Medio</option>
                            <option value="largo">Largo</option>
                        </select>
                    </div>
                </div>

                {/* Emojis */}
                <div className="flex items-center">
                    <input
                        type="checkbox"
                        id="emojis"
                        checked={useEmojis}
                        onChange={(e) => setUseEmojis(e.target.checked)}
                        className="w-4 h-4 text-mango-600 rounded focus:ring-mango-500"
                    />
                    <label htmlFor="emojis" className="ml-2 text-sm font-semibold text-gray-700">
                        ✨ Incluir emojis
                    </label>
                </div>

                {/* Benefits */}
                <div>
                    <label className="block text-sm font-semibold text-gray-700 mb-2">
                        💎 Beneficios Clave (máx 3)
                    </label>
                    <div className="flex gap-2 mb-2">
                        <input
                            type="text"
                            value={benefitInput}
                            onChange={(e) => setBenefitInput(e.target.value)}
                            onKeyPress={(e) => e.key === 'Enter' && addBenefit()}
                            placeholder="Ej: 100% orgánico"
                            disabled={benefits.length >= 3}
                            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-mango-500 focus:border-transparent disabled:bg-gray-100"
                        />
                        <button
                            onClick={addBenefit}
                            disabled={benefits.length >= 3 || !benefitInput.trim()}
                            className="px-4 py-2 bg-mango-500 text-white rounded-lg font-semibold hover:bg-mango-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                        >
                            +
                        </button>
                    </div>
                    <div className="flex flex-wrap gap-2">
                        {benefits.map((benefit, i) => (
                            <span
                                key={i}
                                className="inline-flex items-center gap-2 px-3 py-1 bg-mango-100 text-mango-800 rounded-full text-sm"
                            >
                                {benefit}
                                <button
                                    onClick={() => removeBenefit(i)}
                                    className="text-mango-600 hover:text-mango-800 font-bold"
                                >
                                    ×
                                </button>
                            </span>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    );
}
