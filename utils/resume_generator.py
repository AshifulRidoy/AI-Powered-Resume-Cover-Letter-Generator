from typing import Dict, Any, List
from prompts.prompt_manager import PromptManager
from functools import lru_cache

class ResumeGenerator:
    """Generates customized resumes using AI with predefined guidelines."""
    
    def __init__(self, ai_provider):
        self.ai_provider = ai_provider
        self.prompt_manager = PromptManager()
    
    def generate_resume(self, profile_data: dict, job_description: str, job_analysis: dict = None, 
                       tone: str = "professional", focus_areas: list = None, 
                       experience_level: str = "mid_level", industry: str = "general") -> str:
        """Generate optimized resume content with token efficiency."""
        
        # Token optimization: Use shorter, more focused prompts
        prompt_manager = PromptManager()
        
        # Get optimized prompts based on focus areas
        if focus_areas and "Technical Skills" in focus_areas:
            base_prompt = prompt_manager.get_resume_prompt("technical_focused")
        elif focus_areas and "Leadership" in focus_areas:
            base_prompt = prompt_manager.get_resume_prompt("leadership_focused")
        else:
            base_prompt = prompt_manager.get_resume_prompt("standard")
        
        # Optimize job description length (keep only essential parts)
        optimized_job_desc = self._optimize_job_description(job_description, job_analysis)
        
        # Create concise profile summary
        profile_summary = self._create_profile_summary(profile_data)
        
        # Build efficient prompt
        prompt = f"""
{base_prompt}

PROFILE: {profile_summary}
JOB: {optimized_job_desc}
TONE: {tone}
LEVEL: {experience_level}
INDUSTRY: {industry}

Generate a professional resume text content only.
"""
        
        # Use lower max_tokens for efficiency
        max_tokens = 2000 if "sections_only" in focus_areas else 3000
        
        try:
            response = self.ai_provider.generate(prompt, max_tokens=max_tokens, temperature=0.7)
            return response.strip()
        except Exception as e:
            raise Exception(f"Failed to generate resume: {str(e)}")
    
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
        if len(job_description) > 500:
            return job_description[:500] + "..."
        
        return job_description
    
    def _create_profile_summary(self, profile_data: dict) -> str:
        """Create a concise profile summary to reduce token usage."""
        summary_parts = []
        
        if profile_data.get("name"):
            summary_parts.append(f"Name: {profile_data['name']}")
        
        if profile_data.get("summary"):
            # Truncate summary if too long
            summary = profile_data["summary"]
            if len(summary) > 200:
                summary = summary[:200] + "..."
            summary_parts.append(f"Summary: {summary}")
        
        if profile_data.get("skills"):
            # Limit skills to top 10
            skills = profile_data["skills"].split(",")[:10]
            summary_parts.append(f"Skills: {', '.join(skills)}")
        
        if profile_data.get("experience"):
            # Truncate experience if too long
            experience = profile_data["experience"]
            if len(experience) > 300:
                experience = experience[:300] + "..."
            summary_parts.append(f"Experience: {experience}")
        
        return " | ".join(summary_parts)
    
    def generate_resume_section(self, section: str, profile_data: Dict[str, Any], 
                              job_description: str, job_analysis: Dict[str, Any] = None,
                              tone: str = "professional") -> str:
        """Generate a specific section of the resume using predefined prompts."""
        
        # Validate tone
        tone = tone.lower() if tone else "professional"
        
        # Get the section prompt using predefined guidelines
        prompt = self.prompt_manager.get_resume_section_prompt(
            section, profile_data, job_description, job_analysis, tone
        )
        
        try:
            return self.ai_provider.generate(prompt, max_tokens=500)
        except Exception as e:
            return f"Error generating {section} section: {str(e)}"
    
    def get_customization_options(self) -> Dict[str, Any]:
        """Get available customization options from predefined guidelines."""
        return self.prompt_manager.get_customization_options()
    
    def validate_tone(self, tone: str) -> bool:
        """Validate if a tone is supported."""
        return self.prompt_manager.validate_tone(tone.lower())
    
    def validate_industry(self, industry: str) -> bool:
        """Validate if an industry is supported."""
        return self.prompt_manager.validate_industry(industry.lower())
    
    def validate_experience_level(self, experience_level: str) -> bool:
        """Validate if an experience level is supported."""
        return self.prompt_manager.validate_experience_level(experience_level.lower().replace(" ", "_"))
    
    def get_industry_keywords(self, industry: str) -> List[str]:
        """Get keywords for a specific industry."""
        return self.prompt_manager.get_industry_keywords(industry.lower())
    
    def get_industry_focus_areas(self, industry: str) -> List[str]:
        """Get focus areas for a specific industry."""
        return self.prompt_manager.get_industry_focus_areas(industry.lower())
    
    def get_action_verbs(self, limit: int = 10) -> List[str]:
        """Get action verbs for resume writing."""
        return self.prompt_manager.get_action_verbs(limit)
    
    def generate_modified_resume_sections(self, profile_data: Dict[str, Any], job_description: str, job_analysis: Dict[str, Any] = None, tone: str = "professional") -> Dict[str, str]:
        """
        Generate only the modified Professional Summary, Work Experience, and Skills sections
        based on the job description and profile data.
        Returns a dictionary with the modified sections.
        """
        sections = ["summary", "experience", "skills"]
        results = {}
        for section in sections:
            results[section] = self.generate_resume_section(
                section=section,
                profile_data=profile_data,
                job_description=job_description,
                job_analysis=job_analysis,
                tone=tone
            )
        return results

    @lru_cache(maxsize=8)
    def get_section_prompt(self, section: str) -> str:
        """Cache and return the prompt template for a section."""
        return self.prompt_manager.get_resume_section_prompt(section)

    def generate_resume_sections(self, profile_data: dict, job_description: str, job_analysis: dict = None,
                                 tone: str = "professional", focus_areas: list = None, experience_level: str = "mid_level", industry: str = "general") -> dict:
        """Batch generate skills, work experience, and professional summary in one call."""
        prompt = self.prompt_manager.get_batch_resume_sections_prompt(profile_data, job_description, job_analysis, tone, focus_areas, experience_level, industry)
        try:
            response = self._generate_with_retry(prompt, max_tokens=2000)
            # Expecting a JSON or clearly delimited response for sections
            return self._parse_sections_response(response)
        except Exception as e:
            raise Exception(f"Failed to generate resume sections: {str(e)}")

    def generate_section(self, section: str, profile_data: dict, job_description: str, job_analysis: dict = None,
                        tone: str = "professional", focus_areas: list = None, experience_level: str = "mid_level", industry: str = "general") -> str:
        """Generate a single section (skills, work experience, or summary)."""
        prompt = self.get_section_prompt(section)
        full_prompt = self.prompt_manager.fill_section_prompt(prompt, section, profile_data, job_description, job_analysis, tone, focus_areas, experience_level, industry)
        try:
            return self._generate_with_retry(full_prompt, max_tokens=800)
        except Exception as e:
            raise Exception(f"Failed to generate {section}: {str(e)}")

    def _generate_with_retry(self, prompt, max_tokens):
        """Smart retry logic: retry with a shorter prompt if quota/token error occurs."""
        try:
            return self.ai_provider.generate(prompt, max_tokens=max_tokens)
        except Exception as e:
            if "quota" in str(e).lower() or "token" in str(e).lower():
                # Retry with a shorter prompt (remove job_analysis if present)
                if "job_analysis" in prompt:
                    prompt_short = prompt.replace(str(prompt.get('job_analysis', '')), '')
                else:
                    prompt_short = prompt
                return self.ai_provider.generate(prompt_short, max_tokens=max_tokens//2)
            raise

    def _parse_sections_response(self, response: str) -> dict:
        """Parse the batch response into sections. Expecting JSON or delimited text."""
        import json
        try:
            return json.loads(response)
        except Exception:
            # Fallback: try to split by section headers
            sections = {"summary": "", "skills": "", "experience": ""}
            for key in sections:
                if key in response.lower():
                    start = response.lower().find(key)
                    end = response.lower().find("\n", start)
                    sections[key] = response[start:end].strip()
            return sections 