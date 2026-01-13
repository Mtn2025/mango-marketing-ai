import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface SaveConfigRequest {
    language?: string;
    quality_level?: string;
    llm_provider?: string;
    llm_model?: string;
    llm_api_key?: string;
    image_provider?: string;
    image_model?: string;
    image_api_key?: string;
}

export interface GenerateCopyRequest {
    product_name: string;
    description: string;
    platform: string;
    language?: string;
    api_key: string;
    llm_provider?: string;
    llm_model?: string;
    tone?: string;
    length?: string;
    use_emojis?: boolean;
    cta?: string;
    benefits?: string[];
    keywords?: string[];
}

export interface CopyResponse {
    copy_text: string;
    metadata: {
        provider: string;
        model: string;
        platform: string;
        language: string;
    };
}

// Save configuration
export const saveConfiguration = async (data: SaveConfigRequest) => {
    const response = await axios.post(`${API_BASE_URL}/api/config`, data);
    return response.data;
};

// Generate copy
export const generateCopy = async (data: GenerateCopyRequest): Promise<CopyResponse> => {
    const response = await axios.post(`${API_BASE_URL}/api/generate/copy`, data);
    return response.data;
};

// Health check
export const healthCheck = async () => {
    const response = await axios.get(`${API_BASE_URL}/health`);
    return response.data;
};
