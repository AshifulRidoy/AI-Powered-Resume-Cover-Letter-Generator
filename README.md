# AI-Powered Resume & Cover Letter Generator

An intelligent system that customizes resumes and cover letters based on job descriptions using Google Gemini AI, with predefined guidelines and prompts for professional, industry-specific content generation.

## ✨ Features

- **🤖 AI-Powered Generation**: Uses Google Gemini for intelligent content creation
- **📄 PDF Resume Upload**: Upload your existing resume to automatically extract information
- **✏️ Manual Profile Input**: Enter your information manually with a user-friendly form
- **📝 Profile Management**: Save and reuse your profile information
- **🎯 Job Analysis**: Analyze job descriptions to identify key requirements
- **📋 Customizable Content**: Generate tailored resumes and cover letters
- **🎨 Professional Guidelines**: Built-in guidelines for different industries and experience levels
- **📱 Modern UI**: Clean, intuitive Streamlit interface

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Clone the repository
git clone <repository-url>
cd Resume-Automation

# Create conda environment
conda env create -f environment.yml
conda activate resume-automation
```

### 2. Configuration

1. Copy the environment template:
   ```bash
   copy env_example.txt .env
   ```

2. Add your Google Gemini API key to `.env`:
   ```
   GEMINI_API_KEY=your_api_key_here
   ```

### 3. Run the Application

```bash
streamlit run app.py
```

The application will open at `http://localhost:8501`

## 📋 Profile Setup Options

### Option 1: PDF Resume Upload 🆕
- Upload your existing resume in PDF format
- The system automatically extracts your information
- Review and edit the extracted data before saving
- Perfect for quick setup with existing resumes

### Option 2: Manual Input
- Fill out a comprehensive form with your information
- Includes all sections: personal info, experience, education, skills, etc.
- Add additional information like certifications, languages, interests
- Ideal for creating a complete profile from scratch

### Option 3: Use Existing Profile
- Load and use previously saved profile information
- Edit existing data or use as-is
- Convenient for regular users

## 🎯 How to Use

### 1. Profile Setup
- Navigate to "Profile Setup" in the sidebar
- Choose your preferred input method (PDF upload, manual, or existing)
- Complete your profile information
- Save your profile for future use

### 2. Job Analysis
- Go to "Job Analysis" section
- Paste the job description
- Get AI-powered analysis of key requirements and skills

### 3. Resume Generation
- Select "Resume Generator"
- Choose your preferred tone and industry
- Generate a customized resume based on your profile and job requirements

### 4. Cover Letter Generation
- Use "Cover Letter Generator"
- Select tone and customization options
- Create personalized cover letters

## 📁 Project Structure

```
Resume-Automation/
├── ai_providers/          # AI provider management
├── data/                  # Profile and data storage
├── prompts/               # Guidelines and prompts
├── utils/                 # Core utilities
│   ├── pdf_parser.py     # PDF parsing functionality 🆕
│   ├── resume_generator.py
│   ├── cover_letter_generator.py
│   └── job_analyzer.py
├── app.py                # Main Streamlit application
├── demo_pdf_parsing.py   # PDF parsing demo 🆕
└── requirements.txt      # Python dependencies
```

## 🧪 Testing

### Test PDF Parsing
```bash
python demo_pdf_parsing.py
```

### Test Prompt System
```bash
python test_prompt_system.py
```

### Test Text Generation
```bash
python demo_text_generation.py
```

## 🔧 Configuration

### Environment Variables
- `GEMINI_API_KEY`: Your Google Gemini API key

### Customization Options
- **Tone**: Professional, Friendly, Formal, Creative
- **Industry**: Technology, Healthcare, Finance, Marketing, etc.
- **Experience Level**: Entry, Mid, Senior, Executive

## 📊 Features in Detail

### PDF Resume Upload
- **Automatic Extraction**: Extracts contact info, experience, education, skills
- **Smart Parsing**: Identifies sections and formats data appropriately
- **Review & Edit**: Review extracted information before saving
- **Error Handling**: Graceful handling of unreadable PDFs

### Profile Management
- **Persistent Storage**: Saves profile data locally
- **Multiple Input Methods**: PDF upload, manual input, or existing profile
- **Comprehensive Data**: Includes all resume sections plus additional information
- **Easy Updates**: Edit and update profile information anytime

### AI-Powered Generation
- **Context-Aware**: Uses job descriptions to tailor content
- **Professional Guidelines**: Built-in best practices for different industries
- **Customizable Output**: Adjust tone, style, and focus areas
- **Quality Assurance**: Ensures professional, ATS-friendly content

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License.

## 🆘 Support

For issues and questions:
1. Check the documentation
2. Run the demo scripts
3. Review the example files
4. Open an issue on GitHub

## 🔄 Updates

### Latest Features (v2.0)
- ✅ PDF resume upload and parsing
- ✅ Multiple profile input methods
- ✅ Enhanced profile management
- ✅ Improved UI/UX
- ✅ Better error handling
- ✅ Comprehensive documentation

---

**Happy Resume Building! 🚀** 