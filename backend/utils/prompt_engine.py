"""
Prompt templates for LLM-based code security analysis.
"""

SECURITY_ANALYSIS_PROMPT = """You are an expert security code analyst. Analyze the following source code for security vulnerabilities, attack surfaces, and trust boundaries.

## Code to Analyze:
```{language}
{code}
```

{static_findings_section}

## Your Task:
Perform a comprehensive security analysis and return your findings in the following JSON format:

{{
    "language": "detected programming language",
    "summary": "A brief executive summary of the security analysis (2-3 sentences)",
    "risk_score": <number from 0-100, where 100 is highest risk>,
    "attack_surfaces": [
        {{
            "name": "name of attack surface",
            "type": "type (e.g., user_input, api_endpoint, file_operation, database_query)",
            "description": "description of the attack surface",
            "risk_level": "high|medium|low"
        }}
    ],
    "trust_boundaries": [
        {{
            "name": "name of trust boundary",
            "description": "what data/control crosses this boundary",
            "components": ["component1", "component2"]
        }}
    ],
    "vulnerabilities": [
        {{
            "type": "vulnerability type (e.g., SQL Injection, XSS, Command Injection)",
            "severity": "critical|high|medium|low",
            "line_numbers": [line numbers if identifiable],
            "description": "detailed description of the vulnerability",
            "vulnerable_code": "the specific vulnerable code snippet",
            "fix_suggestion": "how to fix this vulnerability",
            "fixed_code": "example of the corrected code"
        }}
    ],
    "recommendations": [
        "General security recommendation 1",
        "General security recommendation 2"
    ]
}}

## Analysis Guidelines:
1. **Attack Surfaces**: Identify all points where external data enters the system (user inputs, API calls, file reads, etc.)
2. **Trust Boundaries**: Identify where data crosses from untrusted to trusted zones (e.g., user input to database, external API to internal processing)
3. **Vulnerabilities**: Focus on common security issues:
   - SQL Injection
   - Cross-Site Scripting (XSS)
   - Command Injection
   - Path Traversal
   - Hardcoded Secrets/Credentials
   - Insecure Deserialization
   - Authentication/Authorization flaws
   - Sensitive Data Exposure
   - Security Misconfiguration
4. **Severity Levels**:
   - **critical**: Immediate exploitation possible, severe impact
   - **high**: Exploitation likely, significant impact
   - **medium**: Exploitation possible, moderate impact
   - **low**: Limited exploitation potential, minor impact
5. **Fix Suggestions**: Provide specific, actionable fixes with corrected code examples

Return ONLY valid JSON, no additional text or markdown formatting."""


STATIC_FINDINGS_TEMPLATE = """
## Static Analysis Findings:
The following potential issues were detected by static analysis:
{findings}

Consider these findings in your analysis and validate whether they represent actual vulnerabilities.
"""


def build_analysis_prompt(code: str, language: str = "auto", static_findings: list = None) -> str:
    """
    Build the complete analysis prompt with code and optional static findings.
    
    Args:
        code: Source code to analyze
        language: Programming language (or "auto" for detection)
        static_findings: Optional list of static analysis findings
    
    Returns:
        Complete prompt string
    """
    static_section = ""
    if static_findings:
        findings_text = "\n".join(f"- {f['type']}: {f['description']} (line {f.get('line', 'N/A')})" 
                                   for f in static_findings)
        static_section = STATIC_FINDINGS_TEMPLATE.format(findings=findings_text)
    
    return SECURITY_ANALYSIS_PROMPT.format(
        language=language if language != "auto" else "",
        code=code,
        static_findings_section=static_section
    )
