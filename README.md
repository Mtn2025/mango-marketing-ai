# Mango Marketing AI

Sistema de automatización de marketing con IA para generar copy e imágenes profesionales para redes sociales.

## 🚀 Quick Start

### Con Docker (Recomendado)

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd mango-marketing-ai

# 2. Configurar variables de entorno
cp .env.example .env
# Editar .env con tus API keys

# 3. Iniciar con Docker Compose
docker-compose up -d

# 4. Acceder a la aplicación
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Sin Docker

#### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend
npm install
npm run dev
```

## 📋 Requisitos

- Python 3.11+
- Node.js 18+
- PostgreSQL 15+
- Docker y Docker Compose (opcional pero recomendado)

## 🎯 Características

- **6 modelos de IA**: 4 LLMs + 3 generadores de imágenes
- **12 combinaciones posibles**: De  $0.021 a $0.063 por publicación
- **Modo Simple**: 3 niveles pre-configurados (Rápido, Profesional, Elite)
- **Modo Avanzado**: Selección manual de Cerebro + Artista
- **5 plataformas sociales**: Facebook, Instagram, TikTok, LinkedIn, WhatsApp
- **Procesamiento avanzado**: Variantes, carruseles, fusión de logo, watermarks
- **Soporte multi-idioma**: Español MX e Inglés

## 🏗️ Arquitectura

- **Backend**: FastAPI + PostgreSQL + SQLAlchemy + Alembic
- **Frontend**: React + TypeScript + Vite + TailwindCSS
- **Deployment**: Docker Compose
- **APIs integradas**: Google Gemini, Azure OpenAI, Groq, Replicate

## 📚 Documentación

Ver [`docs/`](docs/) para documentación completa.

## 📄 Licencia

MIT
