import os
from flask import Flask, request, jsonify, render_template
from src.core.config import config
from src.services.github_service import GitHubService
from src.services.resume_service import ResumeService
from src.utils.export_service import ExportService
from src.core.logging import app_logger

def create_app():
    """
    Application factory for Flask app
    
    Principles:
    - Modular application design
    - Configurable environment
    - Centralized error handling
    """
    app = Flask(__name__, template_folder='../templates')
    
    # Configuration
    app.config.update(
        SECRET_KEY=os.urandom(24),
        DEBUG=config.get('app.debug', False)
    )
    
    @app.route('/')
    def index():
        """
        Render main application page
        """
        return render_template('index.html')
    
    @app.route('/generate_resume', methods=['POST'])
    def generate_resume():
        """
        Generate resume from GitHub username
        """
        try:
            # Extract parameters
            username = request.form.get('github_username')
            output_format = request.form.get('format', 'json')
            
            # Validate input
            if not username:
                return jsonify({'error': 'GitHub username is required'}), 400
            
            # Initialize services
            github_service = GitHubService()
            resume_service = ResumeService(github_service)
            
            # Generate resume
            resume = resume_service.generate_resume(username)
            
            # Export based on format
            if output_format == 'json':
                return jsonify(resume)
            elif output_format == 'markdown':
                return ExportService.to_markdown(resume)
            elif output_format == 'pdf':
                pdf_path = ExportService.to_pdf(resume)
                return jsonify({'pdf_path': pdf_path})
            else:
                return jsonify({'error': 'Invalid output format'}), 400
        
        except Exception as e:
            app_logger.error(f"Resume generation error: {e}")
            return jsonify({'error': str(e)}), 500
    
    @app.errorhandler(Exception)
    def handle_error(e):
        """
        Global error handler
        """
        app_logger.error(f"Unhandled exception: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
    
    return app

# Application instance
app = create_app()

if __name__ == '__main__':
    # Validate configuration before starting
    config.validate()
    app.run(host='0.0.0.0', port=5000)
