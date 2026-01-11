#!/bin/bash
# Stop Script for MFEGSN PDF RAG System Docker containers

echo "=== Stopping MFEGSN Docker Containers ==="
echo ""

# Check if Docker Compose is available
if docker compose version &> /dev/null; then
    echo "Stopping containers..."
    docker compose down
elif command -v docker-compose &> /dev/null; then
    echo "Stopping containers..."
    docker-compose down
else
    echo "❌ Error: Docker Compose not found"
    exit 1
fi

echo ""
echo "✓ Containers stopped successfully"
echo ""
echo "To start again, run: ./start.sh"
echo ""
