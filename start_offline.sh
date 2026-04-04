#!/bin/bash
# Start SecureCodeAI with Ollama (Offline Mode)
# Port: 8001

cd "$(dirname "$0")"
source venv/bin/activate

export LLM_MODE=ollama
export PORT=8001
export OLLAMA_MODEL=qwen2.5-coder:7b

echo "🔒 Starting SecureCodeAI - OFFLINE MODE (Ollama)"
echo "📍 URL: http://localhost:8001"
echo "🤖 Model: qwen2.5-coder:7b"
echo ""

python -m backend.app
