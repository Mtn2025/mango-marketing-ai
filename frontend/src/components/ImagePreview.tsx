import { useState } from 'react';

interface GeneratedImage {
    url: string;
    platform: string;
    format: string;
    size: string;
}

interface ImagePreviewProps {
    images: GeneratedImage[];
    onDownload?: (image: GeneratedImage) => void;
    onRegenerate?: (image: GeneratedImage) => void;
}

export default function ImagePreview({ images, onDownload, onRegenerate }: ImagePreviewProps) {
    const [selectedImage, setSelectedImage] = useState<GeneratedImage | null>(null);

    if (images.length === 0) {
        return (
            <div className="bg-gray-50 border-2 border-dashed border-gray-300 rounded-xl p-12 text-center">
                <div className="text-6xl mb-4">🖼️</div>
                <p className="text-gray-600 font-semibold mb-2">
                    No hay imágenes generadas aún
                </p>
                <p className="text-gray-500 text-sm">
                    Las imágenes aparecerán aquí después de generarlas
                </p>
            </div>
        );
    }

    return (
        <div className="space-y-4">
            {/* Image Grid */}
            <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                {images.map((img, index) => (
                    <div
                        key={index}
                        className="group relative bg-white border-2 border-gray-200 rounded-xl overflow-hidden hover:border-mango-400 transition-all cursor-pointer"
                        onClick={() => setSelectedImage(img)}
                    >
                        {/* Image */}
                        <div className="aspect-square bg-gray-100">
                            <img
                                src={img.url}
                                alt={`${img.platform} - ${img.format}`}
                                className="w-full h-full object-cover"
                            />
                        </div>

                        {/* Overlay on hover */}
                        <div className="absolute inset-0 bg-black bg-opacity-0 group-hover:bg-opacity-50 transition-all flex items-center justify-center opacity-0 group-hover:opacity-100">
                            <div className="text-white text-center">
                                <div className="text-2xl mb-2">🔍</div>
                                <p className="text-sm font-semibold">Ver detalles</p>
                            </div>
                        </div>

                        {/* Info Badge */}
                        <div className="absolute top-2 left-2 bg-black bg-opacity-75 text-white px-2 py-1 rounded-lg text-xs font-semibold">
                            {img.platform}
                        </div>

                        {/* Size Badge */}
                        <div className="absolute top-2 right-2 bg-mango-600 text-white px-2 py-1 rounded-lg text-xs font-semibold">
                            {img.size}
                        </div>
                    </div>
                ))}
            </div>

            {/* Stats */}
            <div className="flex items-center justify-between bg-gray-50 rounded-lg p-4">
                <div className="text-sm text-gray-600">
                    <span className="font-semibold text-gray-800">{images.length}</span> imagen(es) generada(s)
                </div>
                <button className="px-4 py-2 bg-mango-600 text-white rounded-lg font-semibold hover:bg-mango-700 transition-colors text-sm">
                    📥 Descargar todas
                </button>
            </div>

            {/* Modal for selected image */}
            {selectedImage && (
                <div
                    className="fixed inset-0 bg-black bg-opacity-75 z-50 flex items-center justify-center p-4"
                    onClick={() => setSelectedImage(null)}
                >
                    <div
                        className="bg-white rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-auto"
                        onClick={(e) => e.stopPropagation()}
                    >
                        {/* Header */}
                        <div className="flex items-center justify-between p-6 border-b border-gray-200">
                            <div>
                                <h3 className="text-xl font-bold text-gray-800">
                                    {selectedImage.platform} - {selectedImage.format}
                                </h3>
                                <p className="text-sm text-gray-600">{selectedImage.size}</p>
                            </div>
                            <button
                                onClick={() => setSelectedImage(null)}
                                className="text-gray-500 hover:text-gray-700 text-2xl"
                            >
                                ×
                            </button>
                        </div>

                        {/* Image */}
                        <div className="p-6">
                            <img
                                src={selectedImage.url}
                                alt={`${selectedImage.platform} - ${selectedImage.format}`}
                                className="w-full rounded-lg"
                            />
                        </div>

                        {/* Actions */}
                        <div className="flex gap-3 p-6 border-t border-gray-200">
                            <button
                                onClick={() => onDownload?.(selectedImage)}
                                className="flex-1 px-4 py-3 bg-mango-600 text-white rounded-lg font-semibold hover:bg-mango-700 transition-colors"
                            >
                                📥 Descargar
                            </button>
                            <button
                                onClick={() => onRegenerate?.(selectedImage)}
                                className="flex-1 px-4 py-3 bg-gray-200 text-gray-800 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
                            >
                                🔄 Regenerar
                            </button>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
