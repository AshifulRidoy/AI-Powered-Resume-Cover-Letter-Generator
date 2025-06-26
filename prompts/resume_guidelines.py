"""
Resume Generation Guidelines and Prompts
This module contains predefined guidelines and prompts for consistent, professional resume generation.
"""

class ResumeGuidelines:
    """Predefined guidelines for resume generation."""
    
    # Professional writing guidelines
    WRITING_GUIDELINES = {
        "tone": {
            "professional": "Use formal, business-appropriate language. Avoid casual expressions and maintain a confident, authoritative tone.",
            "enthusiastic": "Show passion and excitement while remaining professional. Use dynamic language that conveys energy and motivation.",
            "conservative": "Use traditional, formal language. Focus on stability, reliability, and proven track record.",
            "innovative": "Emphasize creativity, adaptability, and forward-thinking. Use modern, dynamic language."
        },
        
        "action_verbs": [
            "Achieved", "Developed", "Implemented", "Managed", "Led", "Created", "Designed", "Built",
            "Optimized", "Streamlined", "Increased", "Reduced", "Generated", "Established", "Coordinated",
            "Facilitated", "Delivered", "Produced", "Executed", "Orchestrated", "Spearheaded", "Pioneered",
            "Revolutionized", "Transformed", "Enhanced", "Strengthened", "Expanded", "Launched", "Initiated"
        ],
        
        "quantification_phrases": [
            "resulting in", "leading to", "which increased", "that improved", "achieving", "delivering",
            "generating", "reducing", "saving", "improving", "enhancing", "streamlining", "optimizing"
        ],
        
        "achievement_patterns": [
            "Increased [metric] by [percentage] through [action]",
            "Reduced [cost/time] by [amount] by implementing [solution]",
            "Led team of [number] to deliver [result]",
            "Developed [solution] that improved [metric] by [amount]",
            "Managed [budget/project] worth [amount] resulting in [outcome]"
        ]
    }
    
    # Industry-specific guidelines
    INDUSTRY_GUIDELINES = {
        "technology": {
            "focus_areas": ["Technical skills", "Project delivery", "Innovation", "Problem-solving"],
            "keywords": ["Agile", "DevOps", "Cloud", "API", "Database", "Framework", "Architecture"],
            "metrics": ["Performance improvement", "User adoption", "System reliability", "Code quality"]
        },
        "finance": {
            "focus_areas": ["Analytical skills", "Risk management", "Financial modeling", "Compliance"],
            "keywords": ["ROI", "P&L", "Risk assessment", "Compliance", "Portfolio", "Trading"],
            "metrics": ["Revenue growth", "Cost reduction", "Risk mitigation", "Compliance rate"]
        },
        "healthcare": {
            "focus_areas": ["Patient care", "Clinical expertise", "Compliance", "Quality improvement"],
            "keywords": ["Patient outcomes", "Clinical protocols", "HIPAA", "Quality metrics"],
            "metrics": ["Patient satisfaction", "Clinical outcomes", "Compliance rate", "Efficiency"]
        },
        "marketing": {
            "focus_areas": ["Campaign performance", "Brand awareness", "Customer engagement", "ROI"],
            "keywords": ["Digital marketing", "SEO", "Social media", "Analytics", "Conversion"],
            "metrics": ["Conversion rate", "ROI", "Engagement rate", "Brand awareness"]
        },
        "sales": {
            "focus_areas": ["Revenue generation", "Client relationships", "Market expansion", "Target achievement"],
            "keywords": ["Sales pipeline", "CRM", "Lead generation", "Account management"],
            "metrics": ["Sales growth", "Quota achievement", "Client retention", "Market share"]
        }
    }
    
    # Experience level guidelines
    EXPERIENCE_GUIDELINES = {
        "entry_level": {
            "focus": "Education, internships, projects, and transferable skills",
            "emphasis": "Learning ability, enthusiasm, and potential",
            "structure": "Education first, then projects/internships, then skills"
        },
        "mid_level": {
            "focus": "Relevant work experience, achievements, and technical skills",
            "emphasis": "Proven track record and specific accomplishments",
            "structure": "Experience first, then skills, then education"
        },
        "senior_level": {
            "focus": "Leadership, strategic impact, and business results",
            "emphasis": "Team leadership, strategic thinking, and measurable impact",
            "structure": "Experience with leadership focus, then strategic achievements"
        },
        "executive": {
            "focus": "Strategic leadership, business transformation, and organizational impact",
            "emphasis": "Vision, strategy execution, and business growth",
            "structure": "Executive summary, strategic achievements, leadership experience"
        }
    }

