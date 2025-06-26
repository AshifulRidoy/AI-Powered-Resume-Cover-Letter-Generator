# Prompt System Documentation

## Overview

The prompt system transforms your Resume Automation System into a **custom model** with predefined guidelines, consistent outputs, and professional standards. This system ensures that every resume and cover letter generated follows industry best practices and maintains high quality.

## How It Works Like a Custom Model

### 1. **Predefined Guidelines**
Instead of generic AI responses, the system uses carefully crafted guidelines for:
- **Writing Tones**: Professional, Enthusiastic, Conservative, Innovative
- **Industry Focus**: Technology, Finance, Healthcare, Marketing, Sales
- **Experience Levels**: Entry Level, Mid Level, Senior Level, Executive
- **Skill Categories**: Technical, Soft Skills, Business Skills

### 2. **Consistent Prompts**
Every generation uses structured prompts that include:
- Industry-specific keywords and focus areas
- Experience-level appropriate language
- Professional writing guidelines
- Quantification patterns
- Achievement frameworks

### 3. **Quality Assurance**
The system ensures:
- Consistent formatting and structure
- Professional language and tone
- Industry-appropriate terminology
- Quantified achievements where possible
- Relevant skill highlighting

## System Architecture

```
prompts/
├── __init__.py
├── prompt_manager.py          # Main coordinator
├── resume_guidelines.py       # Resume-specific guidelines
├── cover_letter_guidelines.py # Cover letter guidelines
├── job_analysis_guidelines.py # Job analysis guidelines
└── README.md                  # This documentation
```

## Key Components

### 1. PromptManager
The central coordinator that manages all guidelines and prompts.

**Key Methods:**
- `get_resume_prompt()` - Generate resume prompts
- `get_cover_letter_prompt()` - Generate cover letter prompts
- `get_job_analysis_prompt()` - Generate job analysis prompts
- `get_customization_options()` - Get available options
- `validate_tone()`, `validate_industry()`, etc. - Input validation

### 2. ResumeGuidelines
Predefined guidelines for resume generation.

**Features:**
- **Writing Guidelines**: Tone, action verbs, achievement patterns
- **Industry Guidelines**: Technology, Finance, Healthcare, Marketing, Sales
- **Experience Guidelines**: Entry, Mid, Senior, Executive levels
- **Quantification Patterns**: Standard achievement formats

### 3. CoverLetterGuidelines
Predefined guidelines for cover letter generation.

**Features:**
- **Writing Guidelines**: Tone, opening/closing phrases, enthusiasm indicators
- **Industry Guidelines**: Industry-specific focus areas and keywords
- **Experience Guidelines**: Level-appropriate content structure
- **Professional Formatting**: Business letter standards

### 4. JobAnalysisGuidelines
Predefined guidelines for job description analysis.

**Features:**
- **Analysis Categories**: Requirements, Responsibilities, Skills, Qualifications
- **Industry Patterns**: Industry identification and classification
- **Experience Levels**: Seniority level detection
- **Skill Categories**: Technical, Soft, Business skill classification

## Available Customization Options

### Writing Tones
- **Professional**: Formal, business-appropriate language
- **Enthusiastic**: Dynamic, passionate, energetic
- **Conservative**: Traditional, formal, stability-focused
- **Innovative**: Creative, forward-thinking, modern

### Industries
- **Technology**: Software, development, innovation focus
- **Finance**: Analytical, risk management, compliance
- **Healthcare**: Patient care, clinical expertise, safety
- **Marketing**: Campaign performance, brand awareness, ROI
- **Sales**: Revenue generation, client relationships, growth

### Experience Levels
- **Entry Level**: Education focus, potential, enthusiasm
- **Mid Level**: Proven track record, specific achievements
- **Senior Level**: Leadership, strategic impact, team management
- **Executive**: Strategic leadership, business transformation

## Usage Examples

### Basic Resume Generation
```python
from prompts.prompt_manager import PromptManager

pm = PromptManager()
prompt = pm.get_resume_prompt(
    profile_data=profile_data,
    job_description=job_description,
    job_analysis=job_analysis,
    tone="professional",
    experience_level="mid_level",
    industry="technology"
)
```

### Cover Letter Generation
```python
prompt = pm.get_cover_letter_prompt(
    profile_data=profile_data,
    job_description=job_description,
    company_name="Google",
    position_title="Software Engineer",
    tone="enthusiastic",
    experience_level="mid_level"
)
```

### Job Analysis
```python
prompt = pm.get_job_analysis_prompt(job_description)
```

## Benefits of This System

### 1. **Consistency**
- Every output follows the same professional standards
- Consistent formatting and structure
- Uniform language and tone

### 2. **Quality**
- Industry-specific best practices
- Professional writing guidelines
- Quantified achievements where appropriate

### 3. **Customization**
- Multiple tone options
- Industry-specific focus
- Experience-level appropriate content

### 4. **Maintainability**
- Centralized guidelines
- Easy to update and extend
- Version-controlled prompts

### 5. **Scalability**
- Easy to add new industries
- Simple to extend guidelines
- Modular architecture

## Adding New Guidelines

### Adding a New Industry
1. Update `INDUSTRY_GUIDELINES` in both resume and cover letter guidelines
2. Add industry patterns to job analysis guidelines
3. Update the prompt manager validation methods

### Adding a New Tone
1. Add tone description to `WRITING_GUIDELINES["tone"]`
2. Update validation methods in prompt manager
3. Test with sample content

### Adding New Experience Levels
1. Update `EXPERIENCE_GUIDELINES` in all guideline files
2. Add appropriate keywords and patterns
3. Update validation methods

## Integration with Existing System

The prompt system seamlessly integrates with your existing utility classes:

- **ResumeGenerator**: Now uses predefined prompts
- **CoverLetterGenerator**: Uses structured guidelines
- **JobAnalyzer**: Enhanced with industry patterns

All existing functionality is preserved while adding the custom model capabilities.

## Best Practices

### 1. **Use Appropriate Tones**
- Professional for corporate roles
- Enthusiastic for startups and creative roles
- Conservative for traditional industries
- Innovative for tech and forward-thinking companies

### 2. **Match Industry Focus**
- Use industry-specific keywords
- Focus on relevant metrics
- Highlight industry-appropriate achievements

### 3. **Consider Experience Level**
- Entry level: Focus on potential and education
- Mid level: Emphasize proven track record
- Senior level: Highlight leadership and strategy
- Executive: Focus on business impact and vision

### 4. **Validate Inputs**
- Always validate tone, industry, and experience level
- Use the provided validation methods
- Provide fallback options for invalid inputs

## Future Enhancements

### Planned Features
1. **Multi-language Support**: Guidelines for different languages
2. **Regional Variations**: Country-specific formatting and standards
3. **Role-specific Guidelines**: Specialized prompts for different job types
4. **A/B Testing**: Compare different prompt variations
5. **User Feedback Integration**: Learn from user preferences

### Extensibility
The system is designed to be easily extensible:
- Add new guideline categories
- Create custom prompt templates
- Integrate with external style guides
- Support for custom branding

## Conclusion

This prompt system transforms your Resume Automation System into a professional, consistent, and high-quality custom model. It ensures that every generated document meets industry standards while providing the flexibility to customize for different roles, industries, and experience levels.

The system maintains the simplicity of use while providing the sophistication of a custom-trained model, making it perfect for professional resume and cover letter generation. 