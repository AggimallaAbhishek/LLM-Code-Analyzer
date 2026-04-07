# Project Report

## LLM Code Analyzer

**Project Type:** AI-Powered Secure Code Analysis System  
**Repository:** `LLM-Code-Analyzer`  
**Prepared From:** Project README, repository structure, and current implementation  
**Submission Format:** Faculty Project Report Draft  

### Student Details

- **Student Name:** ____________________
- **Roll Number:** ____________________
- **Department:** ____________________
- **Institution:** ____________________
- **Guide / Faculty Name:** ____________________
- **Academic Year / Semester:** ____________________

## Abstract

LLM Code Analyzer is a security-focused software project designed to analyze source code and identify vulnerabilities using a hybrid approach that combines Large Language Models with rule-based static analysis. The system accepts code snippets or multiple source files, detects common weaknesses such as SQL injection, command injection, hardcoded secrets, insecure deserialization, weak cryptography, and unsafe code execution patterns, and then presents the findings in a user-friendly web interface. The project also includes Google OAuth-based authentication, report export functionality, multi-file analysis, syntax-highlighted code viewing, and deployment modes for both online and offline analysis.

The main goal of the project was to create a practical tool that helps developers, students, and security reviewers detect potential security problems early in the development lifecycle. The final system uses a FastAPI backend, a React + Vite frontend, an LLM integration layer, and a static analysis module. It supports modern security reporting through attack surface mapping, trust boundary identification, vulnerability categorization, and remediation suggestions.

## Keywords

LLM, Static Analysis, Secure Coding, Vulnerability Detection, FastAPI, React, OAuth, Ollama, Gemini, Code Security

## 1. Introduction

Modern software systems often contain security weaknesses caused by unsafe input handling, insecure configuration, or misuse of APIs. Manual review is slow and depends heavily on the reviewer’s experience. Traditional static analyzers are fast and deterministic, but they may miss context-sensitive issues. Large Language Models can reason about code semantics, but they can also be inconsistent if used alone.

This project was developed to solve that gap by combining both approaches. LLM Code Analyzer uses static analysis to detect known vulnerability patterns and an LLM to interpret code context, validate findings, explain risks, and suggest fixes. The result is a practical security analysis workflow that is faster than manual review and more informative than pattern matching alone.

## 2. Problem Statement

The problem addressed by this project is the absence of a simple, interactive, and intelligent tool that can:

1. Analyze code for common security vulnerabilities.
2. Work with both single code snippets and multiple uploaded files.
3. Provide meaningful explanations and remediation guidance.
4. Support both cloud-based and privacy-friendly offline analysis.
5. Present results through a modern interface suitable for demonstration and academic evaluation.

## 3. Objectives

The major objectives of the project were:

1. To build a hybrid code security analyzer using LLM reasoning and static pattern detection.
2. To support multiple programming languages such as Python, JavaScript, Java, C/C++, PHP, Go, and Rust as documented in the project README.
3. To classify vulnerabilities by severity and provide fixed-code suggestions.
4. To identify attack surfaces and trust boundaries in the analyzed code.
5. To implement secure user authentication using Google OAuth.
6. To allow single-file and multi-file analysis through a browser-based UI.
7. To support report export in JSON, Markdown, and PDF formats.
8. To provide both online and offline execution modes for broader usability.

## 4. Scope of the Project

The project scope covers secure source-code analysis at the application level. It focuses on developer-facing review rather than runtime monitoring. The system is intended for educational use, security assessment demonstrations, secure coding support, and early-stage vulnerability identification during development.

The project does not replace full manual penetration testing or advanced enterprise SAST/DAST platforms, but it serves as a strong prototype for intelligent secure-code review.

## 5. Technology Stack

| Layer | Technologies Used |
|------|------|
| Backend | Python 3.12+, FastAPI, Pydantic, Authlib, python-jose, httpx |
| Frontend | React 19, Vite, React Router, Tailwind CSS, Framer Motion |
| Security / Auth | Google OAuth, JWT, session middleware |
| AI / Analysis | LLM service abstraction, Ollama, documented Gemini/OpenAI configuration, static analyzer |
| Reporting | JSON export, Markdown export, PDF export using `html2pdf.js` |
| Developer Tooling | ESLint, Vite build, Python bytecode compilation |

### 5.1 Prerequisites

Based on the README, the project requires:

1. Python 3.12 or above
2. Node.js 18 or above
3. Google Gemini API key for online mode or Ollama for offline mode
4. Google OAuth credentials for authentication

### 5.2 Installation Procedure

The documented installation sequence for the project is:

```bash
git clone <repository-url>
cd LLM-Code-Analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd frontend
npm install
npm run build
cd ..
cp .env.example .env
```

