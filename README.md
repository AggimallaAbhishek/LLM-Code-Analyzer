# 🔍 LLM Code Analyzer

AI-powered code security analysis tool that combines Large Language Models with static analysis to identify vulnerabilities, attack surfaces, and trust boundaries in source code.

## ✨ Features

- **AI-Driven Analysis**: Uses OpenAI GPT or local Ollama models for intelligent vulnerability detection
- **Static Analysis**: Pattern-based detection for common security issues
- **Multi-Language Support**: Python, JavaScript, Java, C/C++, PHP
- **Interactive UI**: Web-based interface for easy code analysis
- **Structured Output**: JSON results with detailed findings and fix suggestions

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API key (for online mode) or Ollama (for offline mode)

### Installation

1. **Clone the repository**
   ```bash
   cd LLM-Code-Analyzer
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your OPENAI_API_KEY
   ```

5. **Run the server**
   ```bash
   python -m backend.app
   ```

6. **Open the UI**
   Navigate to `http://localhost:8000` in your browser

## 📖 API Usage

### Analyze Code

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "query = \"SELECT * FROM users WHERE id = \" + user_id",
    "language": "python"
  }'
```

### Response Example

```json
{
  "success": true,
  "language": "python",
  "summary": "Critical SQL injection vulnerability detected...",
  "risk_score": 85,
  "vulnerabilities": [
    {
      "type": "SQL Injection",
      "severity": "critical",
      "line_numbers": [1],
      "description": "User input directly concatenated into SQL query",
      "fix_suggestion": "Use parameterized queries",
      "fixed_code": "cursor.execute(\"SELECT * FROM users WHERE id = ?\", (user_id,))"
    }
  ],
  "attack_surfaces": [...],
  "trust_boundaries": [...],
  "recommendations": [...]
}
```

## 🔧 Configuration

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_MODE` | `online` (OpenAI) or `offline` (Ollama) | `online` |
| `OPENAI_API_KEY` | Your OpenAI API key | - |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model to use | `codellama` |

## 🏗️ Project Structure

```
llm-code-analyzer/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── config.py           # Configuration settings
│   ├── routes/
│   │   └── analyze.py      # API endpoints
│   ├── services/
│   │   ├── analyzer.py     # Main analysis orchestration
│   │   ├── llm_service.py  # LLM integration
│   │   └── static_analyzer.py  # Rule-based analysis
│   ├── models/
│   │   └── schemas.py      # Pydantic models
│   └── utils/
│       └── prompt_engine.py # Prompt templates
├── frontend/
│   ├── index.html          # Main UI
│   └── static/
│       ├── css/style.css   # Styles
│       └── js/script.js    # Frontend logic
├── data/
│   └── samples/            # Sample vulnerable code
├── docs/                   # Documentation
├── requirements.txt        # Python dependencies
└── README.md
```

## 🔒 Detected Vulnerabilities

- SQL Injection
- Command Injection
- Cross-Site Scripting (XSS)
- Path Traversal
- Hardcoded Secrets
- Insecure Deserialization
- Dangerous eval()/exec()
- Weak Cryptography
- And more...

## 🌐 Offline Mode (Ollama)

1. Install Ollama: https://ollama.ai
2. Pull a model:
   ```bash
   ollama pull codellama
   ```
3. Set `LLM_MODE=offline` in `.env`
4. Run the server

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze` | POST | Analyze code for vulnerabilities |
| `/api/health` | GET | Check service health |
| `/api/config` | GET | Get current configuration |
| `/docs` | GET | OpenAPI documentation |

## 🧪 Testing

```bash
# Test with sample code
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"code": "eval(user_input)", "language": "python"}'
```

## 🤝 Contributing

Contributions are welcome! Please read the contributing guidelines before submitting PRs.

## 📄 License

MIT License - see LICENSE file for details.

---

Built with ❤️ using FastAPI, OpenAI, and modern web technologies.
