import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
import json
from datetime import datetime

# Import our modules
from ai_providers.ai_manager import AIManager
from utils.resume_generator import ResumeGenerator
from utils.cover_letter_generator import CoverLetterGenerator
from utils.job_analyzer import JobAnalyzer
from data.profile_manager import ProfileManager
from utils.pdf_parser import PDFParser

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Resume Automation System",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin: 1rem 0;
    }
    .warning-box {
        background-color: #fff3cd;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #ffc107;
        margin: 1rem 0;
    }
    .gemini-card {
        background: linear-gradient(135deg, #4285f4, #34a853);
        color: white;
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Initialize session state
    if 'profile_data' not in st.session_state:
        st.session_state.profile_data = {}
    if 'job_description' not in st.session_state:
        st.session_state.job_description = ""
    if 'generated_resume' not in st.session_state:
        st.session_state.generated_resume = None
    if 'generated_cover_letter' not in st.session_state:
        st.session_state.generated_cover_letter = None

    # Header
    st.markdown('<h1 class="main-header">📄 Resume & Cover Letter Automation</h1>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    with st.sidebar:
        st.markdown("## 🧭 Navigation")
        page = st.radio(
            "Choose a page:",
            ["🏠 Home", "👤 Profile Setup", "💼 Job Analysis", "📝 Generate Content", "⚙️ Settings"]
        )
        
        st.markdown("---")
        st.markdown("## 🤖 Custom Model System")
        
        # Show custom model features
        st.success("✅ Professional Guidelines Active")
        st.info("Industry-specific prompts")
        st.info("Experience-level customization")
        st.info("Multiple writing tones")
        
        st.markdown("---")
        st.markdown("## 🚀 Google Gemini Status")
        
        # Check Google Gemini status (without API call)
        ai_manager = AIManager()
        providers = ai_manager.get_available_providers()
        
        if "Google Gemini" in providers:
            gemini_status = providers["Google Gemini"]
            if gemini_status["available"]:
                st.success("✅ Google Gemini Ready")
                st.info("API Key configured")
                
                # Show quota information
                quota_info = ai_manager.get_quota_info()
                
                st.markdown("### 📊 Quota Usage")
                
                # Daily quota
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Daily Requests", 
                        f"{quota_info['daily_used']}/{quota_info['daily_limit']}",
                        f"{quota_info['daily_remaining']} remaining"
                    )
                with col2:
                    st.metric("Daily Reset", quota_info['daily_reset_in'])
                
                # Minute quota
                col1, col2 = st.columns(2)
                with col1:
                    st.metric(
                        "Minute Requests", 
                        f"{quota_info['minute_used']}/{quota_info['minute_limit']}",
                        f"{quota_info['minute_remaining']} remaining"
                    )
                with col2:
                    st.metric("Minute Reset", quota_info['minute_reset_in'])
                
                # Progress bars
                daily_progress = quota_info['daily_used'] / quota_info['daily_limit']
                minute_progress = quota_info['minute_used'] / quota_info['minute_limit']
                
                st.progress(daily_progress, text="Daily Usage")
                st.progress(minute_progress, text="Minute Usage")
                
                # Warning if approaching limits
                if quota_info['daily_remaining'] < 50:
                    st.warning(f"⚠️ Only {quota_info['daily_remaining']} daily requests remaining!")
                if quota_info['minute_remaining'] < 3:
                    st.warning(f"⚠️ Only {quota_info['minute_remaining']} minute requests remaining!")
                
            else:
                st.error("❌ Google Gemini Not Available")
                error_msg = gemini_status.get('error', 'Unknown error')
                st.info(f"Error: {error_msg}")
                
                # Show quota info even if provider is down
                quota_info = ai_manager.get_quota_info()
                if quota_info['last_quota_error']:
                    st.markdown("### 📊 Last Quota Error")
                    error_time = datetime.fromtimestamp(quota_info['last_quota_error']['timestamp'])
                    st.write(f"**Time:** {error_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    st.write(f"**Error:** {quota_info['last_quota_error']['error'][:100]}...")
        else:
            st.error("❌ Google Gemini Not Found")
            st.info("Add GOOGLE_API_KEY to .env file")

    # Main content based on selected page
    if page == "🏠 Home":
        show_home_page()
    elif page == "👤 Profile Setup":
        show_profile_setup()
    elif page == "💼 Job Analysis":
        show_job_analysis()
    elif page == "📝 Generate Content":
        show_generate_documents()
    elif page == "⚙️ Settings":
        show_settings()

def show_home_page():
    st.markdown('<h2 class="sub-header">Welcome to Resume Automation System</h2>', unsafe_allow_html=True)
    
    # Custom Model System highlight card
    st.markdown("""
    <div class="gemini-card">
        <h3>🤖 Custom Model System</h3>
        <p><strong>Professional Guidelines:</strong> Industry-specific prompts and standards</p>
        <p><strong>Consistent Quality:</strong> Every output follows best practices</p>
        <p><strong>Multiple Tones:</strong> Professional, Enthusiastic, Conservative, Innovative</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### 🚀 What This System Does
        
        This AI-powered system creates customized resume and cover letter **text content** using:
        
        - **🤖 Custom Model System** with predefined professional guidelines
        - **Industry-Specific Focus** (Technology, Finance, Healthcare, Marketing, Sales)
        - **Experience-Level Appropriate** content (Entry, Mid, Senior, Executive)
        - **Multiple Writing Tones** for different company cultures
        - **Smart Job Analysis** to extract key requirements
        
        ### 🎯 How It Works
        
        1. **Setup Your Profile**: Enter your personal information, experience, and skills
        2. **Analyze Job**: Paste a job description for AI analysis
        3. **Customize**: Choose tone, industry focus, and experience level
        4. **Generate**: Get professional text content ready to copy/paste
        
        ### 💰 Completely Free
        
        - **Google Gemini**: 15 requests/minute, 1500 requests/day
        - **No credit card required**
        - **No monthly fees**
        - **Professional results**
        """)
    
    with col2:
        st.markdown("### 📊 Quick Stats")
        st.metric("AI Provider", "Google Gemini")
        st.metric("Custom Model", "✅ Active")
        st.metric("Free Requests", "1500/day")
        st.metric("Cost", "Free")
        
        st.markdown("### 🎨 Features")
        st.markdown("""
        - 🤖 Custom Model System
        - 📝 Text Content Generation
        - 🏭 Industry-Specific Focus
        - 🎯 Experience-Level Customization
        - 📋 Copy/Paste Ready
        - 🌐 Web Interface
        """)
    
    # Quick start section
    st.markdown("---")
    st.markdown('<h3 class="sub-header">🚀 Quick Start</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 1. Get API Key")
        st.markdown("""
        **Google Gemini Setup:**
        1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
        2. Sign in with Google account
        3. Create API key
        4. Copy to `.env` file
        """)
    
    with col2:
        st.markdown("### 2. Setup Profile")
        if st.button("Go to Profile Setup", key="quick_profile"):
            st.session_state.page = "👤 Profile Setup"
    
    with col3:
        st.markdown("### 3. Generate Content")
        if st.button("Generate Content", key="quick_generate"):
            st.session_state.page = "📝 Generate Content"

def show_profile_setup():
    st.markdown('<h2 class="sub-header">👤 Profile Setup</h2>', unsafe_allow_html=True)
    
    profile_manager = ProfileManager()
    
    # Load existing profile if available
    if os.path.exists("data/profile.json"):
        with open("data/profile.json", "r") as f:
            st.session_state.profile_data = json.load(f)
    
    # Profile input method selection
    st.markdown("### 📋 Choose Profile Input Method")
    input_method = st.radio(
        "How would you like to set up your profile?",
        ["📄 Upload Resume (PDF)", "✏️ Manual Input", "📝 Use Existing Profile"]
    )
    
    if input_method == "📄 Upload Resume (PDF)":
        st.markdown("#### 📄 Upload Your Resume")
        st.markdown("Upload your current resume in PDF format. The system will extract your information and pre-fill the form.")
        
        uploaded_resume = st.file_uploader(
            "Choose your resume file",
            type=['pdf'],
            help="Upload your resume in PDF format"
        )
        
        if uploaded_resume is not None:
            with st.spinner("Extracting information from your resume..."):
                try:
                    # Use the PDF parser to extract information
                    pdf_parser = PDFParser()
                    extracted_data = pdf_parser.extract_from_pdf(uploaded_resume)
                    
                    st.success("📄 Resume uploaded and processed successfully!")
                    
                    # Show extracted information
                    st.markdown("#### 📋 Extracted Information Preview")
                    st.markdown("Review and edit the extracted information below:")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        name = st.text_input("Name", value=extracted_data.get("name", ""), key="extracted_name")
                        email = st.text_input("Email", value=extracted_data.get("email", ""), key="extracted_email")
                        phone = st.text_input("Phone", value=extracted_data.get("phone", ""), key="extracted_phone")
                    with col2:
                        location = st.text_input("Location", value=extracted_data.get("location", ""), key="extracted_location")
                        linkedin = st.text_input("LinkedIn", value=extracted_data.get("linkedin", ""), key="extracted_linkedin")
                        github = st.text_input("GitHub", value=extracted_data.get("github", ""), key="extracted_github")
                        website = st.text_input("Website", value=extracted_data.get("website", ""), key="extracted_website")
                    
                    summary = st.text_area("Summary", value=extracted_data.get("summary", ""), height=100, key="extracted_summary")
                    skills = st.text_area("Skills", value=extracted_data.get("skills", ""), height=100, key="extracted_skills")
                    experience = st.text_area("Experience", value=extracted_data.get("experience", ""), height=200, key="extracted_experience")
                    education = st.text_area("Education", value=extracted_data.get("education", ""), height=100, key="extracted_education")
                    projects = st.text_area("Projects", value=extracted_data.get("projects", ""), height=150, key="extracted_projects")
                    further_info = st.text_area("Further Info", value=extracted_data.get("further_info", ""), height=150, key="extracted_further_info")
                    
                    if st.button("✅ Save Extracted Information"):
                        # Save extracted information
                        profile_data = {
                            "name": name,
                            "email": email,
                            "phone": phone,
                            "location": location,
                            "linkedin": linkedin,
                            "github": github,
                            "website": website,
                            "summary": summary,
                            "skills": skills,
                            "experience": experience,
                            "education": education,
                            "projects": projects,
                            "further_info": further_info
                        }
                        
                        # Save profile
                        os.makedirs("data", exist_ok=True)
                        with open("data/profile.json", "w") as f:
                            json.dump(profile_data, f, indent=2)
                        
                        st.session_state.profile_data = profile_data
                        st.success("✅ Profile saved from uploaded resume!")
                        
                except Exception as e:
                    st.error(f"❌ Error processing resume: {str(e)}")
                    st.info("Please use manual input instead or check if your PDF is readable.")
    
    elif input_method == "✏️ Manual Input":
        st.markdown("#### ✏️ Manual Profile Input")
        st.markdown("Enter your information manually in the form below.")
        
        with st.form("profile_form"):
            st.markdown("### Personal Information")
            
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Full Name", value=st.session_state.profile_data.get("name", ""))
                email = st.text_input("Email", value=st.session_state.profile_data.get("email", ""))
                phone = st.text_input("Phone", value=st.session_state.profile_data.get("phone", ""))
                location = st.text_input("Location (City, State)", value=st.session_state.profile_data.get("location", ""))
            
            with col2:
                linkedin = st.text_input("LinkedIn URL", value=st.session_state.profile_data.get("linkedin", ""))
                github = st.text_input("GitHub URL", value=st.session_state.profile_data.get("github", ""))
                website = st.text_input("Personal Website", value=st.session_state.profile_data.get("website", ""))
            
            st.markdown("### Professional Summary")
            summary = st.text_area(
                "Professional Summary (2-3 sentences about your career goals and expertise)",
                value=st.session_state.profile_data.get("summary", ""),
                height=100
            )
            
            st.markdown("### Skills")
            skills = st.text_area(
                "Skills (comma-separated or one per line)",
                value=st.session_state.profile_data.get("skills", ""),
                height=100,
                help="Enter your technical and soft skills"
            )
            
            st.markdown("### Work Experience")
            experience = st.text_area(
                "Work Experience (detailed descriptions of your roles and achievements)",
                value=st.session_state.profile_data.get("experience", ""),
                height=200,
                help="Include job titles, companies, dates, and key achievements"
            )
            
            st.markdown("### Education")
            education = st.text_area(
                "Education (degrees, institutions, graduation dates)",
                value=st.session_state.profile_data.get("education", ""),
                height=100
            )
            
            st.markdown("### Projects")
            projects = st.text_area(
                "Projects (significant projects with descriptions and technologies used)",
                value=st.session_state.profile_data.get("projects", ""),
                height=150
            )
            
            st.markdown("### Further Information")
            further_info = st.text_area(
                "Further Information (additional details, certifications, languages, interests, or any other relevant information)",
                value=st.session_state.profile_data.get("further_info", ""),
                height=150,
                help="Include certifications, languages, interests, volunteer work, or any other information that might be relevant"
            )
            
            submitted = st.form_submit_button("Save Profile")
            
            if submitted:
                profile_data = {
                    "name": name,
                    "email": email,
                    "phone": phone,
                    "location": location,
                    "linkedin": linkedin,
                    "github": github,
                    "website": website,
                    "summary": summary,
                    "skills": skills,
                    "experience": experience,
                    "education": education,
                    "projects": projects,
                    "further_info": further_info
                }
                
                # Save profile
                os.makedirs("data", exist_ok=True)
                with open("data/profile.json", "w") as f:
                    json.dump(profile_data, f, indent=2)
                
                st.session_state.profile_data = profile_data
                st.success("✅ Profile saved successfully!")
    
    elif input_method == "📝 Use Existing Profile":
        if st.session_state.profile_data:
            st.markdown("#### 📝 Current Profile Information")
            st.markdown("Your existing profile is loaded. You can edit it below or use it as is.")
            
            # Display current profile
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Personal Information:**")
                st.write(f"**Name:** {st.session_state.profile_data.get('name', 'Not provided')}")
                st.write(f"**Email:** {st.session_state.profile_data.get('email', 'Not provided')}")
                st.write(f"**Phone:** {st.session_state.profile_data.get('phone', 'Not provided')}")
                st.write(f"**Location:** {st.session_state.profile_data.get('location', 'Not provided')}")
            
            with col2:
                st.markdown("**Professional Information:**")
                st.write(f"**LinkedIn:** {st.session_state.profile_data.get('linkedin', 'Not provided')}")
                st.write(f"**GitHub:** {st.session_state.profile_data.get('github', 'Not provided')}")
                st.write(f"**Website:** {st.session_state.profile_data.get('website', 'Not provided')}")
            
            st.markdown("**Summary:**")
            st.write(st.session_state.profile_data.get('summary', 'Not provided'))
            
            st.markdown("**Skills:**")
            st.write(st.session_state.profile_data.get('skills', 'Not provided'))
            
            st.markdown("**Experience:**")
            st.write(st.session_state.profile_data.get('experience', 'Not provided'))
            
            st.markdown("**Education:**")
            st.write(st.session_state.profile_data.get('education', 'Not provided'))
            
            st.markdown("**Projects:**")
            st.write(st.session_state.profile_data.get('projects', 'Not provided'))
            
            st.markdown("**Further Information:**")
            st.write(st.session_state.profile_data.get('further_info', 'Not provided'))
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("✅ Use This Profile"):
                    st.success("✅ Profile is ready to use!")
            with col2:
                if st.button("✏️ Edit Profile"):
                    st.session_state.edit_profile = True
                    st.rerun()
        else:
            st.warning("⚠️ No existing profile found. Please use one of the other options to create a profile.")
    
    # Show profile status
    if st.session_state.profile_data:
        st.markdown("---")
        st.markdown("### 📊 Profile Status")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.success("✅ Profile Loaded")
            st.write(f"Name: {st.session_state.profile_data.get('name', 'Not provided')}")
        
        with col2:
            st.info("📝 Ready for Generation")
            st.write("Profile can be used for resume and cover letter generation")
        
        with col3:
            if st.button("🗑️ Clear Profile"):
                st.session_state.profile_data = {}
                if os.path.exists("data/profile.json"):
                    os.remove("data/profile.json")
                st.success("✅ Profile cleared!")
                st.rerun()

def show_job_analysis():
    st.markdown('<h2 class="sub-header">💼 Job Analysis</h2>', unsafe_allow_html=True)
    
    # Job description input
    st.markdown("### 📋 Job Description")
    
    job_input_method = st.radio(
        "How would you like to input the job description?",
        ["📝 Paste Text", "📄 Upload File"]
    )
    
    if job_input_method == "📝 Paste Text":
        job_description = st.text_area(
            "Paste the job description here:",
            value=st.session_state.job_description,
            height=300,
            placeholder="Paste the complete job description including requirements, responsibilities, and qualifications..."
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload job description file (TXT, DOCX, PDF)",
            type=['txt', 'docx', 'pdf']
        )
        
        if uploaded_file is not None:
            # For now, we'll handle text files
            if uploaded_file.type == "text/plain":
                job_description = uploaded_file.read().decode("utf-8")
            else:
                st.warning("File format not supported yet. Please paste the text instead.")
                job_description = ""
        else:
            job_description = ""
    
    st.session_state.job_description = job_description
    
    # Analyze job description
    if job_description and st.button("🔍 Analyze Job Description"):
        with st.spinner("Analyzing job description..."):
            job_analyzer = JobAnalyzer()
            analysis = job_analyzer.analyze_job(job_description)
            
            st.markdown("### 📊 Job Analysis Results")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### 🎯 Key Requirements")
                for req in analysis.get("requirements", []):
                    st.markdown(f"- {req}")
                
                st.markdown("#### 💼 Responsibilities")
                for resp in analysis.get("responsibilities", []):
                    st.markdown(f"- {resp}")
            
            with col2:
                st.markdown("#### 🛠️ Required Skills")
                for skill in analysis.get("skills", []):
                    st.markdown(f"- {skill}")
                
                st.markdown("#### 🎓 Preferred Qualifications")
                for qual in analysis.get("qualifications", []):
                    st.markdown(f"- {qual}")
            
            # Additional analysis
            st.markdown("#### 📈 Analysis Summary")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Experience Level", analysis.get("experience_level", "Not specified"))
            
            with col2:
                st.metric("Industry", analysis.get("industry", "General"))
            
            with col3:
                st.metric("Key Phrases Found", len(analysis.get("key_phrases", [])))
            
            # Save analysis
            st.session_state.job_analysis = analysis
            st.success("✅ Job analysis completed!")

def show_generate_documents():
    st.markdown('<h2 class="sub-header">📝 Generate Content</h2>', unsafe_allow_html=True)
    
    # Check if we have necessary data
    if not st.session_state.profile_data:
        st.warning("⚠️ Please set up your profile first!")
        if st.button("Go to Profile Setup"):
            st.session_state.page = "👤 Profile Setup"
        return
    
    if not st.session_state.job_description:
        st.warning("⚠️ Please provide a job description first!")
        if st.button("Go to Job Analysis"):
            st.session_state.page = "💼 Job Analysis"
        return
    
    # Check Google Gemini availability (only on this page)
    ai_manager = AIManager()
    providers = ai_manager.get_available_providers()
    
    if "Google Gemini" not in providers or not providers["Google Gemini"]["available"]:
        st.error("❌ Google Gemini is not available. Please check your API key in Settings.")
        return
    
    # Test connection button (only when needed)
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("### 🔗 Connection Test")
        st.info("Test your Gemini connection before generating content (optional)")
    with col2:
        if st.button("🧪 Test Connection", type="secondary"):
            with st.spinner("Testing connection..."):
                test_result = ai_manager.test_provider_connection()
                if test_result["available"]:
                    st.success("✅ Connection successful!")
                else:
                    st.error(f"❌ Connection failed: {test_result['error']}")
    
    # Customization options using the new prompt system
    st.markdown("### 🎨 Customization Options")
    
    resume_gen = ResumeGenerator(ai_manager.get_provider())
    cover_letter_gen = CoverLetterGenerator(ai_manager.get_provider())
    customization_options = resume_gen.get_customization_options()
    
    col1, col2 = st.columns(2)
    
    with col1:
        tone = st.selectbox(
            "Document Tone:",
            customization_options["tones"],
            help="Choose the tone for your documents"
        )
        
        industry = st.selectbox(
            "Industry Focus:",
            ["general"] + customization_options["industries"],
            help="Select the industry focus for targeted content"
        )
    
    with col2:
        experience_level = st.selectbox(
            "Experience Level:",
            customization_options["experience_levels"],
            help="Target experience level for the role"
        )
        
        focus_areas = st.multiselect(
            "Focus Areas:",
            ["Technical Skills", "Leadership", "Project Management", "Innovation", "Teamwork", "Communication"],
            default=["Technical Skills"],
            help="Select areas to emphasize in your documents"
        )
    
    # Show customization preview
    with st.expander("🎯 Customization Preview"):
        st.markdown(f"""
        **Selected Options:**
        - **Tone**: {tone.title()}
        - **Industry**: {industry.title() if industry != "general" else "General"}
        - **Experience Level**: {experience_level.replace('_', ' ').title()}
        - **Focus Areas**: {', '.join(focus_areas)}
        """)
        
        # Show industry-specific information if selected
        if industry != "general":
            industry_keywords = resume_gen.get_industry_keywords(industry)
            industry_focus_areas = resume_gen.get_industry_focus_areas(industry)
            st.markdown(f"""
            **Industry-Specific Focus:**
            - **Keywords**: {', '.join(industry_keywords[:5])}...
            - **Focus Areas**: {', '.join(industry_focus_areas)}
            """)
    
    # Generate documents (batch: summary, skills, experience, cover letter)
    st.markdown("---")
    st.markdown("### 🚀 Generate Content")
    
    if st.button("🚀 Generate Resume Sections & Cover Letter", type="primary", use_container_width=True):
        with st.spinner("Generating your customized content with Google Gemini..."):
            try:
                batch_result = cover_letter_gen.generate_batch_resume_and_cover_letter(
                    profile_data=st.session_state.profile_data,
                    job_description=st.session_state.job_description,
                    job_analysis=st.session_state.get("job_analysis", {}),
                    tone=tone,
                    focus_areas=focus_areas,
                    experience_level=experience_level,
                    industry=industry
                )
                st.session_state.generated_resume_sections = batch_result
                st.success("✅ Content generated successfully with Google Gemini!")
            except Exception as e:
                st.error(f"❌ Error generating content: {str(e)}")
                if "quota" in str(e).lower():
                    quota_info = ai_manager.get_quota_info()
                    st.info(f"Quota remaining: {quota_info['daily_remaining']} daily, {quota_info['minute_remaining']} minute")
    
    # Display generated content
    sections = st.session_state.get("generated_resume_sections", {})
    if sections:
        st.markdown("### 📝 Professional Summary")
        st.text_area("Professional Summary", value=sections.get("summary", ""), height=150, key="summary_section")
        st.markdown("### 🛠️ Skills")
        st.text_area("Skills", value=sections.get("skills", ""), height=100, key="skills_section")
        st.markdown("### 💼 Work Experience")
        st.text_area("Work Experience", value=sections.get("experience", ""), height=250, key="experience_section")
        st.markdown("### 📝 Cover Letter")
        st.text_area("Cover Letter", value=sections.get("cover_letter", ""), height=400, key="cover_letter_section")

def show_settings():
    st.markdown('<h2 class="sub-header">⚙️ Settings</h2>', unsafe_allow_html=True)
    
    st.markdown("### 🔑 Google Gemini API Configuration")
    
    # Instructions for setting up
    st.markdown("### 📋 Setup Instructions")
    
    with st.expander("How to get your free Google Gemini API key"):
        st.markdown("""
        **🌟 Google Gemini Setup (Recommended):**
        1. Go to https://makersuite.google.com/app/apikey
        2. Sign in with your Google account
        3. Click "Create API Key"
        4. Copy the key to your `.env` file
        5. **Free Tier**: 15 requests/minute, 1500 requests/day
        
        **Why Google Gemini?**
        - Most generous free tier
        - No credit card required
        - Fast and reliable
        - Professional results
        """)
    
    # Show current .env status
    if os.path.exists(".env"):
        st.success("✅ .env file found")
        with open(".env", "r") as f:
            env_content = f.read()
        
        # Check if Google API key is set
        if "GOOGLE_API_KEY" in env_content:
            lines = env_content.split('\n')
            for line in lines:
                if line.startswith('GOOGLE_API_KEY='):
                    key_value = line.split('=', 1)[1]
                    if key_value and key_value != 'your_google_gemini_api_key_here':
                        st.success("✅ Google Gemini API Key configured")
                    else:
                        st.warning("⚠️ Google Gemini API Key - Not configured")
                    break
        else:
            st.warning("⚠️ Google Gemini API Key - Not found in .env")
    else:
        st.warning("⚠️ .env file not found")
        st.info("Create a .env file with your Google Gemini API key")
        st.markdown("""
        **Quick Setup:**
        1. Copy `env_example.txt` to `.env`
        2. Edit `.env` with your Google Gemini API key
        3. Restart the application
        """)
    
    # Google Gemini benefits
    st.markdown("### 💰 Google Gemini Benefits")
    
    st.markdown("""
    **🌟 Why Google Gemini is Perfect:**
    
    **Free Tier Limits:**
    - 15 requests per minute
    - 1500 requests per day
    - No monthly limits
    
    **Cost Savings:**
    - Completely free to start
    - No credit card required
    - No hidden fees
    
    **Performance:**
    - Fast response times
    - High-quality results
    - Reliable service
    
    **Setup:**
    - Just need Google account
    - Simple API key generation
    - Instant activation
    """)
    
    # Usage tips
    st.markdown("### 💡 Usage Tips")
    
    st.markdown("""
    **📊 Monitor Your Usage:**
    - Check Google AI Studio dashboard
    - Track request counts
    - Stay within free limits
    
    **🎯 Optimize Requests:**
    - Use detailed job descriptions
    - Be specific in customization options
    - Review generated content before regenerating
    
    **📈 Daily Limits:**
    - 1500 requests per day
    - Perfect for regular job applications
    - More than enough for most users
    """)

if __name__ == "__main__":
    main() 