"""
Cover Letter Generation Guidelines and Prompts
This module contains predefined guidelines and prompts for consistent, professional cover letter generation.
"""

class CoverLetterGuidelines:
    """Predefined guidelines for cover letter generation."""
    
    # Professional writing guidelines
    WRITING_GUIDELINES = {
        "tone": {
            "professional": "Use formal, business-appropriate language. Show enthusiasm while maintaining professionalism and respect.",
            "enthusiastic": "Express genuine excitement and passion for the opportunity. Use dynamic, engaging language that shows energy.",
            "conservative": "Use traditional, formal language. Emphasize stability, reliability, and proven track record.",
            "innovative": "Show creativity and forward-thinking. Use modern, dynamic language that demonstrates adaptability."
        },
        
        "opening_phrases": [
            "I am writing to express my strong interest in",
            "I am excited to apply for the position of",
            "With great enthusiasm, I am submitting my application for",
            "I am writing to apply for the",
            "I am interested in the opportunity to join"
        ],
        
        "closing_phrases": [
            "I look forward to discussing how my background, skills, and enthusiasm can contribute to",
            "I would welcome the opportunity to discuss how my experience and skills align with",
            "I am excited about the possibility of contributing to",
            "I look forward to the opportunity to speak with you about how I can add value to",
            "Thank you for considering my application. I look forward to discussing this opportunity"
        ],
        
        "enthusiasm_indicators": [
            "excited", "passionate", "enthusiastic", "eager", "motivated", "inspired",
            "thrilled", "delighted", "pleased", "honored", "privileged"
        ]
    }
    
    # Industry-specific guidelines
    INDUSTRY_GUIDELINES = {
        "technology": {
            "focus_areas": ["Innovation", "Problem-solving", "Technical expertise", "Project delivery"],
            "keywords": ["Innovation", "Technology", "Development", "Solutions", "Efficiency"],
            "values": ["Innovation", "Collaboration", "Continuous learning", "Technical excellence"]
        },
        "finance": {
            "focus_areas": ["Analytical skills", "Risk management", "Financial expertise", "Compliance"],
            "keywords": ["Analysis", "Risk management", "Financial modeling", "Compliance", "ROI"],
            "values": ["Integrity", "Accuracy", "Risk management", "Compliance"]
        },
        "healthcare": {
            "focus_areas": ["Patient care", "Clinical expertise", "Quality improvement", "Compliance"],
            "keywords": ["Patient care", "Clinical excellence", "Quality", "Safety", "Compliance"],
            "values": ["Patient care", "Safety", "Quality", "Compassion"]
        },
        "marketing": {
            "focus_areas": ["Campaign performance", "Brand awareness", "Customer engagement", "ROI"],
            "keywords": ["Marketing", "Brand", "Engagement", "ROI", "Strategy"],
            "values": ["Creativity", "Results", "Customer focus", "Innovation"]
        },
        "sales": {
            "focus_areas": ["Revenue generation", "Client relationships", "Market expansion", "Target achievement"],
            "keywords": ["Sales", "Revenue", "Client relationships", "Growth", "Results"],
            "values": ["Results", "Customer focus", "Relationship building", "Growth"]
        }
    }
    
    # Experience level guidelines
    EXPERIENCE_GUIDELINES = {
        "entry_level": {
            "focus": "Education, potential, enthusiasm, and transferable skills",
            "emphasis": "Learning ability, adaptability, and eagerness to contribute",
            "structure": "Introduction → Why interested → Education/Skills → Closing"
        },
        "mid_level": {
            "focus": "Relevant experience, achievements, and technical skills",
            "emphasis": "Proven track record and specific accomplishments",
            "structure": "Introduction → Why interested → Relevant Experience → Closing"
        },
        "senior_level": {
            "focus": "Leadership, strategic impact, and business results",
            "emphasis": "Team leadership, strategic thinking, and measurable impact",
            "structure": "Introduction → Why interested → Leadership Experience → Strategic Impact → Closing"
        },
        "executive": {
            "focus": "Strategic leadership, business transformation, and organizational impact",
            "emphasis": "Vision, strategy execution, and business growth",
            "structure": "Introduction → Strategic Vision → Leadership Impact → Business Results → Closing"
        }
    }

