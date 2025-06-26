import json
import os
from typing import Dict, Any, Optional

class ProfileManager:
    """Manages user profile data for resume and cover letter generation."""
    
    def __init__(self, profile_file: str = "data/profile.json"):
        self.profile_file = profile_file
        self.profile_data = {}
        self._load_profile()
    
    def _load_profile(self):
        """Load profile data from file."""
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, 'r') as f:
                    self.profile_data = json.load(f)
            except Exception as e:
                print(f"Error loading profile: {e}")
                self.profile_data = {}
    
    def save_profile(self, profile_data: Dict[str, Any]) -> bool:
        """Save profile data to file."""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.profile_file), exist_ok=True)
            
            with open(self.profile_file, 'w') as f:
                json.dump(profile_data, f, indent=2)
            
            self.profile_data = profile_data
            return True
        except Exception as e:
            print(f"Error saving profile: {e}")
            return False
    
    def get_profile(self) -> Dict[str, Any]:
        """Get current profile data."""
        return self.profile_data.copy()
    
    def update_profile(self, updates: Dict[str, Any]) -> bool:
        """Update specific fields in the profile."""
        self.profile_data.update(updates)
        return self.save_profile(self.profile_data)
    
    def get_field(self, field: str, default: Any = "") -> Any:
        """Get a specific field from the profile."""
        return self.profile_data.get(field, default)
    
    def set_field(self, field: str, value: Any) -> bool:
        """Set a specific field in the profile."""
        self.profile_data[field] = value
        return self.save_profile(self.profile_data)
    
    def has_required_fields(self) -> bool:
        """Check if profile has required fields for generation."""
        required_fields = ["name", "email", "summary", "skills", "experience"]
        return all(field in self.profile_data and self.profile_data[field] for field in required_fields)
    
    def get_missing_fields(self) -> list:
        """Get list of missing required fields."""
        required_fields = ["name", "email", "summary", "skills", "experience"]
        missing = []
        for field in required_fields:
            if field not in self.profile_data or not self.profile_data[field]:
                missing.append(field)
        return missing
    
    def validate_profile(self) -> Dict[str, Any]:
        """Validate profile data and return validation results."""
        validation = {
            "is_valid": True,
            "missing_fields": [],
            "warnings": []
        }
        
        # Check required fields
        missing = self.get_missing_fields()
        if missing:
            validation["is_valid"] = False
            validation["missing_fields"] = missing
        
        # Check field lengths
        if "summary" in self.profile_data and len(self.profile_data["summary"]) < 50:
            validation["warnings"].append("Professional summary is quite short")
        
        if "skills" in self.profile_data and len(self.profile_data["skills"]) < 20:
            validation["warnings"].append("Skills section is quite short")
        
        if "experience" in self.profile_data and len(self.profile_data["experience"]) < 100:
            validation["warnings"].append("Work experience section is quite short")
        
        return validation
    
    def export_profile(self, format: str = "json") -> str:
        """Export profile data in specified format."""
        if format.lower() == "json":
            return json.dumps(self.profile_data, indent=2)
        elif format.lower() == "txt":
            lines = []
            for key, value in self.profile_data.items():
                lines.append(f"{key.upper()}: {value}")
            return "\n\n".join(lines)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def import_profile(self, data: str, format: str = "json") -> bool:
        """Import profile data from specified format."""
        try:
            if format.lower() == "json":
                profile_data = json.loads(data)
            elif format.lower() == "txt":
                profile_data = {}
                lines = data.split("\n\n")
                for line in lines:
                    if ":" in line:
                        key, value = line.split(":", 1)
                        profile_data[key.lower().strip()] = value.strip()
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            return self.save_profile(profile_data)
        except Exception as e:
            print(f"Error importing profile: {e}")
            return False
    
    def clear_profile(self) -> bool:
        """Clear all profile data."""
        self.profile_data = {}
        try:
            if os.path.exists(self.profile_file):
                os.remove(self.profile_file)
            return True
        except Exception as e:
            print(f"Error clearing profile: {e}")
            return False 