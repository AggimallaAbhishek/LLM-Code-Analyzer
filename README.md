# 🔍 LLM Code Analyser

AI-powered code security analysis tool that combines Large Language Models with static analysis to identify vulnerabilities, attack surfaces, and trust boundaries in source code.

![LLM Code Analyser](https://img.shields.io/badge/version-1.2.0-blue.svg)
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
- **🔐 Google OAuth**: Secure authentication with Google Sign-In
- **🎨 Syntax Highlighting**: Color-coded code with Prism.js
- **📍 Line Highlighting**: Visual indicators for vulnerable lines (severity-based colors)
- **📁 Multi-File Upload**: Analyze entire folders or ZIP archives at once
- **📥 Export Reports**: Download analysis as JSON, Markdown, or PDF
- **📋 Copy Fixed Code**: One-click copy for suggested code fixes
- **💻 Modern UI**: Beautiful React interface with cybersecurity aesthetic

## 🖼️ Screenshots

### Login Page
- Secure Google OAuth authentication
- Beautiful animated UI
- Feature preview

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
- Google OAuth credentials (for authentication)

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

6. **Set up Google OAuth** (see [Authentication Setup](#-authentication-setup))

7. **Run the application**
   
   **Development Mode (Recommended for testing OAuth):**
   ```bash
   ./start_dev.sh
   # Frontend: http://localhost:3000
   # Backend: http://localhost:8000
   ```
   
   **Production - Online Mode (Gemini):**
   ```bash
   ./start_online.sh
   # Access: http://localhost:8000
   ```
   
   **Production - Offline Mode (Ollama):**
   ```bash
   ./start_offline.sh
   # Access: http://localhost:8001
   ```

## 🔐 Authentication Setup

This application uses Google OAuth for secure authentication. All pages require login.

### Setting up Google OAuth

1. **Go to Google Cloud Console**
   - Visit [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Create a new project or select an existing one

2. **Create OAuth 2.0 Credentials**
   - Click "Create Credentials" → "OAuth client ID"
   - Select "Web application"
   - Add Authorized JavaScript origins:
     - `http://localhost:3000` (for development mode)
     - `http://localhost:8000` (for production online mode)
   - Add Authorized redirect URIs:
     - `http://localhost:3000/api/auth/callback` (for development mode)
     - `http://localhost:8000/api/auth/callback` (for production online mode)
     - `http://localhost:8001/api/auth/callback` (for production offline mode)

3. **Configure .env file**
   ```env
   # Google OAuth
   GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=your-client-secret
   SECRET_KEY=YourAlphanumericSecretKeyHere
   FRONTEND_URL=http://localhost:3000
   ```

4. **Generate SECRET_KEY** (alphanumeric only)
   ```bash
   python3 -c "import secrets; import string; chars = string.ascii_letters + string.digits; print(''.join(secrets.choice(chars) for _ in range(48)))"
   ```

### Authentication Flow
1. User visits any page → Redirected to `/login`
2. User clicks "Continue with Google" → Google OAuth flow
3. After successful login → Redirected back with JWT token
4. Token stored securely for API calls
5. User profile shown in navbar with logout option

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
| `GOOGLE_CLIENT_ID` | Google OAuth Client ID | - |
| `GOOGLE_CLIENT_SECRET` | Google OAuth Client Secret | - |
| `SECRET_KEY` | JWT signing key (alphanumeric) | - |
| `FRONTEND_URL` | Frontend URL for OAuth redirect | `http://localhost:3000` |

### Startup Scripts

| Script | Mode | Port | Description |
|--------|------|------|-------------|
| `./start_dev.sh` | Development | 3000 (FE) + 8000 (BE) | Hot-reload, best for OAuth testing |
| `./start_online.sh` | Production (Gemini) | 8000 | Cloud-based AI analysis |
| `./start_offline.sh` | Production (Ollama) | 8001 | Local AI analysis |

All scripts automatically kill existing processes on their ports before starting.

## 📖 API Usage

### Authentication Required

All API endpoints (except `/api/auth/*`) require authentication. Include the JWT token in the Authorization header:

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "code": "query = \"SELECT * FROM users WHERE id = \" + user_id",
    "language": "python"
  }'
```

### Analyze Code

```bash
curl -X POST http://localhost:8000/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "query = \"SELECT * FROM users WHERE id = \" + user_id",
    "language": "python"
  }'
```

### Analyze Multiple Files

```bash
curl -X POST http://localhost:8000/api/analyze-multiple \
  -H "Content-Type: application/json" \
  -d '{
    "files": [
      {"filename": "main.py", "content": "import os\nos.system(cmd)", "language": "python"},
      {"filename": "utils.py", "content": "eval(user_input)", "language": "python"}
    ]
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
  "attack_surfaces": [...],
  "trust_boundaries": [...],
  "recommendations": [...]
}
```

## 🏗️ Project Structure

```
LLM-Code-Analyzer/
├── backend/
│   ├── app.py                 # FastAPI application with lifespan events
│   ├── config.py              # Configuration settings
│   ├── routes/
│   │   ├── analyze.py         # Analysis API endpoints
│   │   └── auth.py            # Google OAuth authentication
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
│   │   ├── context/
│   │   │   └── AuthContext.jsx    # Authentication state management
│   │   ├── pages/
│   │   │   ├── LoginPage.jsx      # Google OAuth login
│   │   │   ├── LandingPage.jsx    # Hero, features, stats
│   │   │   └── Dashboard.jsx      # Code editor, results, exports
│   │   └── components/
│   │       ├── Navbar.jsx         # Navigation with user profile
│   │       ├── ProtectedRoute.jsx # Route protection
│   │       ├── CodeEditor.jsx     # Syntax highlighted editor
│   │       ├── ResultsPanel.jsx   # Vulnerability display
│   │       ├── FileUpload.jsx     # Multi-file upload
│   │       ├── MultiFileResults.jsx # Multi-file results
│   │       └── GlowButton.jsx     # Animated buttons
│   ├── index.html
│   └── vite.config.js         # Vite config with API proxy
├── data/                      # Sample vulnerable code
├── docs/                      # Documentation
├── start_dev.sh               # Development mode (FE + BE with hot-reload)
├── start_online.sh            # Production with Gemini (port 8000)
├── start_offline.sh           # Production with Ollama (port 8001)
├── requirements.txt           # Python dependencies
├── .gitignore                 # Git ignore rules
└── README.md
```

## 📊 API Endpoints

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/auth/login` | GET | No | Initiate Google OAuth login |
| `/api/auth/callback` | GET | No | OAuth callback handler |
| `/api/auth/me` | GET | Yes | Get current user info |
| `/api/auth/logout` | POST | Yes | Logout user |
| `/api/auth/status` | GET | No | Check auth status |
| `/api/analyze` | POST | Yes | Analyze single code snippet |
| `/api/analyze-multiple` | POST | Yes | Analyze multiple files |
| `/api/health` | GET | No | Check service health |
| `/api/config` | GET | No | Get current configuration |
| `/docs` | GET | No | Interactive OpenAPI documentation |

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

## ✅ Completed Features

- [x] AI-driven vulnerability detection (Gemini/Ollama)
- [x] Static analysis with 20+ patterns
- [x] Google OAuth authentication
- [x] Syntax highlighting (Prism.js)
- [x] Line highlighting for vulnerabilities (severity-based colors)
- [x] Export reports (JSON/Markdown/PDF)
- [x] Multi-file upload (ZIP support)
- [x] Copy fixed code button
- [x] User profile with Google avatar
- [x] Secure logout functionality
- [x] Development mode with hot-reload
- [x] Automatic port cleanup on startup
- [x] Modern lifespan event handling (no deprecation warnings)

## 🚧 Roadmap

- [ ] Analysis history with database storage
- [ ] VS Code extension
- [ ] GitHub integration
- [ ] CI/CD pipeline integration
- [ ] Custom vulnerability rules
- [ ] Team collaboration features
- [ ] Dark/Light theme toggle

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
- Authentication by [Authlib](https://authlib.org/) + Google OAuth
- Syntax highlighting by [Prism.js](https://prismjs.com/)
- PDF export by [html2pdf.js](https://ekoopmans.github.io/html2pdf.js/)
- Animations by [Framer Motion](https://www.framer.com/motion/)

---

<p align="center">
  Built with ❤️ for secure code everywhere
</p>
