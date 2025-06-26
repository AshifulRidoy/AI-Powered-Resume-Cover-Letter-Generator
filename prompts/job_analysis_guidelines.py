"""
Job Analysis Guidelines and Prompts
This module contains predefined guidelines and prompts for consistent, accurate job analysis.
"""

class JobAnalysisGuidelines:
    """Predefined guidelines for job analysis."""
    
    # Analysis categories and their importance
    ANALYSIS_CATEGORIES = {
        "requirements": {
            "priority": "high",
            "description": "Must-have qualifications and skills",
            "keywords": ["required", "must have", "qualifications", "requirements", "essential"],
            "extraction_method": "direct_match"
        },
        "responsibilities": {
            "priority": "high", 
            "description": "Job duties and day-to-day tasks",
            "keywords": ["responsibilities", "duties", "tasks", "role", "position", "will"],
            "extraction_method": "context_analysis"
        },
        "skills": {
            "priority": "high",
            "description": "Technical and soft skills needed",
            "keywords": ["skills", "proficient", "experience with", "knowledge of", "familiarity"],
            "extraction_method": "keyword_extraction"
        },
        "qualifications": {
            "priority": "medium",
            "description": "Educational and experience requirements",
            "keywords": ["degree", "bachelor", "master", "phd", "years of experience", "certification"],
            "extraction_method": "pattern_matching"
        },
        "experience_level": {
            "priority": "medium",
            "description": "Seniority level required",
            "keywords": ["entry level", "junior", "senior", "lead", "principal", "executive"],
            "extraction_method": "classification"
        },
        "industry": {
            "priority": "medium",
            "description": "Industry or domain focus",
            "keywords": ["technology", "finance", "healthcare", "marketing", "sales", "consulting"],
            "extraction_method": "keyword_classification"
        }
    }
    
    # Industry classification patterns
    INDUSTRY_PATTERNS = {
        "technology": {
            "keywords": ["software", "tech", "it", "development", "programming", "coding", "engineering"],
            "companies": ["Google", "Microsoft", "Apple", "Amazon", "Meta", "Netflix"],
            "skills": ["Python", "Java", "JavaScript", "React", "AWS", "Docker"]
        },
        "finance": {
            "keywords": ["finance", "banking", "investment", "trading", "fintech", "financial"],
            "companies": ["Goldman Sachs", "JP Morgan", "Morgan Stanley", "BlackRock"],
            "skills": ["Financial modeling", "Excel", "Bloomberg", "Risk management"]
        },
        "healthcare": {
            "keywords": ["healthcare", "medical", "pharmaceutical", "biotech", "clinical"],
            "companies": ["Johnson & Johnson", "Pfizer", "Merck", "UnitedHealth"],
            "skills": ["Patient care", "Clinical protocols", "HIPAA", "Medical terminology"]
        },
        "marketing": {
            "keywords": ["marketing", "advertising", "brand", "digital marketing", "campaign"],
            "companies": ["WPP", "Omnicom", "Publicis", "Interpublic"],
            "skills": ["SEO", "Social media", "Analytics", "Brand management"]
        },
        "sales": {
            "keywords": ["sales", "business development", "account management", "revenue"],
            "companies": ["Salesforce", "Oracle", "SAP", "Microsoft"],
            "skills": ["CRM", "Lead generation", "Pipeline management", "Negotiation"]
        },
        "consulting": {
            "keywords": ["consulting", "advisory", "strategy", "management consulting"],
            "companies": ["McKinsey", "BCG", "Bain", "Deloitte", "PwC"],
            "skills": ["Strategy", "Analysis", "Problem solving", "Client management"]
        }
    }
    
    # Experience level classification
    EXPERIENCE_LEVELS = {
        "entry_level": {
            "keywords": ["entry level", "junior", "0-2 years", "fresh graduate", "new grad", "associate"],
            "requirements": ["Bachelor's degree", "internship", "basic skills"],
            "responsibilities": ["learning", "support", "assist", "entry-level tasks"]
        },
        "mid_level": {
            "keywords": ["mid-level", "intermediate", "3-5 years", "experienced", "specialist"],
            "requirements": ["3+ years experience", "proven track record", "specialized skills"],
            "responsibilities": ["independent work", "project management", "mentoring"]
        },
        "senior_level": {
            "keywords": ["senior", "lead", "principal", "5+ years", "experienced professional"],
            "requirements": ["5+ years experience", "leadership experience", "expert skills"],
            "responsibilities": ["leadership", "strategy", "mentoring", "decision making"]
        },
        "executive": {
            "keywords": ["executive", "director", "manager", "head of", "vp", "cto", "ceo"],
            "requirements": ["10+ years experience", "executive experience", "strategic thinking"],
            "responsibilities": ["strategy", "leadership", "business decisions", "team management"]
        }
    }
    
    # Skill categorization
    SKILL_CATEGORIES = {
        "technical_skills": [
            "Python", "Java", "JavaScript", "React", "Angular", "Vue", "Node.js", "SQL", "MongoDB",
            "AWS", "Azure", "Docker", "Kubernetes", "Git", "Machine Learning", "AI", "Data Science"
        ],
        "soft_skills": [
            "Leadership", "Communication", "Problem Solving", "Teamwork", "Collaboration",
            "Project Management", "Agile", "Scrum", "Innovation", "Creativity", "Analytical"
        ],
        "business_skills": [
            "Strategy", "Analysis", "Financial modeling", "Risk management", "Compliance",
            "Marketing", "Sales", "Customer service", "Operations", "Supply chain"
        ]
    }

