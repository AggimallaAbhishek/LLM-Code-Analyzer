#!/bin/bash
# Start SecureCodeAI with Ollama (Offline Mode)
# Port: 8001

cd "$(dirname "$0")"
source venv/bin/activate

export LLM_MODE=ollama
export PORT=8001

echo "🔒 Starting SecureCodeAI - OFFLINE MODE (Ollama)"
echo "📍 URL: http://localhost:8001"
echo "🤖 Model: llama3.2"
echo ""
echo "⚠️  Make sure Ollama is running: ollama serve"
echo ""

python -m backend.app
