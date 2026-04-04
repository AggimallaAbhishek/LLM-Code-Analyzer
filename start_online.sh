#!/bin/bash
# Start SecureCodeAI with Gemini (Online Mode)
# Port: 8000

cd "$(dirname "$0")"
source venv/bin/activate

export LLM_MODE=gemini
export PORT=8000

echo "🌐 Starting SecureCodeAI - ONLINE MODE (Gemini)"
echo "📍 URL: http://localhost:8000"
echo "🤖 Model: gemini-2.0-flash"
echo ""

python -m backend.app
