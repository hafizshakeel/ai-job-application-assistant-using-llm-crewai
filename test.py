#!/usr/bin/env python
"""
Test script for Job Application Assistant

This script provides a simple test of the Job Application Assistant functionality
using the example files provided.
"""
import os
import sys
from pathlib import Path

# Ensure we can import the package by adding the project root to sys.path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from src.main import JobApplicationAssistant

def main():
    """Run a basic test of the Job Application Assistant"""
    print("Running Job Application Assistant test...")
    
    # Check if example files exist
    job_desc_path = os.path.join("examples", "job_description.txt")
    resume_path = os.path.join("examples", "resume.txt")
    
    if not os.path.exists(job_desc_path) or not os.path.exists(resume_path):
        print(f"Error: Example files not found. Make sure you have the following files:")
        print(f"- {job_desc_path}")
        print(f"- {resume_path}")
        return
    
    try:
        # Read example files
        with open(job_desc_path, 'r', encoding='utf-8') as f:
            job_description = f.read()
        
        with open(resume_path, 'r', encoding='utf-8') as f:
            resume_text = f.read()
        
        print("\n✓ Successfully loaded example files")
        print(f"- Job description: {len(job_description)} characters")
        print(f"- Resume: {len(resume_text)} characters")
        
        # Create test output directory
        test_output_dir = os.path.join("outputs", "test")
        os.makedirs(test_output_dir, exist_ok=True)
        
        # Initialize the Job Application Assistant
        print("\nInitializing Job Application Assistant...")
        assistant = JobApplicationAssistant()
        print("✓ Successfully initialized assistant")
        
        # Process the application
        print("\nProcessing application...")
        print("This may take a few minutes depending on your API keys and model settings.")
        results = assistant.process_application(job_description, resume_text)
        
        # Save outputs
        print("\nSaving outputs...")
        saved_files = assistant.save_outputs(test_output_dir)
        
        print("\n✅ Test completed successfully!")
        print("\nFiles saved:")
        for output_type, file_path in saved_files.items():
            print(f"- {output_type}: {file_path}")
        
        print("\nTo run with your own files, use:")
        print("python run.py --job your_job_description.txt --resume your_resume.txt")
        print("\nOr to use the Streamlit UI, run:")
        print("streamlit run streamlit_app.py")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        print("\nMake sure you have:")
        print("1. Set up your environment variables in .env file")
        print("2. Installed all required packages from requirements.txt")
        print("3. Valid API keys for your LLM provider (Gemini) and SerpAPI")

if __name__ == "__main__":
    main()