After this, the `.env` file is configured with API keys, OAuth credentials, secret key, and frontend URL.

### 5.3 Operating Modes

The project supports three documented ways to run the application:

1. Development mode using `./start_dev.sh`
2. Online mode using `./start_online.sh`
3. Offline mode using `./start_offline.sh`

This gives the project flexibility for local development, faculty demonstrations, and privacy-friendly offline execution.

## 6. System Architecture

The project follows a modular client-server architecture.

```text
User
  |
  v
React Frontend
  |
  v
FastAPI Backend
  |
  +--> Authentication Module (Google OAuth + JWT + Session)
  |
  +--> Analysis API Layer
         |
         +--> Static Analyzer
         |
         +--> Prompt Engine
         |
         +--> LLM Service
                |
                +--> Online Model Configuration
                +--> Offline Ollama Model
```

### Architectural Highlights

1. The frontend handles login, protected routing, code input, file upload, results rendering, and report export.
2. The backend exposes analysis and authentication APIs.
3. The analyzer service orchestrates static analysis and LLM analysis.
4. The prompt engine standardizes the JSON structure expected from the LLM.
5. The schemas layer enforces consistent request and response contracts.

## 7. Major Modules Implemented

### 7.1 Backend Modules

| Module | Purpose |
|------|------|
| `backend/app.py` | Initializes FastAPI, middleware, API routes, and SPA serving |
| `backend/config.py` | Loads environment variables and application settings |
| `backend/routes/analyze.py` | Provides single-file and multi-file analysis endpoints |
| `backend/routes/auth.py` | Implements Google OAuth login, callback, user session, and logout |
| `backend/services/analyzer.py` | Coordinates static analysis and LLM-driven reasoning |
| `backend/services/llm_service.py` | Handles LLM requests and response parsing |
| `backend/services/static_analyzer.py` | Detects known vulnerability patterns using rules |
| `backend/models/schemas.py` | Defines request/response data models |
| `backend/utils/prompt_engine.py` | Builds the LLM prompt and response format |

### 7.2 Frontend Modules

| Module | Purpose |
|------|------|
| `frontend/src/App.jsx` | Defines application routing |
| `frontend/src/context/AuthContext.jsx` | Manages user authentication state |
| `frontend/src/pages/LoginPage.jsx` | Provides Google login flow UI |
| `frontend/src/pages/LandingPage.jsx` | Displays the main secured landing page |
| `frontend/src/pages/Dashboard.jsx` | Supports code input, analysis, export, and multi-file mode |
| `frontend/src/components/CodeEditor.jsx` | Displays syntax-highlighted code |
| `frontend/src/components/ResultsPanel.jsx` | Shows vulnerabilities, risk score, and recommendations |
| `frontend/src/components/FileUpload.jsx` | Handles multi-file and archive upload |
| `frontend/src/components/MultiFileResults.jsx` | Displays aggregated file-wise analysis |
| `frontend/src/components/ProtectedRoute.jsx` | Restricts routes to authenticated users |

## 8. Development Process From Start to End

This section summarizes the complete development journey in chronological order.

### Phase 1: Requirement Analysis and Planning

At the beginning, the goal was defined clearly: build an intelligent code analyzer that could detect security vulnerabilities and present them in a practical web interface. The README-established feature set included hybrid analysis, multiple model support, secure authentication, multi-file upload, report export, and a modern dashboard.

### Phase 2: Project Setup and Repository Structure

The project was divided into two major parts:

1. A FastAPI backend for API services and analysis logic.
2. A React + Vite frontend for user interaction.

The repository was organized into backend services, routes, models, utilities, frontend pages, frontend components, sample data, and startup scripts. This separation improved maintainability and kept the architecture modular.

### Phase 3: Backend Foundation

The backend was implemented using FastAPI. Core setup included:

1. Application bootstrap and lifespan events.
2. Session middleware for authentication.
3. CORS configuration for frontend communication.
4. API route registration.
5. Static frontend serving when the production build is available.

This phase established the base platform on which all security analysis features were built.

### Phase 4: Static Analysis Engine

A dedicated static analyzer module was developed to detect common vulnerability patterns using rule-based pattern matching. It currently includes patterns for issues such as:

1. SQL injection
2. Command injection
3. Dangerous `eval()` and `exec()`
4. Hardcoded credentials and tokens
5. Insecure deserialization
6. Weak cryptography such as MD5 and SHA1
7. Debug mode exposure
8. Path traversal risks

Language detection logic was also added so the analyzer can infer the likely source language when the user selects automatic mode.

### Phase 5: LLM Integration and Prompt Engineering

After static analysis, the next step was integrating an LLM service layer. The objective of this layer was not only to flag issues, but also to:

1. Understand code context.
2. Validate whether rule-based findings represent real vulnerabilities.
3. Produce structured JSON output.
4. Generate summaries, risk scores, recommendations, and fixed-code examples.

