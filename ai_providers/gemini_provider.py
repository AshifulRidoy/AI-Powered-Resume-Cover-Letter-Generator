import os
import google.generativeai as genai
from .base_provider import BaseAIProvider

class GeminiProvider(BaseAIProvider):
    """Google Gemini API provider - Primary choice for free tier."""
    
    def __init__(self):
        super().__init__("Google Gemini")
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("Google API key not found in environment variables")
        
        genai.configure(api_key=self.api_key)
        # Use Gemini 1.5 Flash for cost efficiency and speed
        self.model = genai.GenerativeModel('gemini-1.5-flash')
    
    def generate(self, prompt: str, max_tokens: int = None, temperature: float = None) -> str:
        """Generate response using Google Gemini API."""
        try:
            # Use the specified parameters or defaults
            temp = temperature or self.temperature
            
            # Configure generation config
            generation_config = genai.types.GenerationConfig(
                temperature=temp,
                max_output_tokens=max_tokens or self.max_tokens,
            )
            
            # Create the prompt with system message
            system_prompt = "You are a professional resume and cover letter writer. Provide clear, well-formatted responses."
            full_prompt = f"{system_prompt}\n\n{prompt}"
            
            response = self.model.generate_content(
                full_prompt,
                generation_config=generation_config
            )
            
            return self.extract_text_from_response(response)
            
        except Exception as e:
            raise Exception(f"Gemini API error: {str(e)}")
    
    def is_available(self) -> bool:
        """Check if Gemini API is available."""
        try:
            # Test with a minimal request
            response = self.model.generate_content("Test")
            return True
        except:
            return False
    
    def extract_text_from_response(self, response) -> str:
        """Extract text from Gemini response."""
        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'parts') and response.parts:
            return response.parts[0].text
        else:
            return str(response) 