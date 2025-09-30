"""
Main Job Application Assistant implementation
"""
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
import os
import logging
from typing import Dict, Any

# Import custom tools and utilities
from .tools.custom_tool import web_search_tool
from .utils.application_processor import ApplicationProcessor

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@CrewBase
class JobApplicationAssistant:
    """  
    A simple tool that uses AI agents to help with job applications:
    - Analyze job descriptions
    - Provide resume tailoring suggestions
    - Generate cover letters
    - Prepare for interviews
    """
    
    # Config file path (only agents.yaml is needed now)
    agents_config = os.path.join(os.path.dirname(__file__), "config/agents.yaml")
    
    def __init__(self):
        """Initialize the Job Application Assistant"""
        self.processor = ApplicationProcessor()
        # Check if memory feature should be enabled
        self.use_memory = os.getenv("OPENAI_API_KEY") is not None
    
    @agent
    def job_analyzer(self) -> Agent: 
        """Create the Job Description Analyst agent"""
        return Agent(
            config=self.agents_config['job_analyzer_agent'],
            tools=[web_search_tool],
            verbose=True,
        )
    
    @agent
    def resume_tailor(self) -> Agent:
        """Create the Resume Optimization Specialist agent"""
        return Agent(
            config=self.agents_config['resume_tailor_agent'],
            tools=[web_search_tool],
            verbose=True,
        )
    
    @agent
    def cover_letter_writer(self) -> Agent:
        """Create the Cover Letter Writer agent"""
        return Agent(
            config=self.agents_config['cover_letter_agent'],
            tools=[web_search_tool],
            verbose=True,
        )
    
    @agent
    def interview_coach(self) -> Agent:
        """Create the Interview Coach agent"""
        return Agent(
            config=self.agents_config['interview_prep_agent'],
            tools=[web_search_tool],
            verbose=True,
        )
    
    @task
    def analyze_job_description(self) -> Task:
        """Create task for analyzing job description"""
        return Task(
            description="""
            # Job Analysis
            
            Analyze the provided job description and extract the following basic information:
            1. Key technical skills required
            2. Main responsibilities of the role  
            3. Experience level required
            
            Keep your analysis simple and concise.
            Always start your output with the header "# Job Analysis" to clearly mark this section.
            
            Job Description:
            {job_description}
            """,
            expected_output="A simple analysis of the job description with key requirements.",
            agent=self.job_analyzer(),
        )
    
    @task
    def tailor_resume(self) -> Task:
        """Create task for tailoring resume"""
        return Task(
            description="""
            # Resume Suggestions
            
            Compare the candidate's resume with the job description and provide 3-5 simple suggestions for optimization:
            1. Skills to highlight based on job requirements
            2. Experiences to emphasize that align with the role
            3. Keywords to include for ATS optimization
            
            Keep your suggestions simple and actionable.
            Always start your output with the header "# Resume Suggestions" to clearly mark this section.
            
            Job Description:
            {job_description}
            
            Resume:
            {resume}
            """,
            expected_output="Simple suggestions for tailoring the resume to better match the job requirements.",
            agent=self.resume_tailor(),
        )
    
    @task
    def write_cover_letter(self) -> Task:
        """Create task for writing cover letter"""
        return Task(
            description="""
            # Cover Letter
            
            Write a brief, simple personalized cover letter that:
            1. Addresses the hiring manager (use "Hiring Manager" if no name provided)
            2. Expresses interest in the specific role
            3. Highlights 2-3 relevant experiences/skills that match the job requirements  
            4. Includes a professional closing

            KEEP IT SIMPLE. The cover letter should be concise and focused ONLY on introducing the candidate and expressing interest in the role.
            
            DO NOT include interview questions or preparation materials in this output.
            Always start your output with the header "# Cover Letter" to clearly mark the section.
            
            Job Description:
            {job_description}
            
            Resume:
            {resume}
            """,
            expected_output="A simple, personalized cover letter ready to be submitted with the application.",
            agent=self.cover_letter_writer(),
        )
    
    @task
    def prepare_interview(self) -> Task:
        """Create task for interview preparation"""
        return Task(
            description="""
            # Interview Preparation
            
            Generate a simple interview preparation guide with:
            1. 3-5 potential interview questions based on the job description
            2. Brief suggested answers that highlight the candidate's relevant experience
            3. 1-2 key talking points to emphasize during the interview
            
            KEEP IT SIMPLE. Focus only on interview preparation content.
            Always start your output with the header "# Interview Preparation" to clearly mark this section.
            
            Job Description:
            {job_description}
            
            Resume:
            {resume}
            """,
            expected_output="A simple interview preparation guide with questions, suggested answers, and talking points.",
            agent=self.interview_coach(),
        )
    
    @crew
    def crew(self) -> Crew:
        """Create the crew with all agents and tasks"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            memory=self.use_memory,
            verbose=True,
        )
    
    def process_application(self, job_description: str, resume_text: str) -> Dict[str, Any]:
        """
        Process a job application using the crew
        
        Args:
            job_description: The job description text
            resume_text: The resume text
            
        Returns:
            Dict containing all outputs from the crew
        """
        crew_instance = self.crew()
        return self.processor.process_application(crew_instance, job_description, resume_text)
    
    def save_outputs(self, output_dir: str = "outputs") -> Dict[str, str]:
        """
        Save all outputs to files
        
        Args:
            output_dir: Directory to save outputs
            
        Returns:
            Dict with paths to saved files
        """
        return self.processor.save_outputs(output_dir)

def main():  
    # Create and run the job application assistant
    assistant = JobApplicationAssistant()
    
    # Save outputs to a specific directory for example runs
    saved_files = assistant.save_outputs("outputs/example")
    
    print("Job Application Assistant process completed.")
    print("Files saved:")
    for output_type, file_path in saved_files.items():
        print(f"- {output_type}: {file_path}")

# Only run if explicitly called as a script, not when imported
if __name__ == "__main__" and "__file__" in globals():
    main()
