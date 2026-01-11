#!/bin/bash
# Quick Start Script for MFEGSN PDF RAG System with Docker
# This script launches the application using Docker with data persistence

set -e

echo "=== MFEGSN PDF RAG System - Docker Quick Start ==="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker is not installed"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi
echo "✓ Docker is installed"

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Error: Docker Compose is not installed"
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi
echo "✓ Docker Compose is installed"

# Check if Docker daemon is running
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker daemon is not running"
    echo "Please start Docker and try again"
    exit 1
fi
echo "✓ Docker daemon is running"

# Create necessary directories for data persistence
echo ""
echo "Creating data directories..."
mkdir -p pdfs markdown_outputs chroma_db
echo "✓ Directories created (pdfs, markdown_outputs, chroma_db)"

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "✓ .env file created"
    else
        echo "⚠ Warning: .env.example not found, creating default .env"
        cat > .env << EOF
# Environment Configuration
PDF_DIR=pdfs
MARKDOWN_OUTPUT_DIR=markdown_outputs
CHROMA_DB_DIR=./chroma_db
WEB_PORT=8000
EOF
        echo "✓ Default .env file created"
    fi
fi

# Stop any existing containers
echo ""
echo "Stopping existing containers (if any)..."
docker-compose down 2>/dev/null || docker compose down 2>/dev/null || true

# Build and start containers
echo ""
echo "Building and starting Docker containers..."
echo "This may take a few minutes on the first run..."
echo ""

# Try docker compose first (newer syntax), fallback to docker-compose
if docker compose version &> /dev/null; then
    docker compose up -d --build
else
    docker-compose up -d --build
fi

# Wait for services to be ready
echo ""
echo "Waiting for services to start..."
sleep 5

# Check if containers are running
if docker-compose ps 2>/dev/null | grep -q "Up" || docker compose ps 2>/dev/null | grep -q "running"; then
    echo "✓ Containers are running"
else
    echo "⚠ Warning: Containers may not have started correctly"
    echo "Run 'docker-compose logs' or 'docker compose logs' to check the logs"
fi

echo ""
echo "=== 🎉 Setup Complete! ==="
echo ""
echo "📊 Services are now running with data persistence:"
echo ""
echo "  🌐 Web Interface:"
echo "     → http://localhost:8000"
echo "     → Upload PDFs, search documents, view statistics"
echo ""
echo "  🔧 MCP Server:"
echo "     → Running in the background"
echo "     → Use with VSCode Copilot or Roo Code"
echo ""
echo "📁 Data Persistence (bind mounts):"
echo "  • ./pdfs           → /app/pdfs           (PDF files)"
echo "  • ./markdown_outputs → /app/markdown_outputs (Markdown files)"
echo "  • ./chroma_db      → /app/chroma_db      (Vector database)"
echo ""
echo "💾 All data is saved in your repository!"
echo "   You can commit and push changes with: git add . && git commit -m 'Update data' && git push"
echo ""
echo "📝 Useful commands:"
echo "  • View logs:          docker-compose logs -f"
echo "  • Stop services:      docker-compose down"
echo "  • Restart services:   docker-compose restart"
echo "  • Rebuild containers: docker-compose up -d --build"
echo ""
echo "🔍 To check container status:"
echo "  docker-compose ps"
echo ""
