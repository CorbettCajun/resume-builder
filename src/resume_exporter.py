import os
import json
import markdown
import pdfkit
from typing import Dict, List, Any, Optional

class ResumeExporter:
    """
    Handles exporting resume to various formats
    """

    @staticmethod
    def to_json(resume: Dict[str, Any], output_path: str = None) -> str:
        """
        Convert resume to JSON format

        :param resume: Resume dictionary
        :param output_path: Optional path to save JSON file
        :return: JSON string
        """
        json_content = json.dumps(resume, indent=2)
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(json_content)
        
        return json_content

    @staticmethod
    def to_markdown(resume: Dict[str, Any], output_path: str = None) -> str:
        """
        Convert resume to markdown format

        :param resume: Resume dictionary
        :param output_path: Optional path to save markdown file
        :return: Markdown content
        """
        profile = resume.get('profile', {})
        repositories = resume.get('repositories', [])
        skills = resume.get('skills', [])
        contributions = resume.get('contributions', {})

        markdown_content = f"""# {profile.get('name', 'GitHub Resume')}

## Profile
- **Location**: {profile.get('location', 'Not specified')}
- **Email**: {profile.get('email', 'Not available')}
- **Bio**: {profile.get('bio', 'No bio available')}
- **Total Repositories**: {contributions.get('total_repositories', 0)}
- **Total Contributions**: {contributions.get('total_contributions', 0)}

## Skills
**Programming Languages**: {', '.join(skills)}

## Projects
"""
        for repo in repositories:
            markdown_content += f"""### {repo.get('name', 'Unnamed Project')}
- **Language**: {repo.get('language', 'Not specified')}
- **Description**: {repo.get('description', 'No description')}
- **Stars**: {repo.get('stars', 0)}
- **Forks**: {repo.get('forks', 0)}

"""
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(markdown_content)
        
        return markdown_content

    @staticmethod
    def to_pdf(resume: Dict[str, Any], output_path: str = None) -> Optional[str]:
        """
        Convert resume to PDF format

        :param resume: Resume dictionary
        :param output_path: Optional path to save PDF file
        :return: PDF file path or None
        """
        # Check if wkhtmltopdf is available
        try:
            config = pdfkit.configuration()
        except OSError:
            raise RuntimeError("wkhtmltopdf not installed. Please install it to generate PDFs.")
        
        # Convert to markdown first
        markdown_content = ResumeExporter.to_markdown(resume)
        
        # Convert markdown to HTML
        html_content = markdown.markdown(markdown_content)
        
        # Wrap HTML with basic styling
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; max-width: 800px; margin: 0 auto; padding: 20px; }}
                h1, h2 {{ color: #333; }}
                ul {{ padding-left: 20px; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        # Generate PDF
        if output_path is None:
            output_path = 'resume.pdf'
        
        try:
            pdfkit.from_string(full_html, output_path, configuration=config)
            return output_path
        except Exception as e:
            print(f"Error generating PDF: {e}")
            return None
