import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

interface ImageFile {
    file: File;
    preview: string;
    type: 'producto' | 'servicio' | 'logo' | null;
}

interface ImageUploaderProps {
    onImagesChange?: (images: ImageFile[]) => void;
    maxImages?: number;
}

export default function ImageUploader({ onImagesChange, maxImages = 5 }: ImageUploaderProps) {
    const [images, setImages] = useState<ImageFile[]>([]);

    const onDrop = useCallback((acceptedFiles: File[]) => {
        const newImages = acceptedFiles.slice(0, maxImages - images.length).map(file => ({
            file,
            preview: URL.createObjectURL(file),
            type: null as 'producto' | 'servicio' | 'logo' | null
        }));

        const updated = [...images, ...newImages];
        setImages(updated);
        onImagesChange?.(updated);
    }, [images, maxImages, onImagesChange]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: {
            'image/*': ['.png', '.jpg', '.jpeg', '.webp']
        },
        maxFiles: maxImages,
        disabled: images.length >= maxImages
    });

    const updateImageType = (index: number, type: 'producto' | 'servicio' | 'logo') => {
        const updated = images.map((img, i) =>
            i === index ? { ...img, type } : img
        );
        setImages(updated);
        onImagesChange?.(updated);
    };

    const removeImage = (index: number) => {
        const updated = images.filter((_, i) => i !== index);
        setImages(updated);
        onImagesChange?.(updated);
    };

    return (
        <div className="space-y-4">
            {/* Dropzone */}
            {images.length < maxImages && (
                <div
                    {...getRootProps()}
                    className={`border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all ${isDragActive
                            ? 'border-mango-500 bg-mango-50'
                            : 'border-gray-300 hover:border-mango-400 hover:bg-gray-50'
                        }`}
                >
                    <input {...getInputProps()} />
                    <div className="text-4xl mb-2">📸</div>
                    {isDragActive ? (
                        <p className="text-mango-600 font-semibold">Suelta las imágenes aquí...</p>
                    ) : (
                        <div>
                            <p className="text-gray-700 font-semibold mb-1">
                                Arrastra imágenes aquí o haz click para seleccionar
                            </p>
                            <p className="text-gray-500 text-sm">
                                PNG, JPG, WEBP • Máximo {maxImages} imágenes • {images.length}/{maxImages} cargadas
                            </p>
                        </div>
                    )}
                </div>
            )}

            {/* Image Grid with Type Selectors */}
            {images.length > 0 && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {images.map((img, index) => (
                        <div key={index} className="bg-white border-2 border-gray-200 rounded-xl p-4">
                            {/* Image Preview */}
                            <div className="relative mb-3">
                                <img
                                    src={img.preview}
                                    alt={`Preview ${index + 1}`}
                                    className="w-full h-48 object-cover rounded-lg"
                                />
                                <button
                                    onClick={() => removeImage(index)}
                                    className="absolute top-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center hover:bg-red-600 transition-colors shadow-lg"
                                >
                                    ×
                                </button>
                            </div>

                            {/* Type Selector - Checkboxes como en el plan */}
                            <div className="space-y-2">
                                <p className="text-sm font-semibold text-gray-700 mb-2">
                                    Tipo de imagen:
                                </p>
                                <div className="flex flex-col gap-2">
                                    <label className="flex items-center gap-2 cursor-pointer">
                                        <input
                                            type="checkbox"
                                            checked={img.type === 'producto'}
                                            onChange={() => updateImageType(index, 'producto')}
                                            className="w-4 h-4 text-mango-600 rounded focus:ring-mango-500"
                                        />
                                        <span className="text-sm text-gray-700">
                                            ☑️ Es foto de producto
                                        </span>
                                    </label>

                                    <label className="flex items-center gap-2 cursor-pointer">
                                        <input
                                            type="checkbox"
                                            checked={img.type === 'servicio'}
                                            onChange={() => updateImageType(index, 'servicio')}
                                            className="w-4 h-4 text-mango-600 rounded focus:ring-mango-500"
                                        />
                                        <span className="text-sm text-gray-700">
                                            ☑️ Es actividad/servicio
                                        </span>
                                    </label>

                                    <label className="flex items-center gap-2 cursor-pointer">
                                        <input
                                            type="checkbox"
                                            checked={img.type === 'logo'}
                                            onChange={() => updateImageType(index, 'logo')}
                                            className="w-4 h-4 text-mango-600 rounded focus:ring-mango-500"
                                        />
                                        <span className="text-sm text-gray-700">
                                            ☑️ Es logo (se colocará en esquina)
                                        </span>
                                    </label>
                                </div>

                                {img.type && (
                                    <div className="mt-2 px-3 py-1 bg-mango-100 text-mango-700 rounded-lg text-xs font-semibold inline-block">
                                        Tipo: {img.type}
                                    </div>
                                )}
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Summary */}
            {images.length > 0 && (
                <div className="text-sm text-gray-600 bg-gray-50 rounded-lg p-3">
                    <span className="font-semibold">{images.length}</span> imagen(es) cargada(s) •{' '}
                    <span className="font-semibold">
                        {images.filter(img => img.type).length}
                    </span>{' '}
                    con tipo asignado
                </div>
            )}
        </div>
    );
}