To support this, a prompt engine was implemented that sends the source code and static findings to the model and requires a structured JSON response containing attack surfaces, trust boundaries, vulnerabilities, and recommendations.

### Phase 6: Hybrid Analysis Orchestration

The analyzer service was then designed as the core orchestration layer. Its workflow is:

1. Receive code and metadata.
2. Run static analysis first.
3. Build the LLM prompt using code plus static findings.
4. Call the configured model service.
5. Parse the model response.
6. Merge results into a unified analysis response.
7. Compute or validate an overall risk score.

This hybrid design is the central contribution of the project.

### Phase 7: Authentication and Access Control

Since analysis features were intended to be protected, a full authentication flow was added using Google OAuth. This phase included:

1. Login route generation.
2. OAuth callback handling.
3. User information retrieval from Google.
4. Session storage for authenticated users.
5. JWT access-token generation for API requests.
6. User status and logout APIs.
7. Frontend authentication context and protected routes.

This ensured that the application is not openly exposed and that only authenticated users can access major pages.

### Phase 8: Frontend Interface Development

The frontend was built using React and Vite with a security-themed interface. Development focused on clarity and usability. Major UI work included:

1. Login screen for Google authentication.
2. Landing page highlighting project capabilities.
3. Dashboard for entering or pasting source code.
4. Syntax-highlighted code display.
5. Severity-based line highlighting.
6. Result cards for vulnerabilities and fix suggestions.
7. Risk score presentation.
8. Upload support for multiple files and ZIP-based workflows.

This phase made the project usable for demonstration and end users.

### Phase 9: Report Export and Productivity Features

Once core analysis was working, reporting and usability features were added:

1. Export analysis results as JSON.
2. Export analysis results as Markdown.
3. Export analysis results as PDF.
4. Copy fixed code snippets.
5. Support one-click sample loading for demonstration.

These additions improved the project’s usefulness for submissions, presentations, and security documentation.

### Phase 10: Startup Automation and Execution Modes

To simplify execution, shell scripts were created for different usage scenarios:

1. `start_dev.sh` for frontend + backend development with hot reload.
2. `start_online.sh` for online model execution on port 8000.
3. `start_offline.sh` for offline Ollama execution on port 8001.

These scripts also clean up previously running processes on the required ports before launching the application.

### Phase 11: Documentation and User Guidance

The README was expanded to include:

1. Prerequisites and installation steps
2. Google OAuth setup
3. Environment variable configuration
4. API usage examples
5. Project structure
6. Supported vulnerabilities
7. Offline mode instructions
8. Troubleshooting guidance
9. Sample vulnerable code
10. Development and quality commands

This documentation made the project easier to install, demonstrate, and evaluate.

### Phase 12: Validation and Final Review

The final stage focused on validating that the project can be built and checked successfully. On **April 7, 2026**, the following repository-level checks were run successfully in the current workspace:

1. Frontend lint: `npm run lint`
2. Frontend production build: `npm run build`
3. Backend syntax validation: `python3 -m py_compile backend/*.py backend/routes/*.py backend/services/*.py backend/models/*.py backend/utils/*.py`

The frontend build completed successfully. Vite reported a large chunk warning related to bundled client assets, which is a performance optimization concern rather than a build failure.

## 9. Functional Workflow of the System

The working flow of the final application is as follows:

1. The user opens the application.
2. Unauthenticated users are redirected to the login page.
3. The user signs in through Google OAuth.
4. After login, the user accesses the secured landing page or dashboard.
5. The user either pastes a code snippet or uploads multiple files.
6. The frontend sends the request to the analysis API.
7. The backend validates the request and triggers the analyzer service.
8. Static analysis scans the code for known patterns.
9. The prompt engine constructs the LLM request.
10. The LLM generates structured analysis results.
11. The backend returns vulnerabilities, summaries, trust boundaries, attack surfaces, recommendations, and risk score.
12. The frontend renders the results and allows export or copy operations.

## 10. Security-Oriented Design Decisions

The project was built around secure-coding analysis, so several security-focused decisions were included in the implementation:

1. Google OAuth-based authentication for protected access.
2. JWT token generation for authenticated API usage.
3. Session-based user tracking.
4. Request validation through Pydantic schemas.
5. Maximum code-length restriction for analysis requests.
6. Maximum file-count restriction for batch analysis.
7. Structured risk scoring and severity classification.
8. Static analysis rules aligned with common OWASP-style vulnerability categories such as injection, insecure deserialization, weak cryptography, and secret exposure.

For a production-hardening phase, additional steps such as restrictive CORS, HTTPS-only cookies, and more extensive automated tests would be appropriate.

## 11. Features Achieved

