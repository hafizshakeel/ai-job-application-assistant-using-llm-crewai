"""
Tools for the Job Application Assistant agents
"""
import os
from typing import Dict, Any, List
from dotenv import load_dotenv
from crewai_tools import SerperDevTool
from crewai.tools import BaseTool

# Load environment variables
load_dotenv()

# Create an instance of SerperDevTool directly
serper_tool = SerperDevTool()

class WebSearchTool(BaseTool):
    """Tool for web search using SerperDev through CrewAI Tools"""
    
    name: str = "Web Search"
    description: str = "Search the web for up-to-date information about companies, job skills, or industry trends."
    
    def _run(self, query: str) -> str:
        """
        Run a web search query
        
        Args:
            query: The search query
            
        Returns:
            str: Search results formatted as text
        """
        try:
            # Use the SerperDevTool to perform the search
            results = serper_tool.search(query)
            return results
        except Exception as e:
            return f"Error performing web search: {str(e)}"

# Create an instance of the tool for easy import
web_search_tool = WebSearchTool()
