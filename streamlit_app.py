"""
Modern Streamlit UI for Job Application Assistant
"""
import streamlit as st
import os
import json
import logging
from datetime import datetime
from typing import Dict, Any, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import our components
from src.main import JobApplicationAssistant
from src.utils.pdf_processor import PDFProcessor
from src.ui.app import UIComponents

# Set page configuration with modern settings
st.set_page_config(
    page_title="AI Job Application Assistant",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Helper functions for file handling
def extract_text_from_file(uploaded_file):
    """Extract text from an uploaded file (PDF or TXT)"""
    try:
        if uploaded_file.type == "application/pdf":
            pdf_processor = PDFProcessor()
            return pdf_processor.extract_text_from_pdf(uploaded_file)
        else:  # Assume it's text file
            return uploaded_file.getvalue().decode("utf-8")
    except Exception as e:
        st.error(f"Error extracting text from file: {str(e)}")
        return None

# Helper functions for history
def save_application_history(job_title: str, company: str, results: Dict[str, Any]):
    """Save application history to a JSON file"""
    # Create history directory if it doesn't exist
    history_dir = os.path.join("outputs", "history")
    os.makedirs(history_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Sanitize filenames
    job_title_safe = "".join([c if c.isalnum() else "_" for c in job_title])
    company_safe = "".join([c if c.isalnum() else "_" for c in company])
    
    # Create filename
    filename = f"{timestamp}_{company_safe}_{job_title_safe}.json"
    
    # Prepare data
    history_data = {
        "timestamp": timestamp,
        "job_title": job_title,
        "company": company,
        "results": results
    }
    
    # Save to file
    file_path = os.path.join(history_dir, filename)
    try:
        with open(file_path, 'w') as f:
            json.dump(history_data, f)
        return filename
    except Exception as e:
        logger.error(f"Error saving history file: {str(e)}")
        return None

def load_application_history() -> List[Dict[str, Any]]:
    """Load application history from JSON files"""
    history_dir = os.path.join("outputs", "history")
    if not os.path.exists(history_dir):
        return []
    
    # Get all JSON files in the history directory
    history_files = [f for f in os.listdir(history_dir) if f.endswith('.json')]
    history = []
    
    # Load each file
    for filename in history_files:
        try:
            with open(os.path.join(history_dir, filename), 'r') as f:
                history_data = json.load(f)
                history.append(history_data)
        except Exception as e:
            logger.error(f"Error loading history file {filename}: {e}")
    
    # Sort by timestamp (newest first)
    history.sort(key=lambda x: x.get("timestamp", ""), reverse=True)
    return history

# Initialize session state
def init_session_state():
    """Initialize session state variables"""
    if "processing" not in st.session_state:
        st.session_state.processing = False
    if "results" not in st.session_state:
        st.session_state.results = {}
    if "saved_files" not in st.session_state:
        st.session_state.saved_files = {}
    if "job_title" not in st.session_state:
        st.session_state.job_title = ""
    if "company" not in st.session_state:
        st.session_state.company = ""
    if "job_description" not in st.session_state:
        st.session_state.job_description = ""
    if "resume_text" not in st.session_state:
        st.session_state.resume_text = ""
    if "history" not in st.session_state:
        st.session_state.history = load_application_history()
    if "input_method" not in st.session_state:
        st.session_state.input_method = "text"

def display_application_page():
    """Display the main application page with clear input sections"""
    
    # Job Information Section
    st.markdown("### 💼 Job Information")
    col1, col2 = st.columns(2)
    with col1:
        job_title = st.text_input(
            "Job Title", 
            value=st.session_state.job_title,
            placeholder="e.g., Senior Software Engineer"
        )
        st.session_state.job_title = job_title
    
    with col2:
        company = st.text_input(
            "Company", 
            value=st.session_state.company,
            placeholder="e.g., Google, Microsoft, Amazon"
        )
        st.session_state.company = company
    
    st.markdown("---")
    
    # Job Description Section
    st.markdown("### 📋 Job Description")
    
    input_method = st.radio(
        "How would you like to provide the job description?",
        ["📝 Text Input", "📄 File Upload"], 
        horizontal=True
    )
    
    if input_method == "📝 Text Input":
        job_description = st.text_area(
            "Paste the job description here:", 
            height=200, 
            value=st.session_state.job_description,
            placeholder="Copy and paste the complete job description including responsibilities, requirements, and qualifications..."
        )
        st.session_state.job_description = job_description
    else:
        job_file = st.file_uploader(
            "Upload job description file", 
            type=["pdf", "txt"], 
            key="job_file"
        )
        if job_file:
            job_description = extract_text_from_file(job_file)
            if job_description:
                st.session_state.job_description = job_description
                st.success("✅ Job description loaded successfully!")
                with st.expander("📖 Preview Job Description"):
                    preview_text = job_description[:800] + ("..." if len(job_description) > 800 else "")
                    st.text(preview_text)

    st.markdown("---")
    
    # Resume Section
    st.markdown("### 👤 Your Resume")
    
    resume_method = st.radio(
        "How would you like to provide your resume?",
        ["📝 Text Input", "📄 File Upload"], 
        horizontal=True, 
        key="resume_method"
    )
    
    if resume_method == "📝 Text Input":
        resume_text = st.text_area(
            "Paste your resume content here:", 
            height=200, 
            value=st.session_state.resume_text,
            placeholder="Copy and paste your complete resume including experience, education, skills, and achievements..."
        )
        st.session_state.resume_text = resume_text
    else:
        resume_file = st.file_uploader(
            "Upload your resume", 
            type=["pdf", "txt"], 
            key="resume_file"
        )
        if resume_file:
            resume_text = extract_text_from_file(resume_file)
            if resume_text:
                st.session_state.resume_text = resume_text
                st.success("✅ Resume loaded successfully!")
                with st.expander("📖 Preview Resume"):
                    preview_text = resume_text[:800] + ("..." if len(resume_text) > 800 else "")
                    st.text(preview_text)

    st.markdown("---")
    
    # Processing Section
    st.markdown("### 🚀 Generate Your Optimized Application")
    
    if st.button("🎯 Optimize My Application", type="primary", use_container_width=True):
        # Validate inputs
        if not st.session_state.job_description.strip():
            st.error("📋 Please provide a job description to continue.")
            st.stop()
        
        if not st.session_state.resume_text.strip():
            st.error("👤 Please provide your resume to continue.")
            st.stop()
        
        # Show loading
        with st.spinner("🤖 Processing your application... This may take 2-3 minutes"):
            try:
                # Create Job Application Assistant
                assistant = JobApplicationAssistant()
                
                # Process application
                results = assistant.process_application(
                    st.session_state.job_description, 
                    st.session_state.resume_text
                )
                
                # Create specific output directory for streamlit runs
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                streamlit_output_dir = os.path.join("outputs", "streamlit", timestamp)
                
                # Save outputs
                saved_files = assistant.save_outputs(streamlit_output_dir)
                
                # Update session state
                st.session_state.processing = False
                st.session_state.results = results
                st.session_state.saved_files = saved_files
                
                # Save to history
                if st.session_state.job_title and st.session_state.company:
                    save_application_history(
                        st.session_state.job_title, 
                        st.session_state.company, 
                        results
                    )
                    # Reload history
                    st.session_state.history = load_application_history()
                
                st.success("🎉 Application optimized successfully!")
                st.balloons()
                
            except Exception as e:
                st.session_state.processing = False
                st.error(f"❌ An error occurred: {str(e)}")
                logger.error(f"Error processing application: {e}", exc_info=True)

    # Display results if available
    if st.session_state.results:
        st.markdown("---")
        st.markdown("## 📊 Your Application Results")
        
        # Create tabs for results
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔍 Job Analysis", 
            "📄 Resume Tips", 
            "✉️ Cover Letter", 
            "🎯 Interview Prep"
        ])
        
        with tab1:
            if "job_analysis" in st.session_state.results:
                st.markdown(st.session_state.results["job_analysis"])
                if "job_analysis" in st.session_state.saved_files:
                    with open(st.session_state.saved_files["job_analysis"], 'r', encoding='utf-8') as f:
                        st.download_button(
                            label="📥 Download Job Analysis",
                            data=f.read(),
                            file_name="job_analysis.md",
                            mime="text/markdown",
                            key="download_job_analysis"
                        )
        
        with tab2:
            if "resume_suggestions" in st.session_state.results:
                st.markdown(st.session_state.results["resume_suggestions"])
                if "resume_suggestions" in st.session_state.saved_files:
                    with open(st.session_state.saved_files["resume_suggestions"], 'r', encoding='utf-8') as f:
                        st.download_button(
                            label="📥 Download Resume Tips",
                            data=f.read(),
                            file_name="resume_suggestions.md",
                            mime="text/markdown",
                            key="download_resume_suggestions"
                        )
        
        with tab3:
            if "cover_letter" in st.session_state.results:
                st.markdown(st.session_state.results["cover_letter"])
                if "cover_letter" in st.session_state.saved_files:
                    with open(st.session_state.saved_files["cover_letter"], 'r', encoding='utf-8') as f:
                        st.download_button(
                            label="📥 Download Cover Letter",
                            data=f.read(),
                            file_name="cover_letter.md",
                            mime="text/markdown",
                            key="download_cover_letter"
                        )
        
        with tab4:
            if "interview_prep" in st.session_state.results:
                st.markdown(st.session_state.results["interview_prep"])
                if "interview_prep" in st.session_state.saved_files:
                    with open(st.session_state.saved_files["interview_prep"], 'r', encoding='utf-8') as f:
                        st.download_button(
                            label="📥 Download Interview Guide",
                            data=f.read(),
                            file_name="interview_prep.md",
                            mime="text/markdown",
                            key="download_interview_prep"
                        )

