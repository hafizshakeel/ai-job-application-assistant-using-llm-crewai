"""
Application processor utilities for the Job Application Assistant
"""
import os
import logging
from typing import Dict, Any
from .document_generator import DocumentGenerator

# Configure logging
logger = logging.getLogger(__name__)

class ApplicationProcessor:
    """Handles processing and output management for job applications"""
    
    def __init__(self):
        """Initialize the application processor"""
        self.outputs = {}
    
    def process_application(self, crew_instance, job_description: str, resume_text: str) -> Dict[str, Any]:
        """
        Process a job application using the crew
        
        Args:
            crew_instance: The CrewAI crew instance
            job_description: The job description text
            resume_text: The resume text
            
        Returns:
            Dict containing all outputs from the crew
        """
        # Validate inputs
        if len(job_description.strip()) < 10:
            raise ValueError("Job description is too short or empty.")
        
        if len(resume_text.strip()) < 10:
            raise ValueError("Resume is too short or empty.")
        
        # Prepare inputs for the crew
        inputs = {
            "job_description": job_description,
            "resume": resume_text
        }
        
        # Run the crew to process the application
        logger.info("Starting job application processing")
        results = crew_instance.kickoff(inputs=inputs)
        
        # Process the results to extract relevant sections
        processed_results = self.extract_outputs(results)
        self.outputs = processed_results
        
        return processed_results
    
    def extract_outputs(self, results) -> Dict[str, Any]:
        """
        Extract and format outputs from the crew results
        
        Args:
            results: The raw crew results from CrewAI
            
        Returns:
            Dictionary with formatted outputs
        """
        outputs = {
            "job_analysis": "",
            "resume_suggestions": "",
            "cover_letter": "",
            "interview_prep": ""
        }
        
        try:
            # CrewAI returns a CrewOutput object with tasks_output list
            if hasattr(results, 'tasks_output') and results.tasks_output:
                # Extract individual task results
                for task_output in results.tasks_output:
                    if hasattr(task_output, 'raw') and task_output.raw:
                        content = str(task_output.raw).strip()
                        
                        # Determine which section this content belongs to based on headers
                        content_lower = content.lower()
                        if "# job analysis" in content_lower:
                            outputs["job_analysis"] = content
                        elif "# resume suggestions" in content_lower:
                            outputs["resume_suggestions"] = content
                        elif "# cover letter" in content_lower:
                            outputs["cover_letter"] = content
                        elif "# interview preparation" in content_lower:
                            outputs["interview_prep"] = content
            
            # Fallback: if extraction fails, try alternative methods
            if not any(outputs.values()):
                logger.warning("Primary extraction failed, trying fallback methods")
                result_text = str(results)
                
                # Simple text splitting approach
                sections = []
                current_section = ""
                
                for line in result_text.split('\n'):
                    if any(header in line.lower() for header in ['# job analysis', '# resume suggestions', '# cover letter', '# interview preparation']):
                        if current_section.strip():
                            sections.append(current_section.strip())
                        current_section = line + '\n'
                    else:
                        current_section += line + '\n'
                
                if current_section.strip():
                    sections.append(current_section.strip())
                
                # Assign sections to appropriate outputs
                for section in sections:
                    section_lower = section.lower()
                    if "# job analysis" in section_lower:
                        outputs["job_analysis"] = section
                    elif "# resume suggestions" in section_lower:
                        outputs["resume_suggestions"] = section
                    elif "# cover letter" in section_lower:
                        outputs["cover_letter"] = section
                    elif "# interview preparation" in section_lower:
                        outputs["interview_prep"] = section
        
        except Exception as e:
            logger.error(f"Error extracting outputs: {str(e)}")
            # Provide meaningful error information
            error_msg = f"Error extracting results: {str(e)}"
            outputs = {
                "job_analysis": f"# Job Analysis\n\n{error_msg}",
                "resume_suggestions": f"# Resume Suggestions\n\n{error_msg}",
                "cover_letter": f"# Cover Letter\n\n{error_msg}",
                "interview_prep": f"# Interview Preparation\n\n{error_msg}"
            }
        
        # Ensure all outputs have appropriate headers
        for key in outputs:
            if outputs[key] and not outputs[key].strip().startswith("#"):
                header = f"# {key.replace('_', ' ').title()}"
                outputs[key] = f"{header}\n\n{outputs[key]}"
        
        return outputs
    
    def save_outputs(self, output_dir: str = "outputs") -> Dict[str, str]:
        """
        Save all outputs to files
        
        Args:
            output_dir: Directory to save outputs
            
        Returns:
            Dict with paths to saved files
        """
        os.makedirs(output_dir, exist_ok=True)
        saved_files = {}
        document_generator = DocumentGenerator()
        
        # Define output files
        output_files = {
            "job_analysis": "job_analysis.md",
            "resume_suggestions": "resume_suggestions.md", 
            "cover_letter": "cover_letter.md",
            "interview_prep": "interview_prep.md"
        }
        
        # Save each output type
        for output_type, filename in output_files.items():
            content = self.outputs.get(output_type, "")
            
            # Ensure we have some content
            if not content or len(content.strip()) < 10:
                title = f"# {output_type.replace('_', ' ').title()}"
                content = f"{title}\n\nNo content was generated for this section."
            
            # Save to file
            file_path = document_generator.save_document(content, filename, output_dir)
            saved_files[output_type] = file_path
        
        return saved_files