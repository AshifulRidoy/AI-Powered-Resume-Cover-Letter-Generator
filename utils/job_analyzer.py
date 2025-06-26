import re
from typing import Dict, List, Any
from prompts.prompt_manager import PromptManager

class JobAnalyzer:
    """Analyzes job descriptions to extract key requirements and information using predefined guidelines."""
    
    def __init__(self):
        self.prompt_manager = PromptManager()
        
        # Keep existing patterns for backward compatibility
        self.skill_patterns = [
            r'\b(?:Python|Java|JavaScript|React|Angular|Vue|Node\.js|SQL|MongoDB|AWS|Azure|Docker|Kubernetes|Git|Agile|Scrum)\b',
            r'\b(?:Machine Learning|AI|Data Science|Analytics|Business Intelligence|ETL|API|REST|GraphQL|Microservices)\b',
            r'\b(?:Project Management|Leadership|Communication|Problem Solving|Teamwork|Collaboration|Innovation)\b',
            r'\b(?:Bachelor|Master|PhD|Degree|Certification|Experience|Years)\b'
        ]
        
        self.requirement_patterns = [
            r'(?:required|requirement|must have|should have|qualifications?|requirements?)',
            r'(?:responsibilities?|duties?|tasks?|role|position)',
            r'(?:preferred|nice to have|bonus|plus|advantage)'
        ]
    
    def analyze_job(self, job_description: str) -> Dict[str, Any]:
        """Analyze job description and extract key information using predefined guidelines."""
        if not job_description:
            return {}
        
        # Clean the text
        clean_text = self._clean_text(job_description)
        
        # Use AI-powered analysis with predefined guidelines
        try:
            ai_analysis = self._analyze_with_ai(job_description)
            if ai_analysis:
                return ai_analysis
        except Exception as e:
            print(f"AI analysis failed, falling back to pattern matching: {e}")
        
        # Fallback to pattern-based analysis
        return self._analyze_with_patterns(clean_text)
    
    def _analyze_with_ai(self, job_description: str) -> Dict[str, Any]:
        """Analyze job description using AI with predefined guidelines."""
        # This would be implemented when we have an AI provider
        # For now, return None to fall back to pattern matching
        return None
    
    def _analyze_with_patterns(self, text: str) -> Dict[str, Any]:
        """Analyze job description using pattern matching (fallback method)."""
        # Extract different components
        analysis = {
            "requirements": self._extract_requirements(text),
            "responsibilities": self._extract_responsibilities(text),
            "skills": self._extract_skills(text),
            "qualifications": self._extract_qualifications(text),
            "experience_level": self._determine_experience_level(text),
            "industry": self._identify_industry(text),
            "key_phrases": self._extract_key_phrases(text)
        }
        
        return analysis
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove special characters but keep important ones
        text = re.sub(r'[^\w\s\-\.\,\!\?\:\;\(\)]', '', text)
        return text.strip()
    
    def _extract_requirements(self, text: str) -> List[str]:
        """Extract required qualifications and skills."""
        requirements = []
        
        # Look for requirement sections
        requirement_sections = re.findall(
            r'(?:requirements?|qualifications?|must have|should have)[\s\:]*([^\.]+)',
            text,
            re.IGNORECASE
        )
        
        for section in requirement_sections:
            # Split by common delimiters
            items = re.split(r'[;,\n•]', section)
            for item in items:
                item = item.strip()
                if item and len(item) > 5:  # Filter out very short items
                    requirements.append(item)
        
        return requirements[:10]  # Limit to top 10
    
    def _extract_responsibilities(self, text: str) -> List[str]:
        """Extract job responsibilities and duties."""
        responsibilities = []
        
        # Look for responsibility sections
        responsibility_sections = re.findall(
            r'(?:responsibilities?|duties?|tasks?|role|position)[\s\:]*([^\.]+)',
            text,
            re.IGNORECASE
        )
        
        for section in responsibility_sections:
            # Split by common delimiters
            items = re.split(r'[;,\n•]', section)
            for item in items:
                item = item.strip()
                if item and len(item) > 5:
                    responsibilities.append(item)
        
        return responsibilities[:10]  # Limit to top 10
    
    def _extract_skills(self, text: str) -> List[str]:
        """Extract technical and soft skills."""
        skills = set()
        
        # Get skills from predefined guidelines
        all_skills = []
        for category_skills in self.prompt_manager.job_analysis_guidelines.SKILL_CATEGORIES.values():
            all_skills.extend(category_skills)
        
        # Check for skills in text
        for skill in all_skills:
            if re.search(rf'\b{re.escape(skill)}\b', text, re.IGNORECASE):
                skills.add(skill)
        
        return list(skills)
    
    def _extract_qualifications(self, text: str) -> List[str]:
        """Extract educational and experience qualifications."""
        qualifications = []
        
        # Look for education requirements
        education_patterns = [
            r'(?:Bachelor|Master|PhD|Degree|Diploma|Certificate)[\s\w]*',
            r'(?:\d+[\s\-]*years?[\s\-]*of[\s\-]*experience)',
            r'(?:experience[\s\-]*in[\s\-]*[\w\s]+)'
        ]
        
        for pattern in education_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            qualifications.extend(matches)
        
        return qualifications[:5]  # Limit to top 5
    
    def _determine_experience_level(self, text: str) -> str:
        """Determine the experience level required using predefined guidelines."""
        text_lower = text.lower()
        
        # Use predefined experience level patterns
        for level, data in self.prompt_manager.job_analysis_guidelines.EXPERIENCE_LEVELS.items():
            for keyword in data["keywords"]:
                if re.search(rf'\b{re.escape(keyword)}\b', text_lower):
                    return level.replace("_", " ").title()
        
        return "Mid Level"  # Default
    
    def _identify_industry(self, text: str) -> str:
        """Identify the industry or domain using predefined guidelines."""
        text_lower = text.lower()
        
        # Use predefined industry patterns
        for industry, data in self.prompt_manager.job_analysis_guidelines.INDUSTRY_PATTERNS.items():
            for keyword in data["keywords"]:
                if keyword in text_lower:
                    return industry.title()
        
        return "General"
    
    def _extract_key_phrases(self, text: str) -> List[str]:
        """Extract key phrases that might be important."""
        key_phrases = []
        
        # Look for phrases in quotes or with emphasis
        quoted_phrases = re.findall(r'"([^"]+)"', text)
        key_phrases.extend(quoted_phrases)
        
        # Look for bullet points or list items
        bullet_points = re.findall(r'•\s*([^•\n]+)', text)
        key_phrases.extend(bullet_points)
        
        # Look for capitalized phrases (might be important terms)
        capitalized_phrases = re.findall(r'\b[A-Z][A-Z\s]{3,}\b', text)
        key_phrases.extend(capitalized_phrases[:5])  # Limit to avoid noise
        
        return key_phrases[:10]  # Limit to top 10
    
    def get_analysis_guidelines(self) -> Dict[str, Any]:
        """Get analysis guidelines from predefined system."""
        return {
            "categories": self.prompt_manager.job_analysis_guidelines.ANALYSIS_CATEGORIES,
            "industries": self.prompt_manager.job_analysis_guidelines.INDUSTRY_PATTERNS,
            "experience_levels": self.prompt_manager.job_analysis_guidelines.EXPERIENCE_LEVELS,
            "skill_categories": self.prompt_manager.job_analysis_guidelines.SKILL_CATEGORIES
        }
    
    def get_available_industries(self) -> List[str]:
        """Get available industries from predefined guidelines."""
        return list(self.prompt_manager.job_analysis_guidelines.INDUSTRY_PATTERNS.keys())
    
    def get_available_experience_levels(self) -> List[str]:
        """Get available experience levels from predefined guidelines."""
        return list(self.prompt_manager.job_analysis_guidelines.EXPERIENCE_LEVELS.keys())
    
    def get_skill_categories(self) -> Dict[str, List[str]]:
        """Get skill categories from predefined guidelines."""
        return self.prompt_manager.job_analysis_guidelines.SKILL_CATEGORIES 