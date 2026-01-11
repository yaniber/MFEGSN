#!/bin/bash
# Quick Start Script for MFEGSN PDF RAG System with Docker
# This script launches the application using Docker with data persistence

set -e

# Function to detect and set Docker Compose command
get_docker_compose_cmd() {
    if docker compose version &> /dev/null; then
        echo "docker compose"
    else
        echo "docker-compose"
    fi
}

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
DOCKER_COMPOSE_CMD=$(get_docker_compose_cmd)
$DOCKER_COMPOSE_CMD down 2>/dev/null || true

# Build and start containers
echo ""
echo "Building and starting Docker containers..."
echo "This may take a few minutes on the first run..."
echo ""

$DOCKER_COMPOSE_CMD up -d --build

# Wait for services to be ready
echo ""
echo "Waiting for services to start..."
sleep 5

# Check if containers are running (using -q for more reliable check)
if [ -n "$($DOCKER_COMPOSE_CMD ps -q)" ]; then
    echo "✓ Containers are running"
else
    echo "⚠ Warning: Containers may not have started correctly"
    echo "Run '$DOCKER_COMPOSE_CMD logs' to check the logs"
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
echo "   To commit data changes (review changes with 'git status' first):"
echo "   git add pdfs markdown_outputs chroma_db"
echo "   git commit -m 'Update data'"
echo "   git push"
echo ""
echo "📝 Useful commands:"
echo "  • View logs:          $DOCKER_COMPOSE_CMD logs -f"
echo "  • Stop services:      $DOCKER_COMPOSE_CMD down"
echo "  • Restart services:   $DOCKER_COMPOSE_CMD restart"
echo "  • Rebuild containers: $DOCKER_COMPOSE_CMD up -d --build"
echo ""
echo "🔍 To check container status:"
echo "  $DOCKER_COMPOSE_CMD ps"
echo ""
