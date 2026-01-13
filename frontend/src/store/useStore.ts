import { create } from 'zustand';

interface AppState {
    // Configuration
    apiKey: string;
    language: string;
    qualityLevel: string;

    // Product info
    productName: string;
    description: string;
    platform: string;

    // Copy settings
    tone: string;
    length: string;
    useEmojis: boolean;
    cta: string;
    benefits: string[];

    // Generated copy
    generatedCopy: string | null;
    isGenerating: boolean;

    // Actions
    setApiKey: (key: string) => void;
    setLanguage: (lang: string) => void;
    setQualityLevel: (level: string) => void;
    setProductName: (name: string) => void;
    setDescription: (desc: string) => void;
    setPlatform: (platform: string) => void;
    setTone: (tone: string) => void;
    setLength: (length: string) => void;
    setUseEmojis: (use: boolean) => void;
    setCta: (cta: string) => void;
    setBenefits: (benefits: string[]) => void;
    setGeneratedCopy: (copy: string | null) => void;
    setIsGenerating: (generating: boolean) => void;
}

export const useStore = create<AppState>((set) => ({
    // Initial state
    apiKey: '',
    language: 'es-MX',
    qualityLevel: 'rapido',
    productName: '',
    description: '',
    platform: 'instagram',
    tone: 'casual',
    length: 'medio',
    useEmojis: false,
    cta: '',
    benefits: [],
    generatedCopy: null,
    isGenerating: false,

    // Actions
    setApiKey: (key) => set({ apiKey: key }),
    setLanguage: (lang) => set({ language: lang }),
    setQualityLevel: (level) => set({ qualityLevel: level }),
    setProductName: (name) => set({ productName: name }),
    setDescription: (desc) => set({ description: desc }),
    setPlatform: (platform) => set({ platform }),
    setTone: (tone) => set({ tone }),
    setLength: (length) => set({ length }),
    setUseEmojis: (use) => set({ useEmojis: use }),
    setCta: (cta) => set({ cta }),
    setBenefits: (benefits) => set({ benefits }),
    setGeneratedCopy: (copy) => set({ generatedCopy: copy }),
    setIsGenerating: (generating) => set({ isGenerating: generating }),
}));
