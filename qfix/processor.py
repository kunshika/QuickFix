import os
from rich.console import Console
from rich.markdown import Markdown
from rich.syntax import Syntax
from langchain_groq import ChatGroq

console = Console()

class CodeProcessor:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if self.api_key:
            # Initialize ChatGroq with a specific model
            self.model = ChatGroq(
                api_key=self.api_key,
                model="groq/compound"  # Fast and capable model
            )
        else:
            self.model = None
            console.print("[yellow]Warning: No GROQ_API_KEY found. Running in mock mode.[/yellow]")

    def process_code(self, code_snippet: str, language: str = "python"):
        if not self.model:
            return self._mock_process(code_snippet, language)

        prompt = f"""
        You are an expert code formatting and explanation assistant.
        I will provide you with a snippet of {language} code.
        
        Your task is to:
        1. Format the code according to best practices (indentation, spacing, etc.).
        2. STRICTLY DO NOT CHANGE THE LOGIC. Only improve readability and formatting.
        3. Explain the formatting changes you made.

        Output format should be strictly separated sections:
        
        ---IMPROVED_CODE---
        (The code block only)
        ---EXPLANATION---
        (The explanation in Markdown)
        
        Here is the code:
        ```
        {code_snippet}
        ```
        """

        try:
            response = self.model.invoke(prompt)
            return self._parse_response(response.content)
        except Exception as e:
            console.print(f"[red]Error calling Groq API: {e}[/red]")
            return self._mock_process(code_snippet, language)

    def _parse_response(self, text: str):
        parts = text.split("---IMPROVED_CODE---")
        if len(parts) < 2:
            return {"code": "", "explanation": text} # Fallback
        
        content = parts[1].split("---EXPLANATION---")
        code = content[0].strip()
        # Remove markdown code fences if present
        if code.startswith("```"):
            code = "\n".join(code.split("\n")[1:])
        if code.endswith("```"):
            code = "\n".join(code.split("\n")[:-1])
            
        explanation = content[1].strip() if len(content) > 1 else ""
        
        return {
            "code": code.strip(),
            "explanation": explanation
        }

    def _mock_process(self, code_snippet: str, language: str):
        return {
            "code": code_snippet,  # Just return original in mock
            "explanation": "## Mock Explanation\n\nNo API key provided. This is a mock response.\n\n- The code was not actually processed by AI.\n- Please set `GROQ_API_KEY` in your .env file to get real results."
        }
