"""
PDF Parser for Resume Information Extraction
This module extracts information from uploaded resume PDFs.
"""

import re
from typing import Dict, Any, Optional
import PyPDF2
import io

class PDFParser:
    """Extracts information from resume PDFs."""
    
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.phone_pattern = r'(\+\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        self.linkedin_pattern = r'(?:https?://)?(?:www\.)?linkedin\.com/in/[\w-]+'
        self.github_pattern = r'(?:https?://)?(?:www\.)?github\.com/[\w-]+'
        self.website_pattern = r'(?:https?://)?(?:www\.)?[\w-]+\.[a-z]{2,}(?:/[\w-]*)*'
    
    def extract_from_pdf(self, pdf_file) -> Dict[str, Any]:
        """Extract information from uploaded PDF file."""
        try:
            # Read PDF content
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text_content = ""
            
            # Extract text from all pages
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
            
            # Parse the extracted text
            return self.parse_resume_text(text_content)
            
        except Exception as e:
            raise Exception(f"Error reading PDF: {str(e)}")
    
    def parse_resume_text(self, text: str) -> Dict[str, Any]:
        """Parse resume text and extract structured information."""
        
        # Clean the text
        text = text.strip()
        lines = text.split('\n')
        
        # Initialize extracted data
        extracted_data = {
            "name": "",
            "email": "",
            "phone": "",
            "location": "",
            "linkedin": "",
            "github": "",
            "website": "",
            "summary": "",
            "skills": "",
            "experience": "",
            "education": "",
            "projects": "",
            "further_info": ""
        }
        
        # Extract contact information
        extracted_data["email"] = self._extract_email(text)
        extracted_data["phone"] = self._extract_phone(text)
        extracted_data["linkedin"] = self._extract_linkedin(text)
        extracted_data["github"] = self._extract_github(text)
        extracted_data["website"] = self._extract_website(text)
        
        # Extract name (usually the first prominent line)
        extracted_data["name"] = self._extract_name(lines)
        
        # Extract location
        extracted_data["location"] = self._extract_location(lines)
        
        # Extract sections
        extracted_data["summary"] = self._extract_summary(text)
        extracted_data["skills"] = self._extract_skills(text)
        extracted_data["experience"] = self._extract_experience(text)
        extracted_data["education"] = self._extract_education(text)
        extracted_data["projects"] = self._extract_projects(text)
        extracted_data["further_info"] = self._extract_further_info(text)
        
        return extracted_data
    
    def _extract_name(self, lines: list) -> str:
        """Extract name from resume lines."""
        # Look for the first prominent line (usually the name)
        for line in lines[:5]:  # Check first 5 lines
            line = line.strip()
            if line and len(line) < 50 and not any(char.isdigit() for char in line):
                # Likely a name if it's short and contains no digits
                return line
        return ""
    
    def _extract_email(self, text: str) -> str:
        """Extract email address from text."""
        match = re.search(self.email_pattern, text)
        return match.group() if match else ""
    
    def _extract_phone(self, text: str) -> str:
        """Extract phone number from text."""
        match = re.search(self.phone_pattern, text)
        return match.group() if match else ""
    
    def _extract_linkedin(self, text: str) -> str:
        """Extract LinkedIn URL from text."""
        match = re.search(self.linkedin_pattern, text, re.IGNORECASE)
        return match.group() if match else ""
    
    def _extract_github(self, text: str) -> str:
        """Extract GitHub URL from text."""
        match = re.search(self.github_pattern, text, re.IGNORECASE)
        return match.group() if match else ""
    
    def _extract_website(self, text: str) -> str:
        """Extract website URL from text."""
        match = re.search(self.website_pattern, text, re.IGNORECASE)
        return match.group() if match else ""
    
    def _extract_location(self, lines: list) -> str:
        """Extract location from resume lines."""
        # Look for location patterns in the first few lines
        for line in lines[:10]:
            line = line.strip()
            # Look for city, state patterns
            if re.search(r'[A-Z][a-z]+,\s*[A-Z]{2}', line):
                return line
            # Look for city, country patterns
            elif re.search(r'[A-Z][a-z]+,\s*[A-Z][a-z]+', line):
                return line
        return ""
    
    def _extract_summary(self, text: str) -> str:
        """Extract professional summary from text."""
        # Look for summary section
        summary_patterns = [
            r'(?:summary|profile|objective)[:\s]*([^•\n]+(?:\n[^•\n]+)*)',
            r'(?:professional\s+summary|career\s+summary)[:\s]*([^•\n]+(?:\n[^•\n]+)*)'
        ]
        
        for pattern in summary_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_skills(self, text: str) -> str:
        """Extract skills from text."""
        # Look for skills section
        skills_patterns = [
            r'(?:skills|technical\s+skills|competencies)[:\s]*([^•\n]+(?:\n[^•\n]+)*)',
            r'(?:programming\s+languages|technologies|tools)[:\s]*([^•\n]+(?:\n[^•\n]+)*)'
        ]
        
        for pattern in skills_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_experience(self, text: str) -> str:
        """Extract work experience from text."""
        # Look for experience section
        experience_patterns = [
            r'(?:experience|work\s+experience|employment\s+history)[:\s]*([^•\n]+(?:\n[^•\n]+)*)',
            r'(?:professional\s+experience|career\s+history)[:\s]*([^•\n]+(?:\n[^•\n]+)*)'
        ]
        
        for pattern in experience_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_education(self, text: str) -> str:
        """Extract education from text."""
        # Look for education section
        education_patterns = [
            r'(?:education|academic|qualifications)[:\s]*([^•\n]+(?:\n[^•\n]+)*)',
            r'(?:degree|university|college)[:\s]*([^•\n]+(?:\n[^•\n]+)*)'
        ]
        
        for pattern in education_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_projects(self, text: str) -> str:
        """Extract projects from text."""
        # Look for projects section
        projects_patterns = [
            r'(?:projects|portfolio|key\s+projects)[:\s]*([^•\n]+(?:\n[^•\n]+)*)',
            r'(?:selected\s+projects|notable\s+projects)[:\s]*([^•\n]+(?:\n[^•\n]+)*)'
        ]
        
        for pattern in projects_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return ""
    
    def _extract_further_info(self, text: str) -> str:
        """Extract additional information from text."""
        # Look for additional sections
        additional_patterns = [
            r'(?:certifications|certificates)[:\s]*([^•\n]+(?:\n[^•\n]+)*)',
            r'(?:languages|language\s+skills)[:\s]*([^•\n]+(?:\n[^•\n]+)*)',
            r'(?:interests|hobbies|activities)[:\s]*([^•\n]+(?:\n[^•\n]+)*)',
            r'(?:volunteer|community)[:\s]*([^•\n]+(?:\n[^•\n]+)*)',
            r'(?:awards|achievements|recognition)[:\s]*([^•\n]+(?:\n[^•\n]+)*)'
        ]
        
        additional_info = []
        for pattern in additional_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                additional_info.append(match.group(1).strip())
        
        return "; ".join(additional_info) if additional_info else "" 