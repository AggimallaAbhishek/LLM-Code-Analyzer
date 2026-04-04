# 🔍 LLM Code Analyser

AI-powered code security analysis tool that combines Large Language Models with static analysis to identify vulnerabilities, attack surfaces, and trust boundaries in source code.

![LLM Code Analyser](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.12+-green.svg)
![License](https://img.shields.io/badge/license-MIT-purple.svg)

## ✨ Features

### Core Analysis
- **🤖 AI-Driven Analysis**: Uses Google Gemini or local Ollama models for intelligent vulnerability detection
- **📊 Static Analysis**: Pattern-based detection for 20+ common security issues
- **🔄 Hybrid Intelligence**: Combines LLM insights with rule-based verification
- **🌐 Multi-Language Support**: Python, JavaScript, Java, C/C++, PHP, Go, Rust
- **🔒 Offline Mode**: Privacy-friendly local analysis with Ollama
- **⚡ Fast Results**: Static analysis fallback when LLM is slow

### Advanced Features
- **🎨 Syntax Highlighting**: Color-coded code with Prism.js
- **📍 Line Highlighting**: Visual indicators for vulnerable lines (severity-based colors)
- **📁 Multi-File Upload**: Analyze entire folders or ZIP archives at once
- **📥 Export Reports**: Download analysis as JSON, Markdown, or PDF
- **📋 Copy Fixed Code**: One-click copy for suggested code fixes
- **💻 Modern UI**: Beautiful React interface with cybersecurity aesthetic

## 🖼️ Screenshots

### Dashboard
- Clean code editor with syntax highlighting and line numbers
- Real-time vulnerability detection
- Risk score visualization
- Expandable vulnerability cards with fix suggestions
- Multi-file upload with drag-and-drop

### Analysis Results
- Attack surfaces identification
- Trust boundary mapping
- Severity-based categorization (Critical/High/Medium/Low)
- One-click access to fixed code
- Export to JSON/Markdown/PDF

## 🚀 Quick Start

### Prerequisites

- Python 3.12+
- Node.js 18+ (for frontend development)
- Google Gemini API key (for online mode) OR Ollama (for offline mode)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/LLM-Code-Analyzer.git
   cd LLM-Code-Analyzer
   ```

2. **Create virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Install frontend dependencies**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

5. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your API keys
   ```

6. **Run the application**
   
   **Online Mode (Gemini):**
   ```bash
   ./start_online.sh
   ```
   
   **Offline Mode (Ollama):**
   ```bash
   ./start_offline.sh
   ```

7. **Open the UI**
   - Online mode: http://localhost:8000
   - Offline mode: http://localhost:8001

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLM_MODE` | `gemini`, `openai`, or `ollama` | `gemini` |
| `GEMINI_API_KEY` | Your Google Gemini API key | - |
| `GEMINI_MODEL` | Gemini model to use | `gemini-2.0-flash` |
| `OPENAI_API_KEY` | Your OpenAI API key | - |
| `OPENAI_MODEL` | OpenAI model to use | `gpt-4o-mini` |
| `OLLAMA_BASE_URL` | Ollama server URL | `http://localhost:11434` |
| `OLLAMA_MODEL` | Ollama model to use | `qwen3-coder:480b-cloud` |
| `PORT` | Server port | `8000` |

### Startup Scripts

| Script | Mode | Port | Model |
|--------|------|------|-------|
| `./start_online.sh` | Gemini (Cloud) | 8000 | gemini-2.0-flash |
| `./start_offline.sh` | Ollama (Local) | 8001 | qwen3-coder:480b-cloud |

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
  "summary": "Critical SQL injection vulnerability detected",
  "risk_score": 85,
  "vulnerabilities": [
    {
      "type": "SQL Injection",
      "severity": "critical",
      "line_numbers": [1],
      "description": "User input directly concatenated into SQL query",
      "vulnerable_code": "query = \"SELECT * FROM users WHERE id = \" + user_id",
      "fix_suggestion": "Use parameterized queries",
      "fixed_code": "cursor.execute(\"SELECT * FROM users WHERE id = ?\", (user_id,))"
    }
  ],
  "attack_surfaces": [
    {
      "name": "User Input",
      "type": "user_input",
      "description": "Direct user input used in database query",
      "risk_level": "high"
    }
  ],
  "trust_boundaries": [
    {
      "name": "Input to Database",
      "description": "Data crosses from untrusted user to trusted database",
      "components": ["user_input", "sql_query"]
    }
  ],
  "recommendations": [
    "Use parameterized queries or prepared statements",
    "Validate and sanitize all user inputs"
  ]
}
```

## 🏗️ Project Structure

```
LLM-Code-Analyzer/
├── backend/
│   ├── app.py                 # FastAPI application
│   ├── config.py              # Configuration settings
│   ├── routes/
│   │   └── analyze.py         # API endpoints
│   ├── services/
│   │   ├── analyzer.py        # Main analysis orchestration
│   │   ├── llm_service.py     # LLM integration (Gemini/OpenAI/Ollama)
│   │   └── static_analyzer.py # Rule-based analysis (20+ patterns)
│   ├── models/
│   │   └── schemas.py         # Pydantic request/response models
│   └── utils/
│       └── prompt_engine.py   # Security analysis prompts
├── frontend/
│   ├── src/
│   │   ├── pages/
│   │   │   ├── LandingPage.jsx   # Hero, features, stats
│   │   │   └── Dashboard.jsx     # Code editor & results
│   │   └── components/
│   │       ├── Navbar.jsx        # Navigation bar
│   │       ├── CodeEditor.jsx    # Code input with line numbers
│   │       ├── ResultsPanel.jsx  # Vulnerability display
│   │       ├── GlowButton.jsx    # Animated buttons
│   │       └── ...
│   ├── index.html
│   └── vite.config.js
├── data/                      # Sample vulnerable code
├── docs/                      # Documentation
├── start_online.sh            # Start with Gemini (port 8000)
├── start_offline.sh           # Start with Ollama (port 8001)
├── requirements.txt           # Python dependencies
└── README.md
```

## 🔒 Detected Vulnerabilities

| Category | Vulnerabilities |
|----------|-----------------|
| **Injection** | SQL Injection, Command Injection, Code Injection, XPath Injection |
| **XSS** | Reflected XSS, Stored XSS, DOM-based XSS |
| **Secrets** | Hardcoded Passwords, API Keys, Tokens, Connection Strings |
| **Crypto** | Weak Hashing (MD5/SHA1), Hardcoded Encryption Keys |
| **Code Execution** | eval(), exec(), pickle.loads(), unsafe deserialization |
| **File Operations** | Path Traversal, Arbitrary File Read/Write |
| **Authentication** | Weak Passwords, Missing Auth Checks |
| **Configuration** | Debug Mode Enabled, Verbose Errors |

## 🌐 Offline Mode (Ollama)

For privacy-sensitive environments, run analysis completely offline:

1. **Install Ollama**: https://ollama.ai

2. **Pull a code-focused model:**
   ```bash
   ollama pull qwen2.5-coder:7b
   # OR for better results (requires cloud):
   ollama pull qwen3-coder:480b-cloud
   ```

3. **Start Ollama server:**
   ```bash
   ollama serve
   ```

4. **Run offline mode:**
   ```bash
   ./start_offline.sh
   ```

## 📊 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/analyze` | POST | Analyze code for vulnerabilities |
| `/api/health` | GET | Check service health and LLM status |
| `/api/config` | GET | Get current configuration |
| `/docs` | GET | Interactive OpenAPI documentation |
| `/redoc` | GET | ReDoc API documentation |