def display_history_page():
    """Display the history page"""
    st.markdown("## 📚 Application History")
    
    if not st.session_state.history:
        st.info("📭 No application history yet. Process your first application to see history here.")
        return
    
    # Display history entries
    for i, entry in enumerate(st.session_state.history):
        job_title = entry.get('job_title', 'Untitled Position')
        company = entry.get('company', 'Unknown Company')
        timestamp = entry.get('timestamp', '')
        
        # Format timestamp
        try:
            dt = datetime.strptime(timestamp, "%Y%m%d_%H%M%S")
            formatted_date = dt.strftime("%B %d, %Y at %I:%M %p")
        except:
            formatted_date = timestamp
        
        with st.expander(f"🎯 {job_title} at {company} - {formatted_date}"):
            if "results" in entry:
                # Show results in tabs
                hist_tab1, hist_tab2, hist_tab3, hist_tab4 = st.tabs([
                    "Job Analysis", "Resume Tips", "Cover Letter", "Interview Prep"
                ])
                
                with hist_tab1:
                    st.markdown(entry["results"].get("job_analysis", "No job analysis available."))
                
                with hist_tab2:
                    st.markdown(entry["results"].get("resume_suggestions", "No resume suggestions available."))
                
                with hist_tab3:
                    st.markdown(entry["results"].get("cover_letter", "No cover letter available."))
                
                with hist_tab4:
                    st.markdown(entry["results"].get("interview_prep", "No interview preparation available."))

