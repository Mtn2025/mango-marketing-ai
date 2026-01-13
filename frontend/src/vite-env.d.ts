/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_API_URL: string
    // Agrega más variables aquí según las necesites
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}
