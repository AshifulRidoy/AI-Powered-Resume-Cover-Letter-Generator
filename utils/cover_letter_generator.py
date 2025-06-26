from typing import Dict, Any, List
from prompts.prompt_manager import PromptManager
from functools import lru_cache

class CoverLetterGenerator:
    """Generates customized cover letters using AI with predefined guidelines."""
    
    def __init__(self, ai_provider):
        self.ai_provider = ai_provider
        self.prompt_manager = PromptManager()
    
    @lru_cache(maxsize=8)
    def get_cover_letter_prompt(self) -> str:
        return self.prompt_manager.get_cover_letter_prompt("standard")
    
    def generate_cover_letter(self, profile_data: dict, job_description: str, job_analysis: dict = None,
                            tone: str = "professional", focus_areas: list = None,
                            experience_level: str = "mid_level") -> str:
        """Generate optimized cover letter content with token efficiency."""
        
        prompt = self.get_cover_letter_prompt()
        full_prompt = self.prompt_manager.fill_cover_letter_prompt(prompt, profile_data, job_description, job_analysis, tone, focus_areas, experience_level)
        
        try:
            return self._generate_with_retry(full_prompt, max_tokens=1500)
        except Exception as e:
            raise Exception(f"Failed to generate cover letter: {str(e)}")
    
    def generate_batch_resume_and_cover_letter(self, profile_data: dict, job_description: str, job_analysis: dict = None,
                                               tone: str = "professional", focus_areas: list = None, experience_level: str = "mid_level", industry: str = "general") -> dict:
        """Batch generate resume sections and cover letter in one call."""
        prompt = self.prompt_manager.get_batch_resume_and_cover_letter_prompt(profile_data, job_description, job_analysis, tone, focus_areas, experience_level, industry)
        try:
            response = self._generate_with_retry(prompt, max_tokens=3000)
            return self._parse_batch_response(response)
        except Exception as e:
            raise Exception(f"Failed to generate batch content: {str(e)}")
    
    def _generate_with_retry(self, prompt, max_tokens):
        try:
            return self.ai_provider.generate(prompt, max_tokens=max_tokens)
        except Exception as e:
            if "quota" in str(e).lower() or "token" in str(e).lower():
                return self.ai_provider.generate(prompt, max_tokens=max_tokens//2)
            raise
    
    def _parse_batch_response(self, response: str) -> dict:
        import json
        try:
            return json.loads(response)
        except Exception:
            # Fallback: try to split by section headers
            sections = {"summary": "", "skills": "", "experience": "", "cover_letter": ""}
            for key in sections:
                if key in response.lower():
                    start = response.lower().find(key)
                    end = response.lower().find("\n", start)
                    sections[key] = response[start:end].strip()
            return sections
    
    def _optimize_job_description(self, job_description: str, job_analysis: dict = None) -> str:
        """Optimize job description to reduce token usage while keeping essential info."""
        if not job_description:
            return ""
        
        # If we have job analysis, use the key points
        if job_analysis:
            key_requirements = job_analysis.get("requirements", [])
            key_skills = job_analysis.get("skills", [])
            
            if key_requirements and key_skills:
                return f"Requirements: {', '.join(key_requirements[:5])}. Skills: {', '.join(key_skills[:5])}."
        
        # Otherwise, truncate the job description
        if len(job_description) > 400:
            return job_description[:400] + "..."
        
        return job_description
    
    def _create_profile_summary(self, profile_data: dict) -> str:
        """Create a concise profile summary to reduce token usage."""
        summary_parts = []
        
        if profile_data.get("name"):
            summary_parts.append(f"Name: {profile_data['name']}")
        
        if profile_data.get("summary"):
            # Truncate summary if too long
            summary = profile_data["summary"]
            if len(summary) > 150:
                summary = summary[:150] + "..."
            summary_parts.append(f"Summary: {summary}")
        
        if profile_data.get("experience"):
            # Truncate experience if too long
            experience = profile_data["experience"]
            if len(experience) > 200:
                experience = experience[:200] + "..."
            summary_parts.append(f"Experience: {experience}")
        
        return " | ".join(summary_parts)
    
    def generate_cover_letter_section(self, section: str, profile_data: Dict[str, Any],
                                    job_description: str, job_analysis: Dict[str, Any] = None,
                                    company_name: str = "", position_title: str = "", tone: str = "professional") -> str:
        """Generate a specific section of the cover letter using predefined prompts."""
        
        # Validate tone
        tone = tone.lower() if tone else "professional"
        
        # Get the section prompt using predefined guidelines
        prompt = self.prompt_manager.get_cover_letter_section_prompt(
            section, profile_data, job_description, job_analysis, company_name, position_title, tone
        )
        
        try:
            return self.ai_provider.generate(prompt, max_tokens=300)
        except Exception as e:
            return f"Error generating {section} section: {str(e)}"
    
    def get_customization_options(self) -> Dict[str, Any]:
        """Get available customization options from predefined guidelines."""
        return self.prompt_manager.get_customization_options()
    
    def validate_tone(self, tone: str) -> bool:
        """Validate if a tone is supported."""
        return self.prompt_manager.validate_tone(tone.lower())
    
    def validate_experience_level(self, experience_level: str) -> bool:
        """Validate if an experience level is supported."""
        return self.prompt_manager.validate_experience_level(experience_level.lower().replace(" ", "_")) 