class ResumePrompts:
    """Predefined prompts for resume generation."""
    
    @staticmethod
    def get_main_resume_prompt(profile_data, job_description, job_analysis, tone="professional", 
                              focus_areas=None, experience_level="mid_level", industry="general"):
        """Generate the main resume prompt with predefined guidelines."""
        
        guidelines = ResumeGuidelines()
        
        # Get relevant guidelines
        tone_guide = guidelines.WRITING_GUIDELINES["tone"].get(tone, guidelines.WRITING_GUIDELINES["tone"]["professional"])
        industry_guide = guidelines.INDUSTRY_GUIDELINES.get(industry, guidelines.INDUSTRY_GUIDELINES["technology"])
        experience_guide = guidelines.EXPERIENCE_GUIDELINES.get(experience_level, guidelines.EXPERIENCE_GUIDELINES["mid_level"])
        
        # Build action verbs list
        action_verbs = ", ".join(guidelines.WRITING_GUIDELINES["action_verbs"][:10])
        
        # Build achievement patterns
        achievement_patterns = "\n".join([f"- {pattern}" for pattern in guidelines.WRITING_GUIDELINES["achievement_patterns"]])
        
        prompt = f"""
You are an expert resume writer with 15+ years of experience in creating winning resumes for top companies.

CANDIDATE INFORMATION:
Name: {profile_data.get("name", "Candidate")}
Professional Summary: {profile_data.get("summary", "")}
Skills: {profile_data.get("skills", "")}
Work Experience: {profile_data.get("experience", "")}
Education: {profile_data.get("education", "")}
Projects: {profile_data.get("projects", "")}
Further Information: {profile_data.get("further_info", "")}

JOB DESCRIPTION:
{job_description}

JOB ANALYSIS:
Required Skills: {", ".join(job_analysis.get("skills", [])) if job_analysis else "Not specified"}
Experience Level: {job_analysis.get("experience_level", "Not specified") if job_analysis else "Not specified"}
Industry: {job_analysis.get("industry", "General") if job_analysis else "General"}

PROFESSIONAL GUIDELINES:
Tone: {tone_guide}
Industry Focus: {industry_guide["focus_areas"]}
Experience Level Focus: {experience_guide["focus"]}
Emphasis: {experience_guide["emphasis"]}

WRITING REQUIREMENTS:
1. Use these action verbs: {action_verbs}
2. Follow these achievement patterns:
{achievement_patterns}
3. Quantify achievements with specific numbers and percentages
4. Use industry-specific keywords: {", ".join(industry_guide["keywords"])}
5. Focus on relevant metrics: {", ".join(industry_guide["metrics"])}
6. Structure according to experience level: {experience_guide["structure"]}

RESUME STRUCTURE:
- Contact Information (name, email, phone, LinkedIn)
- Professional Summary (2-3 sentences highlighting key value proposition)
- Work Experience (reverse chronological, with quantifiable achievements)
- Skills (technical and soft skills, prioritized by job requirements)
- Education (degree, institution, graduation year)
- Projects (if relevant to the position)
- Additional Information (certifications, languages, interests, volunteer work, etc.)

FORMATTING REQUIREMENTS:
- Use bullet points for achievements
- Keep each bullet point to 1-2 lines
- Use consistent formatting throughout
- Ensure proper spacing and readability
- Use professional fonts and layout
- Include relevant additional information from Further Information section

Generate a complete, professional resume that follows these guidelines and maximizes the candidate's chances of getting an interview for this specific position.
"""
        
        return prompt
    
    @staticmethod
    def get_summary_prompt(profile_data, job_description, job_analysis, tone="professional"):
        """Generate a professional summary prompt."""
        
        guidelines = ResumeGuidelines()
        tone_guide = guidelines.WRITING_GUIDELINES["tone"].get(tone, guidelines.WRITING_GUIDELINES["tone"]["professional"])
        
        prompt = f"""
Write a compelling professional summary for a resume based on:

CANDIDATE BACKGROUND: {profile_data.get("summary", "")}
JOB DESCRIPTION: {job_description[:500]}...
REQUIRED SKILLS: {", ".join(job_analysis.get("skills", [])) if job_analysis else "Not specified"}

WRITING GUIDELINES:
- Tone: {tone_guide}
- Length: 2-3 sentences maximum
- Focus: Highlight key strengths relevant to the job
- Structure: Experience + Skills + Value Proposition
- Keywords: Include relevant industry keywords

REQUIREMENTS:
1. Start with years of experience and key expertise
2. Mention relevant skills that match job requirements
3. End with value proposition or career objective
4. Use professional, confident language
5. Avoid generic statements
6. Make it specific to this job opportunity

Generate a professional summary that immediately captures the hiring manager's attention.
"""
        
        return prompt
    
    @staticmethod
    def get_experience_prompt(profile_data, job_description, job_analysis, tone="professional"):
        """Generate work experience section prompt."""
        
        guidelines = ResumeGuidelines()
        action_verbs = ", ".join(guidelines.WRITING_GUIDELINES["action_verbs"][:15])
        achievement_patterns = "\n".join([f"- {pattern}" for pattern in guidelines.WRITING_GUIDELINES["achievement_patterns"]])
        
        prompt = f"""
Rewrite the work experience section for a resume based on:

ORIGINAL EXPERIENCE: {profile_data.get("experience", "")}
JOB DESCRIPTION: {job_description[:500]}...
REQUIRED SKILLS: {", ".join(job_analysis.get("skills", [])) if job_analysis else "Not specified"}

WRITING REQUIREMENTS:
1. Use these action verbs: {action_verbs}
2. Follow these achievement patterns:
{achievement_patterns}
3. Quantify achievements with specific numbers
4. Focus on relevant experience for this job
5. Use bullet points for each achievement
6. Keep each bullet to 1-2 lines maximum

ACHIEVEMENT GUIDELINES:
- Start each bullet with a strong action verb
- Include specific metrics (numbers, percentages, amounts)
- Focus on results and impact, not just responsibilities
- Match achievements to job requirements
- Use industry-specific terminology

Generate compelling work experience bullets that showcase relevant achievements and skills.
"""
        
        return prompt
    
    @staticmethod
    def get_skills_prompt(profile_data, job_description, job_analysis):
        """Generate skills section prompt."""
        
        prompt = f"""
Create a skills section for a resume based on:

CANDIDATE SKILLS: {profile_data.get("skills", "")}
JOB REQUIREMENTS: {", ".join(job_analysis.get("skills", [])) if job_analysis else "Not specified"}

SKILLS ORGANIZATION GUIDELINES:
1. Prioritize skills mentioned in the job description
2. Group skills by category:
   - Technical Skills (programming languages, tools, platforms)
   - Soft Skills (leadership, communication, problem-solving)
   - Industry-Specific Skills (domain knowledge, certifications)
3. List most relevant skills first
4. Include skill levels where appropriate (Expert, Advanced, Intermediate, Basic)
5. Add relevant certifications and training

REQUIREMENTS:
- Focus on skills that match job requirements
- Include both technical and soft skills
- Use industry-standard terminology
- Keep it concise and well-organized
- Highlight unique or specialized skills

Generate a well-organized skills section that demonstrates the candidate's qualifications for this position.
"""
        
        return prompt 