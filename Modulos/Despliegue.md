# 🚀 MÓDULO 12: Despliegue

> **Duración estimada:** 3-4 horas | **Nivel:** Intermedio

---

## 1. Opciones de Despliegue

| Plataforma | Coste | Complejidad | Ideal para |
|-----------|-------|-------------|-----------|
| **Docker Local** | $0 | Baja | Desarrollo |
| **Railway** | $5/mes | Media | MVP |
| **Render** | $7/mes | Media | Producción pequeña |
| **Hugging Face** | $0 | Baja | Demos |
| **VPS Linux** | $5-20/mes | Alta | Control total |

---

## 2. Docker Compose Producción

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "7860:7860"
    environment:
      - OLLAMA_HOST=http://ollama:11434
      - PYTHONPATH=/app
    volumes:
      - ./data:/app/data
    depends_on:
      - ollama
    restart: unless-stopped

  ollama:
    image: ollama/ollama
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    restart: unless-stopped

volumes:
  ollama_data:
```

---

## 3. Scripts de Despliegue

```bash
# scripts/deploy.sh
#!/bin/bash

echo "🚀 Desplegando OPEN CAREER COACH..."

# Pull latest
git pull origin main

# Build
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d

# Health check
sleep 10
curl -f http://localhost:7860 || exit 1

echo "✅ Despliegue completado"
```

---

## 4. Ejercicios

### 🟢 Básico
1. Desplegar local con Docker
2. Subir a Hugging Face Spaces

### 🟡 Intermedio
3. Configurar CI/CD con GitHub Actions
4. Implementar health checks y monitoreo

### 🔴 Avanzado
5. Setup con Kubernetes
6. Auto-scaling basado en carga

---

**[⬅️ Módulo 11](11-evaluacion.md) | [➡️ Módulo 13](13-agentes-ia.md)**
```

---

