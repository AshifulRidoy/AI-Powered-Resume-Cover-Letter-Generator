"""
Prompt Manager
This module manages and coordinates all predefined guidelines and prompts for consistent usage.
"""

from .resume_guidelines import ResumeGuidelines, ResumePrompts
from .cover_letter_guidelines import CoverLetterGuidelines, CoverLetterPrompts
from .job_analysis_guidelines import JobAnalysisGuidelines, JobAnalysisPrompts
from .ultimate_resume_cover_letter_prompt import ULTIMATE_PROMPT
import jinja2

class PromptManager:
    """Manages all predefined guidelines and prompts for the system."""
    
    def __init__(self):
        self.resume_guidelines = ResumeGuidelines()
        self.resume_prompts = ResumePrompts()
        self.cover_letter_guidelines = CoverLetterGuidelines()
        self.cover_letter_prompts = CoverLetterPrompts()
        self.job_analysis_guidelines = JobAnalysisGuidelines()
        self.job_analysis_prompts = JobAnalysisPrompts()
    
    def get_resume_prompt(self, profile_data, job_description, job_analysis=None, 
                         tone="professional", focus_areas=None, experience_level="mid_level", 
                         industry="general"):
        """Get a resume generation prompt with predefined guidelines."""
        return self.resume_prompts.get_main_resume_prompt(
            profile_data, job_description, job_analysis, tone, focus_areas, 
            experience_level, industry
        )
    
    def get_cover_letter_prompt(self, profile_data, job_description, job_analysis=None,
                               tone="professional", focus_areas=None, company_name="", 
                               position_title="", experience_level="mid_level"):
        """Get a cover letter generation prompt with predefined guidelines."""
        return self.cover_letter_prompts.get_main_cover_letter_prompt(
            profile_data, job_description, job_analysis, tone, focus_areas,
            company_name, position_title, experience_level
        )
    
    def get_job_analysis_prompt(self, job_description):
        """Get a job analysis prompt with predefined guidelines."""
        return self.job_analysis_prompts.get_main_analysis_prompt(job_description)
    
    def get_resume_section_prompt(self, section: str) -> str:
        """Return a prompt template for a specific resume section."""
        if section == "skills":
            return "Generate the SKILLS section for a resume based on the following profile and job description."
        elif section == "experience":
            return "Generate the WORK EXPERIENCE section for a resume based on the following profile and job description."
        elif section == "summary":
            return "Generate the PROFESSIONAL SUMMARY section for a resume based on the following profile and job description."
        else:
            return "Generate the requested section for a resume."
    
    def get_cover_letter_section_prompt(self, section, profile_data, job_description,
                                       job_analysis=None, company_name="", position_title="", tone="professional"):
        """Get a specific cover letter section prompt."""
        if section == "introduction":
            return self.cover_letter_prompts.get_introduction_prompt(profile_data, job_description, job_analysis, company_name, position_title, tone)
        elif section == "why_interested":
            return self.cover_letter_prompts.get_why_interested_prompt(profile_data, job_description, job_analysis, company_name, position_title)
        elif section == "qualifications":
            return self.cover_letter_prompts.get_qualifications_prompt(profile_data, job_description, job_analysis, company_name, position_title)
        elif section == "closing":
            return self.cover_letter_prompts.get_closing_prompt(profile_data, job_description, job_analysis, company_name, position_title)
        else:
            return f"Unknown cover letter section: {section}"
    
    def get_job_analysis_section_prompt(self, section, job_description):
        """Get a specific job analysis section prompt."""
        if section == "requirements":
            return self.job_analysis_prompts.get_requirements_extraction_prompt(job_description)
        elif section == "skills":
            return self.job_analysis_prompts.get_skills_extraction_prompt(job_description)
        elif section == "experience_level":
            return self.job_analysis_prompts.get_experience_level_prompt(job_description)
        elif section == "industry":
            return self.job_analysis_prompts.get_industry_identification_prompt(job_description)
        else:
            return f"Unknown job analysis section: {section}"
    
    def get_available_tones(self):
        """Get available writing tones."""
        return list(self.resume_guidelines.WRITING_GUIDELINES["tone"].keys())
    
    def get_available_industries(self):
        """Get available industries."""
        return list(self.resume_guidelines.INDUSTRY_GUIDELINES.keys())
    
    def get_available_experience_levels(self):
        """Get available experience levels."""
        return list(self.resume_guidelines.EXPERIENCE_GUIDELINES.keys())
    
    def get_action_verbs(self, limit=10):
        """Get action verbs for resume writing."""
        return self.resume_guidelines.WRITING_GUIDELINES["action_verbs"][:limit]
    
    def get_industry_keywords(self, industry):
        """Get keywords for a specific industry."""
        return self.resume_guidelines.INDUSTRY_GUIDELINES.get(industry, {}).get("keywords", [])
    
    def get_industry_focus_areas(self, industry):
        """Get focus areas for a specific industry."""
        return self.resume_guidelines.INDUSTRY_GUIDELINES.get(industry, {}).get("focus_areas", [])
    
    def get_experience_guidelines(self, experience_level):
        """Get guidelines for a specific experience level."""
        return self.resume_guidelines.EXPERIENCE_GUIDELINES.get(experience_level, {})
    
    def validate_tone(self, tone):
        """Validate if a tone is supported."""
        return tone in self.get_available_tones()
    
    def validate_industry(self, industry):
        """Validate if an industry is supported."""
        return industry in self.get_available_industries()
    
    def validate_experience_level(self, experience_level):
        """Validate if an experience level is supported."""
        return experience_level in self.get_available_experience_levels()
    
    def get_customization_options(self):
        """Get all available customization options."""
        return {
            "tones": self.get_available_tones(),
            "industries": self.get_available_industries(),
            "experience_levels": self.get_available_experience_levels(),
            "action_verbs": self.get_action_verbs(),
            "achievement_patterns": self.resume_guidelines.WRITING_GUIDELINES["achievement_patterns"]
        }
    
    def get_guidelines_summary(self):
        """Get a summary of all available guidelines."""
        return {
            "resume_guidelines": {
                "writing_guidelines": list(self.resume_guidelines.WRITING_GUIDELINES.keys()),
                "industry_guidelines": list(self.resume_guidelines.INDUSTRY_GUIDELINES.keys()),
                "experience_guidelines": list(self.resume_guidelines.EXPERIENCE_GUIDELINES.keys())
            },
            "cover_letter_guidelines": {
                "writing_guidelines": list(self.cover_letter_guidelines.WRITING_GUIDELINES.keys()),
                "industry_guidelines": list(self.cover_letter_guidelines.INDUSTRY_GUIDELINES.keys()),
                "experience_guidelines": list(self.cover_letter_guidelines.EXPERIENCE_GUIDELINES.keys())
            },
            "job_analysis_guidelines": {
                "analysis_categories": list(self.job_analysis_guidelines.ANALYSIS_CATEGORIES.keys()),
                "industry_patterns": list(self.job_analysis_guidelines.INDUSTRY_PATTERNS.keys()),
                "experience_levels": list(self.job_analysis_guidelines.EXPERIENCE_LEVELS.keys()),
                "skill_categories": list(self.job_analysis_guidelines.SKILL_CATEGORIES.keys())
            }
        }
    
    def get_ultimate_prompt(self, profile_data, job_data):
        """
        Return the ultimate resume & cover letter prompt, rendered with Jinja2 using the provided profile and job data.
        """
        template = jinja2.Template(ULTIMATE_PROMPT)
        # Merge both dicts for context
        context = {**profile_data, **job_data}
        return template.render(**context)

    def get_batch_resume_sections_prompt(self, profile_data, job_description, job_analysis, tone, focus_areas, experience_level, industry):
        """Return a prompt to generate all three sections in one call."""
        return f"""
You are a professional resume writer. Generate the following three sections for a resume:
1. PROFESSIONAL SUMMARY
2. SKILLS
3. WORK EXPERIENCE

Use the following information:
PROFILE: {profile_data}
JOB DESCRIPTION: {job_description}
JOB ANALYSIS: {job_analysis}
TONE: {tone}
FOCUS AREAS: {focus_areas}
EXPERIENCE LEVEL: {experience_level}
INDUSTRY: {industry}

Return the result as a JSON object with keys: summary, skills, experience.
"""

    def fill_section_prompt(self, prompt, section, profile_data, job_description, job_analysis, tone, focus_areas, experience_level, industry):
        """Fill a section prompt with all required data."""
        return f"""
{prompt}
PROFILE: {profile_data}
JOB DESCRIPTION: {job_description}
JOB ANALYSIS: {job_analysis}
TONE: {tone}
FOCUS AREAS: {focus_areas}
EXPERIENCE LEVEL: {experience_level}
INDUSTRY: {industry}
"""

    def get_batch_resume_and_cover_letter_prompt(self, profile_data, job_description, job_analysis, tone, focus_areas, experience_level, industry):
        """Return a prompt to generate resume sections and cover letter in one call."""
        return f"""
You are a professional resume and cover letter writer. Generate the following for a job application:
1. PROFESSIONAL SUMMARY (resume)
2. SKILLS (resume)
3. WORK EXPERIENCE (resume)
4. COVER LETTER

Use the following information:
PROFILE: {profile_data}
JOB DESCRIPTION: {job_description}
JOB ANALYSIS: {job_analysis}
TONE: {tone}
FOCUS AREAS: {focus_areas}
EXPERIENCE LEVEL: {experience_level}
INDUSTRY: {industry}

Return the result as a JSON object with keys: summary, skills, experience, cover_letter.
"""

    def fill_cover_letter_prompt(self, prompt, profile_data, job_description, job_analysis, tone, focus_areas, experience_level):
        """Fill a cover letter prompt with all required data."""
        return f"""
{prompt}
PROFILE: {profile_data}
JOB DESCRIPTION: {job_description}
JOB ANALYSIS: {job_analysis}
TONE: {tone}
FOCUS AREAS: {focus_areas}
EXPERIENCE LEVEL: {experience_level}
""" 