## 🧪 Test Code Sample

Use this code to test the analyzer:

```python
import os
import pickle
import sqlite3
import subprocess
from flask import Flask, request

app = Flask(__name__)

# Hardcoded credentials
API_KEY = "sk-abc123secretkey456"
DB_PASSWORD = "admin123"

def login(username, password):
    conn = sqlite3.connect('users.db')
    query = "SELECT * FROM users WHERE username='" + username + "' AND password='" + password + "'"
    return conn.execute(query).fetchone()

def run_command(user_input):
    os.system("ping " + user_input)

def load_data(data):
    return pickle.loads(data)

def calculate(expr):
    return eval(expr)

@app.route('/search')
def search():
    query = request.args.get('q', '')
    return f"<h1>Results for: {query}</h1>"

if __name__ == '__main__':
    app.run(debug=True)
```

## 🛠️ Development

### Frontend Development
```bash
cd frontend
npm run dev    # Start dev server with hot reload
npm run build  # Build for production
npm run lint   # Run ESLint
```

### Backend Development
```bash
source venv/bin/activate
python -m backend.app  # Start with auto-reload
```

## 🚧 Roadmap

- [ ] Syntax highlighting in code editor
- [ ] Line highlighting for vulnerable code
- [ ] Export reports (PDF/JSON/Markdown)
- [ ] Analysis history with localStorage
- [ ] VS Code extension
- [ ] GitHub integration
- [ ] CI/CD pipeline integration
- [ ] Custom vulnerability rules

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Frontend powered by [React](https://react.dev/) + [Vite](https://vitejs.dev/) + [Tailwind CSS](https://tailwindcss.com/)
- AI powered by [Google Gemini](https://ai.google.dev/) and [Ollama](https://ollama.ai/)
- Animations by [Framer Motion](https://www.framer.com/motion/)

---

<p align="center">
  Built with ❤️ for secure code everywhere
</p>
