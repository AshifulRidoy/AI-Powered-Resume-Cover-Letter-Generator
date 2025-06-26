from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseAIProvider(ABC):
    """Base class for all AI providers."""
    
    def __init__(self, name: str):
        self.name = name
        self.max_tokens = 4000
        self.temperature = 0.7
    
    @abstractmethod
    def generate(self, prompt: str, max_tokens: int = None, temperature: float = None) -> str:
        """Generate text response from the AI model."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if the provider is available and working."""
        pass
    
    def set_parameters(self, max_tokens: int = None, temperature: float = None):
        """Set generation parameters."""
        if max_tokens:
            self.max_tokens = max_tokens
        if temperature:
            self.temperature = temperature
    
    def format_prompt(self, system_prompt: str, user_prompt: str) -> str:
        """Format prompt for the specific provider."""
        return f"{system_prompt}\n\n{user_prompt}"
    
    def extract_text_from_response(self, response: Any) -> str:
        """Extract text content from provider-specific response format."""
        if isinstance(response, str):
            return response
        elif isinstance(response, dict):
            # Handle different response formats
            if 'choices' in response:
                return response['choices'][0]['message']['content']
            elif 'content' in response:
                return response['content']
            elif 'text' in response:
                return response['text']
            else:
                return str(response)
        else:
            return str(response) 