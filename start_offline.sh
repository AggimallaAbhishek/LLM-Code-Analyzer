#!/bin/bash
# Start LLM Code Analyser with Ollama (Offline Mode)
# Port: 8001

cd "$(dirname "$0")"
source venv/bin/activate

export LLM_MODE=ollama
export PORT=8001
export OLLAMA_MODEL=qwen3-coder:480b-cloud

echo "🔒 Starting LLM Code Analyser - OFFLINE MODE (Ollama)"
echo "📍 URL: http://localhost:8001"
echo "🤖 Model: qwen3-coder:480b-cloud"
echo ""

python -m backend.app
