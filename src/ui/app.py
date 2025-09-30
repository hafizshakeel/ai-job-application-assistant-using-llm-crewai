"""
Modern UI components for the Job Application Assistant
"""
import streamlit as st
from typing import Dict, Any, List, Optional
import time

class UIComponents:
    """Modern UI components for the Job Application Assistant"""
    
    @staticmethod
    def load_css():
        """Load clean and minimalistic CSS styles"""
        st.markdown("""
            <style>
            /* Import Google Fonts */
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
            
            /* Global Styles */
            .stApp {
                font-family: 'Inter', sans-serif;
                background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
            }
            
            /* Hide Streamlit branding */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            .stDeployButton {visibility: hidden;}
            
            /* Custom container */
            .main-container {
                background: white;
                border-radius: 12px;
                padding: 2rem;
                margin: 1rem 0;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
                border: 1px solid #e2e8f0;
            }
            
            /* Header Styles */
            .hero-header {
                text-align: center;
                color: #1e293b;
                font-size: 2.5rem;
                font-weight: 600;
                margin: 1rem 0;
                line-height: 1.2;
            }
            
            .hero-subtitle {
                text-align: center;
                font-size: 1.1rem;
                color: #64748b;
                margin-bottom: 2rem;
                font-weight: 400;
                line-height: 1.5;
            }
            
            /* Card Styles */
            .feature-card {
                background: white;
                border-radius: 8px;
                padding: 1.5rem;
                margin: 0.5rem 0;
                border: 1px solid #e2e8f0;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
                transition: all 0.2s ease;
            }
            
            .feature-card:hover {
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                border-color: #cbd5e1;
            }
            
            /* Section Headers */
            .section-header {
                font-size: 1.4rem;
                font-weight: 600;
                color: #1e293b;
                margin: 1.5rem 0 1rem 0;
                padding-left: 0.5rem;
                border-left: 3px solid #3b82f6;
            }
            
            /* Modern Tabs */
            .stTabs [data-baseweb="tab-list"] {
                gap: 4px;
                background: #f8fafc;
                padding: 4px;
                border-radius: 8px;
                border: 1px solid #e2e8f0;
            }
            
            .stTabs [data-baseweb="tab"] {
                height: 44px;
                background: transparent;
                border-radius: 6px;
                color: #64748b;
                font-weight: 500;
                font-size: 0.9rem;
                border: none;
                padding: 0 1rem;
                transition: all 0.2s ease;
            }
            
            .stTabs [data-baseweb="tab"]:hover {
                background: #f1f5f9;
                color: #475569;
            }
            
            .stTabs [aria-selected="true"] {
                background: #3b82f6 !important;
                color: white !important;
                box-shadow: 0 1px 3px rgba(59, 130, 246, 0.3);
            }
            
            /* Modern Buttons */
            .stButton > button {
                background: #3b82f6;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 0.75rem 1.5rem;
                font-weight: 500;
                font-size: 0.95rem;
                transition: all 0.2s ease;
                box-shadow: 0 1px 3px rgba(59, 130, 246, 0.3);
                text-transform: none;
                width: 100%;
            }
            
            .stButton > button:hover {
                background: #2563eb;
                box-shadow: 0 2px 6px rgba(59, 130, 246, 0.4);
                transform: translateY(-1px);
            }
            
            .stButton > button:active {
                transform: translateY(0);
            }
            
            /* Download Button */
            .stDownloadButton > button {
                background: #059669;
                color: white;
                border: none;
                border-radius: 6px;
                padding: 0.5rem 1rem;
                font-weight: 500;
                font-size: 0.85rem;
                transition: all 0.2s ease;
                box-shadow: 0 1px 3px rgba(5, 150, 105, 0.3);
            }
            
            .stDownloadButton > button:hover {
                background: #047857;
                box-shadow: 0 2px 6px rgba(5, 150, 105, 0.4);
            }
            
            /* File Uploader */
            .stFileUploader > div > div {
                background: #f8fafc;
                border: 2px dashed #cbd5e1;
                border-radius: 8px;
                padding: 1.5rem;
                text-align: center;
                transition: all 0.2s ease;
            }
            
            .stFileUploader > div > div:hover {
                border-color: #3b82f6;
                background: #f1f5f9;
            }
            
            /* Text Areas */
            .stTextArea > div > div > textarea {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0.75rem;
                font-family: 'Inter', sans-serif;
                font-size: 0.9rem;
                transition: all 0.2s ease;
                background: white;
                resize: vertical;
            }
            
            .stTextArea > div > div > textarea:focus {
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
                outline: none;
            }
            
            /* Text Inputs */
            .stTextInput > div > div > input {
                border: 1px solid #d1d5db;
                border-radius: 8px;
                padding: 0.75rem;
                font-family: 'Inter', sans-serif;
                font-size: 0.9rem;
                transition: all 0.2s ease;
                background: white;
            }
            
            .stTextInput > div > div > input:focus {
                border-color: #3b82f6;
                box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
                outline: none;
            }
            
            /* Radio buttons */
            .stRadio > div {
                gap: 1rem;
            }
            
            .stRadio > div > label {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 0.75rem 1rem;
                margin: 0;
                cursor: pointer;
                transition: all 0.2s ease;
                font-size: 0.9rem;
            }
            
            .stRadio > div > label:hover {
                border-color: #3b82f6;
                background: #f8fafc;
            }
            
            /* Sidebar */
            .css-1d391kg {
                background: #1e293b;
            }
            
            .css-1d391kg .stMarkdown {
                color: white;
            }
            
            .css-1d391kg .stRadio > div > label {
                background: rgba(255, 255, 255, 0.1);
                border: 1px solid rgba(255, 255, 255, 0.2);
                color: white;
            }
            
            .css-1d391kg .stRadio > div > label:hover {
                background: rgba(255, 255, 255, 0.2);
                border-color: rgba(255, 255, 255, 0.4);
            }
            
            /* Success/Info Messages */
            .stSuccess {
                background: #dcfce7;
                color: #166534;
                border: 1px solid #bbf7d0;
                border-radius: 8px;
                padding: 1rem;
            }
            
            .stInfo {
                background: #dbeafe;
                color: #1e40af;
                border: 1px solid #bfdbfe;
                border-radius: 8px;
                padding: 1rem;
            }
            
            .stError {
                background: #fef2f2;
                color: #dc2626;
                border: 1px solid #fecaca;
                border-radius: 8px;
                padding: 1rem;
            }
            
            /* Progress Animation */
            .progress-container {
                background: #e2e8f0;
                height: 4px;
                border-radius: 2px;
                overflow: hidden;
                margin: 1rem 0;
            }
            
            .progress-bar {
                height: 100%;
                background: #3b82f6;
                border-radius: 2px;
                animation: progress 2s ease-in-out infinite;
            }
            
            @keyframes progress {
                0% { width: 0%; }
                50% { width: 70%; }
                100% { width: 100%; }
            }
            
            /* Footer */
            .modern-footer {
                text-align: center;
                padding: 1.5rem;
                color: #64748b;
                font-size: 0.85rem;
                border-top: 1px solid #e2e8f0;
                margin-top: 2rem;
                background: #f8fafc;
                border-radius: 8px;
            }
            
            /* Stats Cards */
            .stats-card {
                background: white;
                color: #1e293b;
                padding: 1.5rem;
                border-radius: 8px;
                text-align: center;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
                border: 1px solid #e2e8f0;
                transition: all 0.2s ease;
            }
            
            .stats-card:hover {
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                transform: translateY(-2px);
            }
            
            .stats-number {
                font-size: 1.8rem;
                font-weight: 600;
                margin-bottom: 0.5rem;
                color: #3b82f6;
            }
            
            .stats-label {
                font-size: 0.85rem;
                color: #64748b;
                font-weight: 500;
            }
            
            /* Expander */
            .streamlit-expanderHeader {
                background: white;
                border: 1px solid #e2e8f0;
                border-radius: 8px;
                padding: 1rem;
                font-weight: 500;
            }
            
            /* Loading spinner */
            .stSpinner > div {
                border-top-color: #3b82f6 !important;
            }
            
            /* Remove excessive spacing */
            .element-container {
                margin-bottom: 0.5rem !important;
            }
            
            /* Responsive Design */
            @media (max-width: 768px) {
                .hero-header {
                    font-size: 2rem;
                }
                
                .hero-subtitle {
                    font-size: 1rem;
                }
                
                .main-container {
                    margin: 0.5rem;
                    padding: 1rem;
                }
                
                .stats-card {
                    margin-bottom: 1rem;
                }
            }
            </style>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_header():
        """Render the clean application header"""
        st.markdown("""
            <div class="main-container">
                <h1 class="hero-header">🚀 AI Job Application Assistant</h1>
                <p class="hero-subtitle">
                    Transform your job search with AI-powered tools that analyze job descriptions, 
                    optimize your resume, craft cover letters, and prepare you for interviews.
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_modern_sidebar():
        """Render the clean application sidebar"""
        with st.sidebar:
            st.markdown("""
                <div style="text-align: center; padding: 1rem 0; border-bottom: 1px solid rgba(255,255,255,0.2); margin-bottom: 1rem;">
                    <h2 style="color: white; margin-bottom: 0.5rem; font-size: 1.3rem;">Navigation</h2>
                    <p style="color: rgba(255,255,255,0.7); font-size: 0.85rem;">Choose your workflow</p>
                </div>
            """, unsafe_allow_html=True)
            
            page = st.radio(
                "Select Mode:",
                ["New Application", "History", "Analytics"],
                label_visibility="collapsed"
            )
            
            st.markdown("---")
            
            # Feature highlights
            st.markdown("""
                <div style="color: white; padding: 1rem 0;">
                    <h3 style="color: white; font-size: 1rem; margin-bottom: 1rem;">Features</h3>
                    <div style="font-size: 0.85rem; line-height: 1.8; color: rgba(255,255,255,0.8);">
                        • Smart Job Analysis<br>
                        • Resume Optimization<br>
                        • Cover Letter Generation<br>
                        • Interview Preparation<br>
                        • Document Export
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            return page
    
    @staticmethod
    def render_stats_cards():
        """Render simple statistics cards"""
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
                <div class="stats-card">
                    <div class="stats-number">4</div>
                    <div class="stats-label">AI Agents</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
                <div class="stats-card">
                    <div class="stats-number">∞</div>
                    <div class="stats-label">Applications</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown("""
                <div class="stats-card">
                    <div class="stats-number">95%</div>
                    <div class="stats-label">Success Rate</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown("""
                <div class="stats-card">
                    <div class="stats-number">⚡</div>
                    <div class="stats-label">Fast Results</div>
                </div>
            """, unsafe_allow_html=True)
    
    @staticmethod
    def render_feature_card(title: str, description: str, icon: str):
        """Render a simple feature card"""
        st.markdown(f"""
            <div class="feature-card">
                <h4 style="color: #1e293b; font-size: 1rem; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.5rem; font-weight: 500;">
                    <span style="font-size: 1.2rem;">{icon}</span>
                    {title}
                </h4>
                <p style="color: #64748b; line-height: 1.5; margin: 0; font-size: 0.85rem;">{description}</p>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_modern_results_tabs(results: Dict[str, Any], saved_files: Dict[str, str]):
        """Render results in clean tabs"""
        st.markdown("""
            <div class="main-container">
                <h2 class="section-header">📊 Your Application Results</h2>
            </div>
        """, unsafe_allow_html=True)
        
        # Create tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🔍 Job Analysis", 
            "📄 Resume Tips", 
            "✉️ Cover Letter", 
            "🎯 Interview Prep"
        ])
        
        # Job Analysis Tab
        with tab1:
            UIComponents._render_result_section(
                "job_analysis", 
                results, 
                saved_files, 
                "📊 Job Analysis Report",
                "job_analysis.md",
                "Analysis Report"
            )
        
        # Resume Suggestions Tab
        with tab2:
            UIComponents._render_result_section(
                "resume_suggestions", 
                results, 
                saved_files,
                "🎯 Resume Optimization Tips",
                "resume_suggestions.md",
                "Resume Tips"
            )
        
        # Cover Letter Tab
        with tab3:
            UIComponents._render_result_section(
                "cover_letter", 
                results, 
                saved_files,
                "✉️ Personalized Cover Letter",
                "cover_letter.md",
                "Cover Letter"
            )
        
        # Interview Prep Tab
        with tab4:
            UIComponents._render_result_section(
                "interview_prep", 
                results, 
                saved_files,
                "🎯 Interview Preparation Guide",
                "interview_prep.md",
                "Interview Guide"
            )
    
    @staticmethod
    def _render_result_section(key: str, results: Dict[str, Any], saved_files: Dict[str, str], 
                              title: str, filename: str, button_label: str):
        """Helper method to render a result section"""
        if key in results and results[key]:
            st.markdown(results[key])
            
            if key in saved_files:
                try:
                    with open(saved_files[key], 'r', encoding='utf-8') as f:
                        content = f.read()
                        st.download_button(
                            label=f"📥 Download {button_label}",
                            data=content,
                            file_name=filename,
                            mime="text/markdown",
                            key=f"download_{key}"
                        )
                except Exception as e:
                    st.error(f"Error reading file: {e}")
        else:
            st.info(f"⏳ {title} will appear here after processing...")
    
    @staticmethod
    def render_loading_animation():
        """Render a simple loading animation"""
        st.markdown("""
            <div class="main-container">
                <div style="text-align: center; padding: 2rem;">
                    <h3 style="color: #1e293b; margin-bottom: 1rem;">🤖 Processing Your Application</h3>
                    <p style="color: #64748b; margin-bottom: 2rem;">Our AI agents are analyzing and optimizing your application...</p>
                    <div class="progress-container">
                        <div class="progress-bar"></div>
                    </div>
                    <p style="color: #64748b; font-size: 0.85rem; margin-top: 1rem;">This usually takes 2-3 minutes</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_footer():
        """Render the clean application footer"""
        st.markdown("""
            <div class="modern-footer">
                <p style="margin: 0;">
                    <strong>Job Application Assistant</strong> powered by 
                    <a href="https://crewai.com" target="_blank" style="color: #3b82f6; text-decoration: none;">CrewAI</a> 
                    & <a href="https://streamlit.io" target="_blank" style="color: #3b82f6; text-decoration: none;">Streamlit</a>
                </p>
                <p style="margin: 0.5rem 0 0 0; font-size: 0.75rem; color: #9ca3af;">
                    © 2025 • Built for job seekers worldwide
                </p>
            </div>
        """, unsafe_allow_html=True)
    
    # Legacy methods for backward compatibility
    @staticmethod
    def render_sidebar():
        """Legacy sidebar method for compatibility"""
        return UIComponents.render_modern_sidebar()
    
    @staticmethod
    def render_results_tabs(results: Dict[str, Any], saved_files: Dict[str, str]):
        """Legacy results method for compatibility"""
        return UIComponents.render_modern_results_tabs(results, saved_files)