#!/bin/bash
# Script para ejecutar migraciones de Alembic en producción

echo "🚀 Ejecutando migraciones de Alembic..."

# Ejecutar migraciones en el contenedor de backend
docker exec mango_backend alembic upgrade head

if [ $? -eq 0 ]; then
    echo "✅ Migraciones ejecutadas exitosamente"
else
    echo "❌ Error ejecutando migraciones"
    exit 1
fi
