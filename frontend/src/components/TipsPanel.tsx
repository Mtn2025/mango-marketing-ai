import { useState } from 'react';

interface TipCardProps {
    icon: string;
    title: string;
    description: string;
}

function TipCard({ icon, title, description }: TipCardProps) {
    return (
        <div className="p-4 bg-gradient-to-br from-mango-50 to-orange-50 rounded-lg border border-mango-200">
            <div className="text-2xl mb-2">{icon}</div>
            <h3 className="font-semibold text-gray-800 mb-1">{title}</h3>
            <p className="text-sm text-gray-600">{description}</p>
        </div>
    );
}

export default function TipsPanel() {
    const [isExpanded, setIsExpanded] = useState(false);

    const tips = [
        {
            icon: '💡',
            title: 'Describe con detalle',
            description: 'Mientras más específico seas en la descripción, mejor será el copy generado.',
        },
        {
            icon: '🎯',
            title: 'Define beneficios claros',
            description: 'Máximo 3 beneficios concretos ayudan a la IA a crear mensajes impactantes.',
        },
        {
            icon: '🌟',
            title: 'Usa emojis estratégicamente',
            description: 'Los emojis captan atención, pero úsalos con moderación para mejor efecto.',
        },
        {
            icon: '📝',
            title: 'Ajusta el tono',
            description: 'Elige el tono correcto según tu audiencia: casual para jóvenes, formal para B2B.',
        },
        {
            icon: '⚡',
            title: 'Prueba diferentes modelos',
            description: 'Rápido para iteración rápida, Elite para contenido premium.',
        },
        {
            icon: '🔄',
            title: 'Regenera si es necesario',
            description: 'No dudes en regenerar varias veces hasta obtener el resultado perfecto.',
        },
    ];

    return (
        <div className="bg-white rounded-xl shadow-lg p-6">
            <button
                onClick={() => setIsExpanded(!isExpanded)}
                className="w-full flex items-center justify-between mb-4"
            >
                <h2 className="text-2xl font-bold text-gray-800">💡 Tips para mejores resultados</h2>
                <span className="text-2xl text-mango-600">
                    {isExpanded ? '−' : '+'}
                </span>
            </button>

            {isExpanded && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                    {tips.map((tip, index) => (
                        <TipCard key={index} {...tip} />
                    ))}
                </div>
            )}

            {!isExpanded && (
                <p className="text-sm text-gray-600">
                    Click para ver consejos que te ayudarán a generar mejor contenido
                </p>
            )}
        </div>
    );
}
