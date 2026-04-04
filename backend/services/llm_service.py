"""
LLM Service for interacting with OpenAI, Gemini, and Ollama.
Provides unified interface for multiple LLM providers.
"""

import json
import httpx
from typing import Optional
from openai import OpenAI, OpenAIError

from backend.config import settings


class LLMService:
    """Service for LLM interactions supporting OpenAI, Gemini, and Ollama."""
    
    def __init__(self):
        self.mode = settings.llm_mode
        
        if self.mode == "openai":
            if not settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required for OpenAI mode")
            self.client = OpenAI(api_key=settings.openai_api_key)
            self.model = settings.openai_model
        elif self.mode == "gemini":
            if not settings.gemini_api_key:
                raise ValueError("GEMINI_API_KEY is required for Gemini mode")
            import google.generativeai as genai
            genai.configure(api_key=settings.gemini_api_key)
            self.genai = genai
            self.model = settings.gemini_model
        else:  # ollama
            self.ollama_url = settings.ollama_base_url
            self.model = settings.ollama_model
    
    async def analyze(self, prompt: str) -> dict:
        """
        Send prompt to LLM and get structured response.
        
        Args:
            prompt: The analysis prompt with code
            
        Returns:
            Parsed JSON response from LLM
        """
        if self.mode == "openai":
            return await self._analyze_openai(prompt)
        elif self.mode == "gemini":
            return await self._analyze_gemini(prompt)
        else:
            return await self._analyze_ollama(prompt)
    
    async def _analyze_openai(self, prompt: str) -> dict:
        """Analyze using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a security expert analyzing code for vulnerabilities. Always respond with valid JSON only."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,
                max_tokens=4096,
                response_format={"type": "json_object"}
            )
            
            content = response.choices[0].message.content
            return self._parse_response(content)
            
        except OpenAIError as e:
            raise LLMError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise LLMError(f"Unexpected error during OpenAI analysis: {str(e)}")
    
    async def _analyze_gemini(self, prompt: str) -> dict:
        """Analyze using Google Gemini API."""
        try:
            model = self.genai.GenerativeModel(
                self.model,
                generation_config={
                    "temperature": 0.1,
                    "max_output_tokens": 4096,
                }
            )
            
            full_prompt = f"""You are a security expert analyzing code for vulnerabilities. 
You must respond with valid JSON only - no markdown, no code blocks, just pure JSON.

{prompt}"""
            
            response = model.generate_content(full_prompt)
            content = response.text
            return self._parse_response(content)
            
        except Exception as e:
            raise LLMError(f"Gemini API error: {str(e)}")
    
    async def _analyze_ollama(self, prompt: str) -> dict:
        """Analyze using Ollama local model with streaming to avoid truncation."""
        try:
            # Reduced timeout - fall back to static analysis faster if LLM is slow
            timeout = httpx.Timeout(120.0, connect=30.0)
            
            async with httpx.AsyncClient(timeout=timeout) as client:
                # Use streaming to avoid truncation issues
                async with client.stream(
                    "POST",
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model,
                        "prompt": f"""Analyze this code for security vulnerabilities. Return ONLY a valid JSON object.

{prompt}

RULES:
1. Return ONLY valid JSON, no other text
2. Keep all descriptions under 25 words
3. Maximum 4 vulnerabilities
4. Start with {{ end with }}""",
                        "stream": True,
                        "options": {
                            "temperature": 0.1,
                            "num_predict": 4096,
                            "num_ctx": 8192
                        }
                    }
                ) as response:
                    response.raise_for_status()
                    
                    # Collect all streamed chunks
                    full_response = ""
                    async for line in response.aiter_lines():
                        if line.strip():
                            try:
                                chunk = json.loads(line)
                                full_response += chunk.get("response", "")
                                if chunk.get("done", False):
                                    break
                            except json.JSONDecodeError:
                                continue
                
                if not full_response.strip():
                    raise LLMError("Ollama returned empty response")
                
                return self._parse_response(full_response)
                
        except httpx.TimeoutException:
            raise LLMError("Ollama request timed out. Try with smaller code.")
        except httpx.HTTPError as e:
            raise LLMError(f"Ollama API error: {str(e)}")
        except LLMError:
            raise
        except Exception as e:
            raise LLMError(f"Unexpected error during Ollama analysis: {str(e)}")
    
    def _parse_response(self, content: str) -> dict:
        """Parse LLM response into structured dict with repair for truncated JSON."""
        try:
            content = content.strip()
            
            # Handle potential markdown code blocks
            if content.startswith("```"):
                lines = content.split("\n")
                content = "\n".join(lines[1:-1])
            
            # Try to find JSON object in the response
            start_idx = content.find('{')
            end_idx = content.rfind('}')
            
            if start_idx != -1 and end_idx != -1:
                content = content[start_idx:end_idx + 1]
            elif start_idx != -1:
                # JSON is truncated - try to repair it
                content = self._repair_truncated_json(content[start_idx:])
            
            return json.loads(content)
        except json.JSONDecodeError as e:
            # Try to repair and parse again
            try:
                repaired = self._repair_truncated_json(content)
                return json.loads(repaired)
            except:
                raise LLMError(f"Failed to parse LLM response as JSON: {str(e)}\nResponse: {content[:500]}")
    
    def _repair_truncated_json(self, content: str) -> str:
        """Attempt to repair truncated JSON by closing open structures."""
        # Count open brackets and braces
        open_braces = content.count('{') - content.count('}')
        open_brackets = content.count('[') - content.count(']')
        
        # Check if we're in the middle of a string
        in_string = False
        escape_next = False
        for char in content:
            if escape_next:
                escape_next = False
                continue
            if char == '\\':
                escape_next = True
                continue
            if char == '"':
                in_string = not in_string
        
        # If in string, close it
        if in_string:
            content += '"'
        
        # Remove trailing comma if present
        content = content.rstrip().rstrip(',')
        
        # Close open brackets and braces
        content += ']' * open_brackets
        content += '}' * open_braces
        
        return content
    
    def health_check(self) -> bool:
        """Check if the LLM service is available."""
        if self.mode == "openai":
            try:
                self.client.models.list()
                return True
            except Exception:
                return False
        elif self.mode == "gemini":
            try:
                # Simple check - list models
                list(self.genai.list_models())
                return True
            except Exception:
                return False
        else:  # ollama
            try:
                response = httpx.get(f"{self.ollama_url}/api/tags", timeout=5)
                return response.status_code == 200
            except Exception:
                return False


class LLMError(Exception):
    """Custom exception for LLM-related errors."""
    pass


# Singleton instance
_llm_service: Optional[LLMService] = None


def get_llm_service() -> LLMService:
    """Get or create the LLM service singleton."""
    global _llm_service
    if _llm_service is None:
        _llm_service = LLMService()
    return _llm_service
