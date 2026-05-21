# Multi-stage Docker build for GitHub Bug Detection System

# Stage 1: Backend
FROM python:3.13-slim as backend

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Stage 2: Frontend build
FROM node:18-alpine as frontend-build

WORKDIR /app

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci

# Copy frontend code
COPY frontend/ ./

# Build frontend
RUN npm run build

# Stage 3: Final image
FROM python:3.13-slim

WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from backend stage
COPY --from=backend /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=backend /usr/local/bin /usr/local/bin

# Copy application code
COPY --from=backend /app/backend ./backend
COPY --from=frontend-build /app/dist ./frontend/dist

# Copy configuration files
COPY requirements.txt ./

# Create non-root user
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Expose ports
EXPOSE 8000 3000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command
CMD ["uvicorn", "backend.src.api:app", "--host", "0.0.0.0", "--port", "8000"]
