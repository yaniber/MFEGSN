#!/bin/bash
# Setup script for MFEGSN PDF RAG System

echo "=== MFEGSN PDF RAG System Setup ==="
echo ""

# Check Python version
echo "Checking Python version..."
python3 --version
if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Create virtual environment
echo ""
echo "Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "✓ Virtual environment created"
else
    echo "✓ Virtual environment already exists"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file
echo ""
if [ ! -f ".env" ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created"
else
    echo "✓ .env file already exists"
fi

# Create necessary directories
echo ""
echo "Ensuring directories exist..."
mkdir -p pdfs markdown_outputs chroma_db
echo "✓ Directories created"

echo ""
echo "=== Setup Complete! ==="
echo ""
echo "To get started:"
echo "1. Activate the virtual environment:"
echo "   source venv/bin/activate"
echo ""
echo "2. Start the web interface:"
echo "   python web_interface.py"
echo ""
echo "3. Or run the example script:"
echo "   python example_usage.py"
echo ""
echo "4. Or start the MCP server:"
echo "   python mcp_server/server.py"
echo ""
