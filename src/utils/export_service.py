import os
import json
import markdown2
import pdfkit
from typing import Dict, Any

class ExportService:
    """
    Resume export service with multiple format support
    
    Principles:
    - Support multiple export formats
    - Maintain consistent styling
    - Provide flexible export options
    """
    @staticmethod
    def to_json(resume: Dict[str, Any], output_path: str = None) -> str:
        """
        Export resume to JSON format
        
        :param resume: Resume dictionary
        :param output_path: Optional output file path
        :return: JSON string
        """
        json_content = json.dumps(resume, indent=2)
        
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(json_content)
        
        return json_content

    @staticmethod
    def to_markdown(resume: Dict[str, Any], output_path: str = None) -> str:
        """
        Convert resume to markdown format
        
        :param resume: Resume dictionary
        :param output_path: Optional output file path
        :return: Markdown content
        """
        basics = resume.get('basics', {})
        projects = resume.get('projects', [])
        skills = resume.get('skills', {})
        contributions = resume.get('contributions', {})

        markdown_content = f"""# {basics.get('name', 'GitHub Resume')}

## Profile
- **Username**: {basics.get('username', 'N/A')}
- **Location**: {basics.get('location', 'Not specified')}
- **Bio**: {basics.get('bio', 'No bio available')}

## Contributions
- **Total Repositories**: {contributions.get('total_repositories', 0)}
- **Followers**: {contributions.get('followers', 0)}
- **Following**: {contributions.get('following', 0)}

## Skills
- **Programming Languages**: {', '.join(skills.get('programming_languages', []))}
- **Topics**: {', '.join(skills.get('topics', []))}

## Projects
"""
        
        for project in projects:
            markdown_content += f"""
### {project.get('name', 'Unnamed Project')}
- **Description**: {project.get('description', 'No description')}
- **Language**: {project.get('language', 'N/A')}
- **Stars**: {project.get('stars', 0)}
- **Forks**: {project.get('forks', 0)}
- **URL**: {project.get('html_url', '#')}
"""
        
        if output_path:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w') as f:
                f.write(markdown_content)
        
        return markdown_content

    @staticmethod
    def to_pdf(resume: Dict[str, Any], output_path: str = None) -> str:
        """
        Convert resume to PDF
        
        :param resume: Resume dictionary
        :param output_path: Optional output file path
        :return: Path to generated PDF
        """
        # Convert markdown to HTML
        markdown_content = ExportService.to_markdown(resume)
        html_content = markdown2.markdown(markdown_content)
        
        # Default PDF path if not specified
        if not output_path:
            output_path = os.path.join(os.getcwd(), 'github_resume.pdf')
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Convert HTML to PDF with styling
        html_template = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; line-height: 1.6; }}
                h1, h2 {{ color: #333; }}
                a {{ color: #0066cc; text-decoration: none; }}
            </style>
        </head>
        <body>
            {html_content}
        </body>
        </html>
        """
        
        pdfkit.from_string(html_template, output_path)
        
        return output_path
