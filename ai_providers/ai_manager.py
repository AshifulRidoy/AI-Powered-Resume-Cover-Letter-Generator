import os
import time
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from .gemini_provider import GeminiProvider

class AIManager:
    """Manages Google Gemini AI provider for resume and cover letter generation."""
    
    def __init__(self):
        self.provider = None
        self.quota_file = "data/quota_usage.json"
        self._initialize_provider()
    
    def _initialize_provider(self):
        """Initialize Google Gemini provider."""
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key:
            try:
                self.provider = GeminiProvider()
            except Exception as e:
                print(f"Failed to initialize Google Gemini: {e}")
    
    def _load_quota_usage(self) -> Dict[str, Any]:
        """Load quota usage from file."""
        try:
            if os.path.exists(self.quota_file):
                with open(self.quota_file, 'r') as f:
                    return json.load(f)
        except Exception:
            pass
        return {
            "daily_requests": 0,
            "minute_requests": 0,
            "last_minute_reset": time.time(),
            "last_daily_reset": time.time(),
            "quota_errors": []
        }
    
    def _save_quota_usage(self, usage: Dict[str, Any]):
        """Save quota usage to file."""
        try:
            os.makedirs("data", exist_ok=True)
            with open(self.quota_file, 'w') as f:
                json.dump(usage, f, indent=2)
        except Exception:
            pass
    
    def _update_quota_usage(self, success: bool = True, error: str = None):
        """Update quota usage tracking."""
        usage = self._load_quota_usage()
        current_time = time.time()
        
        # Check if we need to reset minute counter (every 60 seconds)
        if current_time - usage["last_minute_reset"] >= 60:
            usage["minute_requests"] = 0
            usage["last_minute_reset"] = current_time
        
        # Check if we need to reset daily counter (every 24 hours)
        if current_time - usage["last_daily_reset"] >= 86400:  # 24 hours
            usage["daily_requests"] = 0
            usage["last_daily_reset"] = current_time
        
        # Increment counters
        if success:
            usage["minute_requests"] += 1
            usage["daily_requests"] += 1
        
        # Store quota errors
        if error and "quota" in error.lower():
            usage["quota_errors"].append({
                "timestamp": current_time,
                "error": error
            })
            # Keep only last 10 errors
            usage["quota_errors"] = usage["quota_errors"][-10:]
        
        self._save_quota_usage(usage)
    
    def get_quota_info(self) -> Dict[str, Any]:
        """Get current quota usage and reset information."""
        usage = self._load_quota_usage()
        current_time = time.time()
        
        # Calculate time until resets
        minute_reset_in = max(0, 60 - (current_time - usage["last_minute_reset"]))
        daily_reset_in = max(0, 86400 - (current_time - usage["last_daily_reset"]))
        
        # Format reset times
        minute_reset_str = f"{int(minute_reset_in)}s" if minute_reset_in < 60 else f"{int(minute_reset_in/60)}m {int(minute_reset_in%60)}s"
        daily_reset_str = f"{int(daily_reset_in/3600)}h {int((daily_reset_in%3600)/60)}m" if daily_reset_in > 3600 else f"{int(daily_reset_in/60)}m"
        
        return {
            "daily_used": usage["daily_requests"],
            "daily_limit": 1500,
            "daily_remaining": max(0, 1500 - usage["daily_requests"]),
            "daily_reset_in": daily_reset_str,
            "daily_reset_timestamp": usage["last_daily_reset"] + 86400,
            
            "minute_used": usage["minute_requests"],
            "minute_limit": 15,
            "minute_remaining": max(0, 15 - usage["minute_requests"]),
            "minute_reset_in": minute_reset_str,
            "minute_reset_timestamp": usage["last_minute_reset"] + 60,
            
            "last_quota_error": usage["quota_errors"][-1] if usage["quota_errors"] else None
        }
    
    def get_available_providers(self) -> Dict[str, Dict[str, Any]]:
        """Get Google Gemini provider status without making API calls."""
        available = {}
        
        if self.provider:
            # Check if provider is initialized without making API calls
            available["Google Gemini"] = {
                "available": True,
                "provider": self.provider,
                "test_response": None
            }
        else:
            available["Google Gemini"] = {
                "available": False,
                "error": "API key not found",
                "provider": None
            }
        
        return available
    
    def test_provider_connection(self) -> Dict[str, Any]:
        """Test the provider connection with a minimal request (only when needed)."""
        if not self.provider:
            return {"available": False, "error": "Provider not initialized"}
        
        try:
            # Test with a very minimal request
            test_response = self.provider.generate("Hi", max_tokens=5)
            self._update_quota_usage(success=True)
            return {"available": True, "response": test_response}
        except Exception as e:
            error_msg = str(e)
            self._update_quota_usage(success=False, error=error_msg)
            return {"available": False, "error": error_msg}
    
    def get_provider(self, provider_name: str = "Google Gemini"):
        """Get the Google Gemini provider."""
        if provider_name != "Google Gemini":
            raise ValueError("Only Google Gemini is supported")
        
        available = self.get_available_providers()
        if "Google Gemini" in available and available["Google Gemini"]["available"]:
            return available["Google Gemini"]["provider"]
        else:
            raise ValueError("Google Gemini is not available. Please check your API key.")
    
    def get_best_provider(self) -> Optional[Any]:
        """Get the Google Gemini provider."""
        available = self.get_available_providers()
        if "Google Gemini" in available and available["Google Gemini"]["available"]:
            return available["Google Gemini"]["provider"]
        return None
    
    def generate_with_fallback(self, prompt: str, max_tokens: int = 1000) -> str:
        """Generate response using Google Gemini."""
        provider = self.get_best_provider()
        if provider:
            try:
                response = provider.generate(prompt, max_tokens)
                self._update_quota_usage(success=True)
                return response
            except Exception as e:
                error_msg = str(e)
                self._update_quota_usage(success=False, error=error_msg)
                raise Exception(f"Google Gemini error: {error_msg}")
        else:
            raise Exception("Google Gemini is not available. Please check your API key.")
    
    def get_provider_info(self) -> Dict[str, Dict[str, Any]]:
        """Get information about Google Gemini."""
        return {
            "Google Gemini": {
                "free_tier": "15 requests/minute, 1500 requests/day",
                "model": "Gemini 1.5 Flash",
                "setup": "Very Easy",
                "recommended": True,
                "url": "https://makersuite.google.com/app/apikey"
            }
        } 