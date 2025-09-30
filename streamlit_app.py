"""
Streamlit UI for Job Application Assistant
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

# Set page configuration
st.set_page_config(
    page_title="Job Application Assistant",
    page_icon="📝",
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

# Application Pages
def display_application_page():
    """Display the main application page"""
    # Job Information
    st.markdown("<h3 class='section-header'>Job Information</h3>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    
    with col1:
        job_title = st.text_input("Job Title", value=st.session_state.job_title)
        st.session_state.job_title = job_title
    
    with col2:
        company = st.text_input("Company", value=st.session_state.company)
        st.session_state.company = company
    
    # Job Description Input
    st.markdown("<h3 class='section-header'>Job Description</h3>", unsafe_allow_html=True)
    input_method = st.radio("Input method", ["Text", "Upload File"], horizontal=True)
    st.session_state.input_method = input_method
    
    if input_method == "Text":
        job_description = st.text_area("Paste the job description here", 
                                      height=200, 
                                      value=st.session_state.job_description)
        st.session_state.job_description = job_description
    else:
        job_file = st.file_uploader("Upload job description", 
                                   type=["pdf", "txt"], 
                                   key="job_file")
        if job_file:
            job_description = extract_text_from_file(job_file)
            if job_description:
                st.session_state.job_description = job_description
                st.success("Job description loaded successfully!")
                with st.expander("Preview Job Description"):
                    st.text(job_description[:500] + ("..." if len(job_description) > 500 else ""))
    
    # Resume Input
    st.markdown("<h3 class='section-header'>Your Resume</h3>", unsafe_allow_html=True)
    resume_method = st.radio("Input method ", ["Text", "Upload File"], horizontal=True, key="resume_method")
    
    if resume_method == "Text":
        resume_text = st.text_area("Paste your resume here", 
                                  height=200, 
                                  value=st.session_state.resume_text)
        st.session_state.resume_text = resume_text
    else:
        resume_file = st.file_uploader("Upload your resume", 
                                     type=["pdf", "txt"], 
                                     key="resume_file")
        if resume_file:
            resume_text = extract_text_from_file(resume_file)
            if resume_text:
                st.session_state.resume_text = resume_text
                st.success("Resume loaded successfully!")
                with st.expander("Preview Resume"):
                    st.text(resume_text[:500] + ("..." if len(resume_text) > 500 else ""))
    
    # Submit Button
    if st.button("Optimize My Application"):
        # Validate inputs
        if not st.session_state.job_description:
            st.error("Please enter a job description.")
            return
        
        if not st.session_state.resume_text:
            st.error("Please enter your resume.")
            return
        
        # Process the application
        st.session_state.processing = True
        
        with st.spinner("Processing your application... This may take a few minutes."):
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
                
                st.success("Application processed successfully!")
                
            except Exception as e:
                st.session_state.processing = False
                st.error(f"An error occurred: {str(e)}")
                logger.error(f"Error processing application: {e}", exc_info=True)
    
    # Display results if available using UIComponents
    if not st.session_state.processing and st.session_state.results:
        UIComponents.render_results_tabs(st.session_state.results, st.session_state.saved_files)

def display_history_page():
    """Display the history page"""
    st.markdown("<h2 class='section-header'>Application History</h2>", unsafe_allow_html=True)
    
    if not st.session_state.history:
        st.info("No previous applications found.")
        return
    
    # Display history entries
    for i, entry in enumerate(st.session_state.history):
        job_title = entry.get('job_title', 'Untitled')
        company = entry.get('company', 'Unknown')
        timestamp = entry.get('timestamp', '')
        
        with st.expander(f"{job_title} at {company} - {timestamp}"):
            if "results" in entry:
                # Use UIComponents for consistent rendering
                UIComponents.render_results_tabs(entry["results"], {})
            else:
                st.warning("No results available for this entry.")

# Main application
def main():
    """Main Streamlit application"""
    # Initialize session state
    init_session_state()
    
    # Load custom CSS using UIComponents
    UIComponents.load_css()
    
    # App header using UIComponents
    UIComponents.render_header()
    
    # Create sidebar using UIComponents
    page = UIComponents.render_sidebar()
    
    # Display the selected page
    if page == "New Application":
        display_application_page()
    else:
        display_history_page()
    
    # Footer using UIComponents
    UIComponents.render_footer()

if __name__ == "__main__":
    main()