"""
UI components for the Job Application Assistant
"""
import streamlit as st
from typing import Dict, Any, List, Optional

class UIComponents:
    """UI components for the Job Application Assistant"""
    
    @staticmethod
    def load_css():
        """Load custom CSS styles"""
        st.markdown("""
            <style>
            .main-header {
                font-size: 2.5rem;
                color: #1E3A8A;
                margin-bottom: 1rem;
            }
            .section-header {
                font-size: 1.5rem;
                color: #1E3A8A;
                margin-top: 1.5rem;
                margin-bottom: 1rem;
            }
            .info-text {
                font-size: 1rem;
                color: #4B5563;
            }
            .output-container {
                background-color: #F3F4F6;
                padding: 1.5rem;
                border-radius: 0.5rem;
                margin: 1rem 0;
            }
            .footer {
                margin-top: 3rem;
                font-size: 0.8rem;
                color: #6B7280;
                text-align: center;
            }
            </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """Render the application header"""
        st.markdown("<h1 class='main-header'>📝 Job Application Assistant</h1>", unsafe_allow_html=True)
        st.markdown(
            "<p class='info-text'>Optimize your job applications with AI assistance: analyze job descriptions, "
            "tailor your resume, create cover letters, and prepare for interviews.</p>",
            unsafe_allow_html=True
        )
    
    @staticmethod
    def render_sidebar():
        """Render the application sidebar"""
        with st.sidebar:
            st.markdown("## Navigation")
            page = st.radio("Go to", ["New Application", "History"])
            
            st.markdown("---")
            st.markdown("## About")
            st.markdown(
                "This app uses AI to help you optimize your job applications. "
                "Upload a job description and your resume to get started."
            )
            return page
    
    @staticmethod
    def render_footer():
        """Render the application footer"""
        st.markdown(
            "<div class='footer'>Job Application Assistant powered by CrewAI © 2025</div>",
            unsafe_allow_html=True
        )
    
    @staticmethod
    def render_results_tabs(results: Dict[str, Any], saved_files: Dict[str, str]):
        """
        Render results in tabs
        
        Args:
            results: Dictionary containing results
            saved_files: Dictionary containing paths to saved files
        """
        st.markdown("<h2 class='section-header'>Results</h2>", unsafe_allow_html=True)
        
        # Create tabs for different outputs
        tab1, tab2, tab3, tab4 = st.tabs(["Job Analysis", "Resume Suggestions", "Cover Letter", "Interview Prep"])
        
        with tab1:
            if "job_analysis" in results and results["job_analysis"]:
                st.markdown(results["job_analysis"])
                if "job_analysis" in saved_files:
                    with open(saved_files["job_analysis"], 'r') as f:
                        st.download_button(
                            label="Download Job Analysis",
                            data=f.read(),
                            file_name="job_analysis.md",
                            mime="text/markdown"
                        )
            else:
                st.info("No job analysis results available.")
        
        with tab2:
            if "resume_suggestions" in results and results["resume_suggestions"]:
                st.markdown(results["resume_suggestions"])
                if "resume_suggestions" in saved_files:
                    with open(saved_files["resume_suggestions"], 'r') as f:
                        st.download_button(
                            label="Download Resume Suggestions",
                            data=f.read(),
                            file_name="resume_suggestions.md",
                            mime="text/markdown"
                        )
            else:
                st.info("No resume suggestion results available.")
        
        with tab3:
            if "cover_letter" in results and results["cover_letter"]:
                st.markdown(results["cover_letter"])
                if "cover_letter" in saved_files:
                    with open(saved_files["cover_letter"], 'r') as f:
                        st.download_button(
                            label="Download Cover Letter",
                            data=f.read(),
                            file_name="cover_letter.md",
                            mime="text/markdown"
                        )
            else:
                st.info("No cover letter results available.")
        
        with tab4:
            if "interview_prep" in results and results["interview_prep"]:
                st.markdown(results["interview_prep"])
                if "interview_prep" in saved_files:
                    with open(saved_files["interview_prep"], 'r') as f:
                        st.download_button(
                            label="Download Interview Preparation",
                            data=f.read(),
                            file_name="interview_prep.md",
                            mime="text/markdown"
                        )
            else:
                st.info("No interview preparation results available.")