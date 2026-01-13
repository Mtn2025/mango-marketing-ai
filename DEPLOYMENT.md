# Mango Marketing AI - Guía de Deployment

## 🐳 Deployment con Docker Compose

### Requisitos Previos
- Docker 20.10+
- Docker Compose 2.0+
- Git

### Pasos para Deploy

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/tu-usuario/mango-marketing-ai.git
cd mango-marketing-ai
```

#### 2. Configurar Variables de Entorno
```bash
cp .env.example .env
```

Editar `.env` con tus credenciales:
```env
# PostgreSQL
POSTGRES_PASSWORD=tu_password_seguro

# Security (generar con: python -c "import secrets; print(secrets.token_urlsafe(32))")
ENCRYPTION_KEY=tu_clave_de_32_caracteres_aqui

# Google AI (Gemini + Imagen)
GOOGLE_API_KEY=tu_google_api_key

# Azure OpenAI (GPT-5-mini + Flux)
AZURE_OPENAI_ENDPOINT=https://tu-recurso.openai.azure.com/
AZURE_OPENAI_KEY=tu_azure_key

# Groq (Llama 4 Scout)
GROQ_API_KEY=tu_groq_api_key
```

#### 3. Construir e Iniciar Servicios
```bash
# Modo desarrollo
docker-compose up --build

# Modo producción (detached)
docker-compose up -d --build
```

#### 4. Verificar Servicios
```bash
# Ver logs
docker-compose logs -f

# Ver estado
docker-compose ps
```

### Acceder a la Aplicación
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

### Comandos Útiles

```bash
# Detener servicios
docker-compose down

# Detener y eliminar volúmenes (⚠️ elimina base de datos)
docker-compose down -v

# Reconstruir solo un servicio
docker-compose up -d --build backend

# Ver logs de un servicio específico
docker-compose logs -f backend

# Ejecutar comando en contenedor
docker-compose exec backend bash
docker-compose exec postgres psql -U mango_user -d mango_db

# Ejecutar migraciones
docker-compose exec backend alembic upgrade head

# Crear nueva migración
docker-compose exec backend alembic revision --autogenerate -m "descripcion"
```

## 🚀 Deployment en Producción

### Railway
1. Crear cuenta en [railway.app](https://railway.app)
2. Conectar repositorio GitHub
3. Agregar PostgreSQL plugin
4. Configurar variables de entorno
5. Deploy automático en cada push

### Render
1. Crear cuenta en [render.com](https://render.com)
2. Nuevo Web Service → Conectar repo
3. Agregar PostgreSQL database
4. Configurar variables de entorno
5. Deploy

### VPS/Cloud (AWS, DigitalOcean, etc.)
```bash
# En el servidor
git clone <repo>
cd mango-marketing-ai
cp .env.example .env
# Editar .env
docker-compose -f docker-compose.prod.yml up -d
```

## 🔒 Seguridad en Producción

### Variables de Entorno Críticas
- ❌ **NUNCA** commitear `.env` a Git
- ✅ Usar secrets management (GitHub Secrets, Railway Vars, etc.)
- ✅ Rotar API keys regularmente
- ✅ Usar passwords fuertes para PostgreSQL

### HTTPS
- Usar reverse proxy (Nginx, Caddy)
- Certificados SSL con Let's Encrypt
- Configurar CORS apropiadamente

## 📊 Monitoreo

### Logs
```bash
# Ver todos los logs
docker-compose logs -f

# Solo errores
docker-compose logs -f | grep ERROR

# Últimas 100 líneas
docker-compose logs --tail=100
```

### Health Checks
```bash
# Backend health
curl http://localhost:8000/health

# PostgreSQL
docker-compose exec postgres pg_isready -U mango_user
```

## 🔄 Actualización

```bash
# Pull cambios
git pull origin main

# Rebuild y restart
docker-compose down
docker-compose up -d --build

# Ejecutar migraciones nuevas
docker-compose exec backend alembic upgrade head
```

## 🆘 Troubleshooting

### Puerto ya en uso
```bash
# Cambiar puertos en docker-compose.yml
ports:
  - "8001:8000"  # Backend
  - "3001:3000"  # Frontend
```

### Base de datos no conecta
```bash
# Verificar PostgreSQL
docker-compose exec postgres pg_isready

# Ver logs
docker-compose logs postgres

# Recrear volumen
docker-compose down -v
docker-compose up -d
```

### Permisos en volúmenes
```bash
# Dar permisos
sudo chown -R $USER:$USER generated_images/
```

## 📝 Backup

### Base de Datos
```bash
# Backup
docker-compose exec postgres pg_dump -U mango_user mango_db > backup.sql

# Restore
docker-compose exec -T postgres psql -U mango_user mango_db < backup.sql
```

### Imágenes Generadas
```bash
# Copiar del contenedor
docker cp mango_backend:/app/generated_images ./backup/
```
