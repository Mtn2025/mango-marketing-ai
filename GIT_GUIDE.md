# Guía para Subir a GitHub - Mango Marketing AI

## ⚠️ Git no está instalado

Detecté que Git no está instalado en tu sistema. Sigue estos pasos:

### Opción 1: Instalar Git (Recomendado)

#### Windows
1. Descarga Git desde: https://git-scm.com/download/win
2. Ejecuta el instalador
3. Deja las opciones por defecto
4. Reinicia la terminal/PowerShell
5. Verifica: `git --version`

#### Después de instalar Git:

```bash
# 1. Ir al directorio del proyecto
cd "c:\Users\INAX\Desktop\Mango 2.0"

# 2. Configurar Git (primera vez)
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@gmail.com"

# 3. Inicializar repositorio
git init

# 4. Agregar todos los archivos
git add .

# 5. Hacer commit inicial
git commit -m "chore: setup inicial del proyecto Mango Marketing AI"

# 6. Crear repositorio en GitHub
# Ve a https://github.com/new
# Nombre: mango-marketing-ai
# Descripción: Sistema de automatización de marketing con IA
# Tipo: Private (o Public si quieres)
# NO marques "Add README" ni otros archivos

# 7. Conectar con GitHub (reemplaza TU-USUARIO)
git remote add origin https://github.com/TU-USUARIO/mango-marketing-ai.git

# 8. Subir código
git branch -M main
git push -u origin main
```

### Opción 2: Usar GitHub Desktop (Más fácil)

1. Descarga GitHub Desktop: https://desktop.github.com/
2. Instala y abre GitHub Desktop
3. Inicia sesión con tu cuenta de GitHub
4. Click "Add" → "Add Existing Repository"
5. Selecciona: `c:\Users\INAX\Desktop\Mango 2.0`
6. Haz commit con mensaje: "chore: setup inicial del proyecto"
7. Click "Publish repository"
8. Elige nombre y si será público o privado
9. Click "Publish"

## ✅ Archivos Listos para GitHub

Todos los archivos ya están creados y listos:

```
Mango 2.0/
├── backend/
│   ├── alembic/
│   │   ├── env.py
│   │   └── script.py.mako
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── core/
│   │       ├── __init__.py
│   │       ├── config.py
│   │       └── database.py
│   ├── alembic.ini
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.tsx
│   │   ├── main.tsx
│   │   └── index.css
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   └── Dockerfile
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── SETUP.md
├── DEPLOYMENT.md
├── CONTRIBUTING.md
├── LICENSE
├── CHANGELOG.md
└── GIT_GUIDE.md (este archivo)
```

## 🔒 Importante: Variables de Entorno

⚠️ **NUNCA subas el archivo `.env` a GitHub**

El archivo `.gitignore` ya está configurado para ignorar:
- `.env`
- `node_modules/`
- `__pycache__/`
- `generated_images/`

## 📝 Después del Push

Una vez subido a GitHub, agrega tus API keys como "Secrets":

1. Ve a tu repo en GitHub
2. Settings → Secrets and variables → Actions
3. New repository secret
4. Agrega:
   - `POSTGRES_PASSWORD`
   - `ENCRYPTION_KEY`
   - `GOOGLE_API_KEY`
   - `AZURE_OPENAI_ENDPOINT`
   - `AZURE_OPENAI_KEY`
   - `GROQ_API_KEY`

## 🚀 Deploy Automático (Opcional)

Para deploy automático en Railway/Render:

### Railway
1. Ve a railway.app
2. "New Project" → "Deploy from GitHub repo"
3. Selecciona `mango-marketing-ai`
4. Agrega PostgreSQL plugin
5. Configura variables de entorno desde Secrets
6. Deploy automático en cada push

### Render
Similar a Railway, pero en render.com

## ❓ Si tienes problemas

### Error: "fatal: not a git repository"
```bash
git init
```

### Error: "failed to push"
```bash
git pull origin main --rebase
git push origin main
```

### Error: "Permission denied"
```bash
# Configura SSH o usa HTTPS con token
# https://docs.github.com/es/authentication
```

## 📞 Siguiente Paso

Una vez que instales Git y ejecutes los comandos, avísame y podemos:
1. Verificar que se subió correctamente
2. Configurar deployment
3. Comenzar con el desarrollo de features
