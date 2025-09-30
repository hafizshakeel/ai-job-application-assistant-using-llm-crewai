"""
Simple document generation utilities for the Job Application Assistant
"""
import os
import logging
from typing import Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DocumentGenerator:
    """Utility for generating and saving simple documents from agent outputs"""
    
    @staticmethod
    def save_document(content: str, filename: str, output_dir: str = "outputs") -> Optional[str]:
        """
        Save content to a markdown file
        
        Args:
            content: Text content to save
            filename: Name of the file
            output_dir: Directory to save the file
            
        Returns:
            str: Path to the saved file or None if failed
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Ensure filename has .md extension for better formatting
            if not filename.endswith('.md'):
                filename = f"{filename}.md"
            
            # Full path to save the file
            file_path = os.path.join(output_dir, filename)
            
            # Make sure the content starts with a proper header
            if not content.strip().startswith("#"):
                # Extract the title from the filename
                title = filename.replace(".md", "").replace("_", " ").title()
                content = f"# {title}\n\n{content}"
            
            # Ensure we have actual content
            if not content.strip():
                # Provide some basic content if empty
                content = f"# {filename.replace('.md', '').replace('_', ' ').title()}\n\nNo content was generated."
            
            logger.info(f"Writing {len(content)} characters to {file_path}")
            
            # Save the content to the file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            
            # Verify file was written correctly
            if os.path.exists(file_path):
                file_size = os.path.getsize(file_path)
                logger.info(f"Document saved successfully to {file_path} (Size: {file_size} bytes)")
                
                # Double-check content
                with open(file_path, 'r', encoding='utf-8') as f:
                    saved_content = f.read()
                    if len(saved_content) < 10:
                        logger.warning(f"File saved but content seems minimal: {saved_content}")
            else:
                logger.error(f"Failed to verify file existence: {file_path}")
            
            return file_path
        except Exception as e:
            logger.error(f"Error saving document: {str(e)}")
            return None