def display_analytics_page():
    """Display analytics page"""
    st.markdown("## 📊 Analytics & Insights")
    
    total_applications = len(st.session_state.history)
    
    if total_applications == 0:
        st.info("📈 Analytics will appear here after you process some job applications.")
        return
    
    # Stats overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Applications", total_applications)
    
    with col2:
        unique_companies = len(set(entry.get('company', '') for entry in st.session_state.history))
        st.metric("Companies", unique_companies)
    
    with col3:
        st.metric("Documents", total_applications * 4)
    
    with col4:
        st.metric("AI Powered", "100%")

# Main application
def main():
    """Main Streamlit application"""
    # Initialize session state
    init_session_state()
    
    # Load CSS
    UIComponents.load_css()
    
    # Header
    st.markdown("# 🚀 AI Job Application Assistant")
    st.markdown("Transform your job search with AI-powered tools that analyze job descriptions, optimize your resume, craft cover letters, and prepare you for interviews.")
    
    # Sidebar navigation
    with st.sidebar:
        st.markdown("## Navigation")
        page = st.radio(
            "Choose a page:",
            ["New Application", "History", "Analytics"]
        )
        
        st.markdown("---")
        st.markdown("### Features")
        st.markdown("""
        - 🔍 Smart Job Analysis
        - 📄 Resume Optimization  
        - ✉️ Cover Letter Generation
        - 🎯 Interview Preparation
        - 📥 Document Export
        """)
    
    # Display selected page
    if page == "New Application":
        display_application_page()
    elif page == "History":
        display_history_page()
    else:  # Analytics
        display_analytics_page()
    
    # Footer
    st.markdown("---")
    st.markdown("**Job Application Assistant** powered by [CrewAI](https://crewai.com) & [Streamlit](https://streamlit.io) • © 2025")

if __name__ == "__main__":
    main()