#!/usr/bin/env python
"""
Runner script for Job Application Assistant

This script provides a convenient way to run the Job Application Assistant.
"""
import os
import sys
import argparse
from pathlib import Path

# Ensure we can import the package by adding the project root to sys.path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from src.main import JobApplicationAssistant

def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Job Application Assistant')
    parser.add_argument('--job', type=str, help='Path to job description file')
    parser.add_argument('--resume', type=str, help='Path to resume file')
    parser.add_argument('--output', type=str, default='outputs', help='Output directory for generated files')
    return parser.parse_args()

def read_file(file_path):
    """Read text from a file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def main():
    """Run the Job Application Assistant from command line"""
    args = parse_args()
    
    if args.job and args.resume:
        # Read job description and resume from files
        job_description = read_file(args.job)
        resume_text = read_file(args.resume)
        
        # Create and run the job application assistant
        assistant = JobApplicationAssistant()
        results = assistant.process_application(job_description, resume_text)
        
        # Create specific output directory for command line runs
        from datetime import datetime
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cmd_output_dir = os.path.join(args.output, "cmd", timestamp)
        
        # Save outputs
        saved_files = assistant.save_outputs(cmd_output_dir)
        
        print("Job Application Assistant process completed.")
        print("Files saved:")
        for output_type, file_path in saved_files.items():
            print(f"- {output_type}: {file_path}")
    else:
        print("Usage examples:")
        print("python run.py --job job_description.txt --resume resume.txt")
        print("python run.py --job job_description.txt --resume resume.txt --output my_outputs")
        print("\nAlternatively, run the Streamlit UI with: streamlit run streamlit_app.py")

if __name__ == "__main__":
    main()