class CoverLetterPrompts:
    """Predefined prompts for cover letter generation."""
    
    @staticmethod
    def get_main_cover_letter_prompt(profile_data, job_description, job_analysis, tone="professional",
                                   focus_areas=None, company_name="", position_title="", experience_level="mid_level"):
        """Generate the main cover letter prompt with predefined guidelines."""
        
        guidelines = CoverLetterGuidelines()
        
        # Get relevant guidelines
        tone_guide = guidelines.WRITING_GUIDELINES["tone"].get(tone, guidelines.WRITING_GUIDELINES["tone"]["professional"])
        experience_guide = guidelines.EXPERIENCE_GUIDELINES.get(experience_level, guidelines.EXPERIENCE_GUIDELINES["mid_level"])
        
        # Determine industry
        industry = job_analysis.get("industry", "general") if job_analysis else "general"
        industry_guide = guidelines.INDUSTRY_GUIDELINES.get(industry, guidelines.INDUSTRY_GUIDELINES["technology"])
        
        # Build opening and closing phrases
        opening_phrases = ", ".join(guidelines.WRITING_GUIDELINES["opening_phrases"][:3])
        closing_phrases = ", ".join(guidelines.WRITING_GUIDELINES["closing_phrases"][:3])
        
        prompt = f"""
You are an expert cover letter writer with 15+ years of experience in creating compelling cover letters for top companies.

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

COMPANY & POSITION:
Company: {company_name if company_name else "the company"}
Position: {position_title if position_title else "the position"}

PROFESSIONAL GUIDELINES:
Tone: {tone_guide}
Industry Focus: {industry_guide["focus_areas"]}
Industry Keywords: {", ".join(industry_guide["keywords"])}
Industry Values: {", ".join(industry_guide["values"])}
Experience Level Focus: {experience_guide["focus"]}
Emphasis: {experience_guide["emphasis"]}
Structure: {experience_guide["structure"]}

WRITING REQUIREMENTS:
1. Use these opening phrases: {opening_phrases}
2. Use these closing phrases: {closing_phrases}
3. Show enthusiasm using words like: {", ".join(guidelines.WRITING_GUIDELINES["enthusiasm_indicators"][:5])}
4. Match candidate's experience with job requirements
5. Explain why the candidate is interested in this specific company/role
6. Highlight relevant achievements and skills
7. Use industry-specific keywords and values
8. Keep it to 3-4 paragraphs maximum
9. Include relevant additional information from Further Information section if applicable

COVER LETTER STRUCTURE:
Paragraph 1 (Introduction):
- Mention the specific position and company
- Show enthusiasm for the opportunity
- Reference how you found the position if relevant

Paragraph 2 (Why Interested):
- Explain why you're interested in this company/role
- Connect your career goals with the opportunity
- Mention specific aspects that appeal to you

Paragraph 3 (Why Qualified):
- Highlight relevant experience and skills
- Match your background to job requirements
- Mention specific achievements if relevant
- Show how you can add value
- Include relevant certifications, languages, or other qualifications if mentioned in Further Information

Paragraph 4 (Closing):
- Express interest in discussing the opportunity further
- Mention availability for interview
- Thank them for considering your application
- Include a call to action

FORMATTING REQUIREMENTS:
- Professional business letter format
- Include date, recipient info, greeting, body, closing, signature
- Use clear, concise language
- Show enthusiasm but remain professional
- Use proper spacing and formatting

Generate a complete, compelling cover letter that follows these guidelines and maximizes the candidate's chances of getting an interview.
"""
        
        return prompt
    
    @staticmethod
    def get_introduction_prompt(profile_data, job_description, job_analysis, company_name="", position_title="", tone="professional"):
        """Generate cover letter introduction prompt."""
        
        guidelines = CoverLetterGuidelines()
        tone_guide = guidelines.WRITING_GUIDELINES["tone"].get(tone, guidelines.WRITING_GUIDELINES["tone"]["professional"])
        opening_phrases = ", ".join(guidelines.WRITING_GUIDELINES["opening_phrases"][:3])
        
        prompt = f"""
Write an engaging introduction paragraph for a cover letter based on:

CANDIDATE: {profile_data.get("name", "Candidate")}
POSITION: {position_title if position_title else "the position"}
COMPANY: {company_name if company_name else "the company"}
JOB DESCRIPTION: {job_description[:300]}...

WRITING GUIDELINES:
- Tone: {tone_guide}
- Use these opening phrases: {opening_phrases}
- Length: 2-3 sentences maximum
- Show enthusiasm for the opportunity

REQUIREMENTS:
1. Start with one of the suggested opening phrases
2. Mention the specific position and company
3. Show genuine enthusiasm for the opportunity
4. Reference how you found the position if relevant
5. Keep it concise and engaging
6. Set up the rest of the letter

Generate an introduction that immediately captures the hiring manager's attention and shows your enthusiasm.
"""
        
        return prompt
    
    @staticmethod
    def get_why_interested_prompt(profile_data, job_description, job_analysis, company_name="", position_title=""):
        """Generate why interested section prompt."""
        
        guidelines = CoverLetterGuidelines()
        
        # Determine industry
        industry = job_analysis.get("industry", "general") if job_analysis else "general"
        industry_guide = guidelines.INDUSTRY_GUIDELINES.get(industry, guidelines.INDUSTRY_GUIDELINES["technology"])
        
        prompt = f"""
Write a paragraph explaining why you're interested in this position and company based on:

CANDIDATE BACKGROUND: {profile_data.get("summary", "")}
POSITION: {position_title if position_title else "the position"}
COMPANY: {company_name if company_name else "the company"}
JOB DESCRIPTION: {job_description[:300]}...
INDUSTRY: {industry}
INDUSTRY VALUES: {", ".join(industry_guide["values"])}

WRITING REQUIREMENTS:
1. Show genuine interest in the company/role
2. Connect your career goals with the opportunity
3. Mention specific aspects that appeal to you
4. Reference industry values: {", ".join(industry_guide["values"])}
5. Keep it to 2-3 sentences
6. Use professional and enthusiastic tone

REQUIREMENTS:
- Explain what attracts you to this specific role
- Connect your interests with the company's mission/values
- Show you've done your research about the company
- Demonstrate alignment with industry values
- Keep it genuine and specific

Generate a paragraph that shows genuine interest and connects your goals with this opportunity.
"""
        
        return prompt
    
    @staticmethod
    def get_qualifications_prompt(profile_data, job_description, job_analysis, company_name="", position_title=""):
        """Generate qualifications section prompt."""
        
        guidelines = CoverLetterGuidelines()
        
        # Determine industry
        industry = job_analysis.get("industry", "general") if job_analysis else "general"
        industry_guide = guidelines.INDUSTRY_GUIDELINES.get(industry, guidelines.INDUSTRY_GUIDELINES["technology"])
        
        prompt = f"""
Write a paragraph explaining why you're qualified for this position based on:

CANDIDATE EXPERIENCE: {profile_data.get("experience", "")}
CANDIDATE SKILLS: {profile_data.get("skills", "")}
JOB REQUIREMENTS: {", ".join(job_analysis.get("requirements", [])) if job_analysis else "Not specified"}
REQUIRED SKILLS: {", ".join(job_analysis.get("skills", [])) if job_analysis else "Not specified"}
INDUSTRY FOCUS: {", ".join(industry_guide["focus_areas"])}
INDUSTRY KEYWORDS: {", ".join(industry_guide["keywords"])}

WRITING REQUIREMENTS:
1. Highlight relevant experience and skills
2. Match your background to job requirements
3. Mention specific achievements if relevant
4. Show how you can add value to the company
5. Use industry-specific keywords
6. Keep it to 2-3 sentences
7. Use specific examples when possible

REQUIREMENTS:
- Focus on experience that directly relates to the job
- Use industry-specific terminology
- Quantify achievements when possible
- Show how your skills match their needs
- Demonstrate value proposition
- Keep it concise and impactful

Generate a paragraph that clearly demonstrates your qualifications for this specific position.
"""
        
        return prompt
    
    @staticmethod
    def get_closing_prompt(profile_data, job_description, job_analysis, company_name="", position_title=""):
        """Generate cover letter closing prompt."""
        
        guidelines = CoverLetterGuidelines()
        closing_phrases = ", ".join(guidelines.WRITING_GUIDELINES["closing_phrases"][:3])
        
        prompt = f"""
Write a professional closing paragraph for a cover letter based on:

POSITION: {position_title if position_title else "the position"}
COMPANY: {company_name if company_name else "the company"}

WRITING GUIDELINES:
- Use these closing phrases: {closing_phrases}
- Length: 1-2 sentences maximum
- Professional and courteous tone

REQUIREMENTS:
1. Express interest in discussing the opportunity further
2. Mention availability for interview
3. Thank them for considering your application
4. Include a call to action
5. Use one of the suggested closing phrases
6. Keep it professional and enthusiastic

Generate a closing that leaves a positive impression and encourages them to contact you.
"""
        
        return prompt 