class JobAnalysisPrompts:
    """Predefined prompts for job analysis."""
    
    @staticmethod
    def get_main_analysis_prompt(job_description):
        """Generate the main job analysis prompt with predefined guidelines."""
        
        guidelines = JobAnalysisGuidelines()
        
        # Build industry patterns
        industry_patterns = "\n".join([
            f"- {industry}: {', '.join(data['keywords'])}" 
            for industry, data in guidelines.INDUSTRY_PATTERNS.items()
        ])
        
        # Build experience level patterns
        experience_patterns = "\n".join([
            f"- {level}: {', '.join(data['keywords'])}" 
            for level, data in guidelines.EXPERIENCE_LEVELS.items()
        ])
        
        # Build skill categories
        skill_categories = "\n".join([
            f"- {category}: {', '.join(skills[:5])}" 
            for category, skills in guidelines.SKILL_CATEGORIES.items()
        ])
        
        prompt = f"""
You are an expert job analyst with 10+ years of experience in analyzing job descriptions for recruitment and career development.

JOB DESCRIPTION TO ANALYZE:
{job_description}

ANALYSIS GUIDELINES:
Analyze the job description and extract the following information:

1. REQUIREMENTS (High Priority):
   - Must-have qualifications and skills
   - Look for keywords: required, must have, qualifications, essential
   - Extract specific requirements and qualifications

2. RESPONSIBILITIES (High Priority):
   - Job duties and day-to-day tasks
   - Look for keywords: responsibilities, duties, tasks, role, will
   - Extract specific responsibilities and expectations

3. SKILLS (High Priority):
   - Technical and soft skills needed
   - Look for keywords: skills, proficient, experience with, knowledge of
   - Categorize as technical, soft, or business skills

4. QUALIFICATIONS (Medium Priority):
   - Educational and experience requirements
   - Look for: degree requirements, years of experience, certifications
   - Extract specific qualification requirements

5. EXPERIENCE LEVEL (Medium Priority):
   - Determine seniority level required
   - Patterns to identify:
{experience_patterns}

6. INDUSTRY (Medium Priority):
   - Identify industry or domain focus
   - Industry patterns to look for:
{industry_patterns}

7. KEY PHRASES (Low Priority):
   - Important phrases or terms mentioned
   - Company-specific terminology
   - Industry jargon or buzzwords

SKILL CATEGORIZATION:
Categorize skills into:
{skill_categories}

ANALYSIS REQUIREMENTS:
1. Be thorough and comprehensive
2. Extract specific, actionable information
3. Prioritize information by importance
4. Use consistent formatting
5. Include relevant context
6. Identify patterns and themes

OUTPUT FORMAT:
Provide a structured analysis with:
- Requirements: [list of specific requirements]
- Responsibilities: [list of job duties]
- Skills: [categorized skills list]
- Qualifications: [educational/experience requirements]
- Experience Level: [entry/mid/senior/executive]
- Industry: [identified industry]
- Key Phrases: [important terms/phrases]

Generate a comprehensive, structured analysis of this job description.
"""
        
        return prompt
    
    @staticmethod
    def get_requirements_extraction_prompt(job_description):
        """Generate prompt for extracting specific requirements."""
        
        guidelines = JobAnalysisGuidelines()
        requirement_keywords = ", ".join(guidelines.ANALYSIS_CATEGORIES["requirements"]["keywords"])
        
        prompt = f"""
Extract specific requirements from this job description:

JOB DESCRIPTION:
{job_description}

EXTRACTION GUIDELINES:
Look for requirements using these keywords: {requirement_keywords}

REQUIREMENTS TO EXTRACT:
1. Educational requirements (degree, field of study)
2. Experience requirements (years, type of experience)
3. Technical requirements (specific skills, tools, technologies)
4. Certification requirements (professional certifications)
5. Soft skill requirements (communication, leadership, etc.)
6. Physical requirements (if any)
7. Travel requirements (if any)
8. Schedule requirements (if any)

EXTRACTION RULES:
- Focus on "must-have" requirements
- Be specific and detailed
- Include both explicit and implicit requirements
- Prioritize by importance
- Use clear, concise language

Generate a comprehensive list of requirements for this position.
"""
        
        return prompt
    
    @staticmethod
    def get_skills_extraction_prompt(job_description):
        """Generate prompt for extracting and categorizing skills."""
        
        guidelines = JobAnalysisGuidelines()
        
        # Build skill categories
        technical_skills = ", ".join(guidelines.SKILL_CATEGORIES["technical_skills"][:10])
        soft_skills = ", ".join(guidelines.SKILL_CATEGORIES["soft_skills"][:10])
        business_skills = ", ".join(guidelines.SKILL_CATEGORIES["business_skills"][:10])
        
        prompt = f"""
Extract and categorize skills from this job description:

JOB DESCRIPTION:
{job_description}

SKILL CATEGORIES TO IDENTIFY:

1. TECHNICAL SKILLS:
   Look for: {technical_skills}
   Also include: programming languages, tools, platforms, technologies

2. SOFT SKILLS:
   Look for: {soft_skills}
   Also include: interpersonal skills, communication, leadership

3. BUSINESS SKILLS:
   Look for: {business_skills}
   Also include: domain knowledge, industry expertise

EXTRACTION GUIDELINES:
- Identify both explicit and implicit skill requirements
- Look for skill levels (basic, intermediate, advanced, expert)
- Include industry-specific skills
- Consider context and job responsibilities
- Prioritize skills by importance to the role

OUTPUT FORMAT:
Provide categorized skills with:
- Technical Skills: [list of technical skills]
- Soft Skills: [list of soft skills]  
- Business Skills: [list of business skills]
- Skill Levels: [basic/intermediate/advanced/expert where specified]

Generate a comprehensive skills analysis for this position.
"""
        
        return prompt
    
    @staticmethod
    def get_experience_level_prompt(job_description):
        """Generate prompt for determining experience level."""
        
        guidelines = JobAnalysisGuidelines()
        
        # Build experience level details
        experience_details = "\n".join([
            f"{level.upper()}:\n- Keywords: {', '.join(data['keywords'])}\n- Requirements: {', '.join(data['requirements'])}\n- Responsibilities: {', '.join(data['responsibilities'])}"
            for level, data in guidelines.EXPERIENCE_LEVELS.items()
        ])
        
        prompt = f"""
Determine the experience level required for this position:

JOB DESCRIPTION:
{job_description}

EXPERIENCE LEVEL CRITERIA:
{experience_details}

ANALYSIS GUIDELINES:
1. Look for explicit experience level indicators
2. Analyze years of experience requirements
3. Consider responsibility level and scope
4. Examine required qualifications
5. Assess leadership requirements
6. Consider reporting structure

CLASSIFICATION RULES:
- Entry Level: 0-2 years, learning focus, basic responsibilities
- Mid Level: 3-5 years, independent work, some leadership
- Senior Level: 5+ years, leadership, strategic thinking
- Executive: 10+ years, strategic leadership, business decisions

OUTPUT FORMAT:
Provide:
- Experience Level: [entry/mid/senior/executive]
- Confidence: [high/medium/low]
- Reasoning: [explanation of classification]
- Key Indicators: [specific evidence from job description]

Generate a detailed experience level analysis for this position.
"""
        
        return prompt
    
    @staticmethod
    def get_industry_identification_prompt(job_description):
        """Generate prompt for identifying industry."""
        
        guidelines = JobAnalysisGuidelines()
        
        # Build industry patterns
        industry_patterns = "\n".join([
            f"{industry.upper()}:\n- Keywords: {', '.join(data['keywords'])}\n- Companies: {', '.join(data['companies'])}\n- Skills: {', '.join(data['skills'])}"
            for industry, data in guidelines.INDUSTRY_PATTERNS.items()
        ])
        
        prompt = f"""
Identify the industry or domain focus for this position:

JOB DESCRIPTION:
{job_description}

INDUSTRY PATTERNS TO LOOK FOR:
{industry_patterns}

IDENTIFICATION GUIDELINES:
1. Look for industry-specific keywords
2. Identify company type or sector
3. Consider required skills and technologies
4. Analyze job responsibilities context
5. Look for industry-specific terminology
6. Consider target market or customers

ANALYSIS REQUIREMENTS:
- Be specific about industry identification
- Consider sub-industries or specialties
- Look for multiple industry indicators
- Consider company context if provided
- Identify primary and secondary industries

OUTPUT FORMAT:
Provide:
- Primary Industry: [main industry]
- Secondary Industry: [sub-industry if applicable]
- Confidence: [high/medium/low]
- Key Indicators: [specific evidence from job description]
- Industry Context: [additional industry-specific details]

Generate a detailed industry analysis for this position.
"""
        
        return prompt 