According to the README and current repository implementation, the following major features were completed:

1. Hybrid analysis using LLM reasoning and static analysis.
2. Detection of 20+ common vulnerability patterns.
3. Support for single-file and multi-file analysis.
4. Attack surface and trust boundary reporting.
5. Severity-based vulnerability presentation.
6. Risk score calculation.
7. Google OAuth login and logout.
8. Protected routes and user session handling.
9. Syntax highlighting and vulnerable line highlighting.
10. Export to JSON, Markdown, and PDF.
11. Copy-to-clipboard support for fixed code.
12. Startup scripts for development, online, and offline modes.
13. Offline analysis option using Ollama.
14. Integrated frontend and backend deployment flow.

## 12. Testing and Validation Summary

### 12.1 Validation Done

The project documentation and current repository support the following validation activities:

1. Running the frontend linter.
2. Building the frontend for production.
3. Verifying backend Python files compile successfully.
4. Using provided sample vulnerable code to test detection quality.
5. Exercising authentication, upload, and export workflows manually through the UI.

### 12.2 Current Testing Observation

The repository does **not** currently contain dedicated automated unit test files. Therefore, the present verification level is based on linting, build validation, backend syntax checks, and functional/manual testing flows. For a future academic or production extension, adding unit tests for the analyzer service, auth helpers, and frontend components would strengthen the project significantly.

## 13. Results and Outcome

The project successfully produced a working secure-code analysis platform with the following outcomes:

1. A usable web-based dashboard for vulnerability analysis.
2. A backend that accepts code and returns structured findings.
3. A hybrid analysis pipeline that combines deterministic and AI-driven methods.
4. A reporting system that converts technical findings into submission-ready outputs.
5. A documented setup process for both online and offline execution.

The overall outcome demonstrates that LLM-assisted security analysis can be integrated effectively with traditional static detection to improve developer productivity and security awareness.

## 14. Challenges and Limitations

During or after implementation, the following practical limitations are relevant:

1. LLM quality depends on model availability and configuration.
2. Static analysis rules are pattern-based and may produce false positives or false negatives.
3. Large client-side report generation libraries increase frontend bundle size.
4. Full production security hardening still requires tighter deployment settings.
5. Automated unit and integration testing are not yet fully implemented in the repository.
6. The tool is best suited for early detection and developer guidance, not as a complete replacement for expert security auditing.

## 15. Future Enhancements

The README roadmap and repository direction suggest the following future work:

1. Analysis history with database storage
2. VS Code extension
3. GitHub integration
4. CI/CD pipeline integration
5. Custom vulnerability rules
6. Team collaboration features
7. Theme improvements and additional UI refinements

Additional technical improvements could include unit tests, stricter backend security configuration, bundle optimization, and richer language coverage validation.

## 16. Conclusion

LLM Code Analyzer is a well-structured academic and practical project that demonstrates how AI can be combined with traditional static analysis to improve source-code security review. Starting from the idea of intelligent vulnerability detection, the project progressed through planning, modular backend development, LLM integration, authentication, frontend dashboard design, multi-file support, report export, execution automation, and final build validation.

The final system is not just a concept demo. It includes a complete web interface, API-driven backend, secure login flow, vulnerability analysis engine, and exportable reports. This makes it suitable as a major project submission, a security-tool prototype, and a strong foundation for future research or product-level expansion.

## Appendix A: Main API Endpoints

| Endpoint | Method | Purpose |
|------|------|------|
| `/api/auth/login` | GET | Starts Google OAuth login |
| `/api/auth/callback` | GET | Handles OAuth callback |
| `/api/auth/me` | GET | Returns current user info |
| `/api/auth/logout` | POST | Logs out current user |
| `/api/auth/status` | GET | Returns authentication status |
| `/api/analyze` | POST | Analyzes a single code snippet |
| `/api/analyze-multiple` | POST | Analyzes multiple files |
| `/api/health` | GET | Returns service health |
| `/api/config` | GET | Returns non-sensitive configuration |

## Appendix B: Faculty Presentation Summary

If a short viva or presentation summary is needed, the project can be described in one paragraph as follows:

> LLM Code Analyzer is an AI-assisted web application for source-code security analysis. It uses a FastAPI backend and a React frontend to analyze code snippets or multiple files, detect vulnerabilities through static rules and LLM reasoning, classify issues by severity, suggest fixes, and export results as JSON, Markdown, or PDF. The system also includes Google OAuth-based authentication, protected routes, offline analysis support through Ollama, and structured reporting of attack surfaces, trust boundaries, and remediation guidance.

## References

1. FastAPI Documentation
2. React Documentation
3. Vite Documentation
4. Tailwind CSS Documentation
5. Google OAuth 2.0 Documentation
6. Ollama Documentation
7. Project README and repository source code
