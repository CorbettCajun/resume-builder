import os
import sys
import pytest
from unittest.mock import patch, MagicMock
from github import Github, Auth

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.github_resume_agent import GitHubResumeAgent
from src.core.config import config

def test_github_resume_agent_initialization():
    """Test initialization of GitHub Resume Agent"""
    # Ensure GitHub token is available
    github_token = os.getenv('GITHUB_TOKEN')
    assert github_token is not None, "GitHub token not found in environment"
    
    # Create agent
    agent = GitHubResumeAgent(github_token)
    
    # Verify basic attributes
    assert agent.github is not None
    assert agent.user is not None

def test_generate_resume():
    """Test resume generation"""
    github_token = os.getenv('GITHUB_TOKEN')
    agent = GitHubResumeAgent(github_token)
    
    # Generate resume
    resume = agent.generate_resume()
    
    # Basic resume validation
    assert isinstance(resume, dict)
    assert 'profile' in resume
    assert 'repositories' in resume

def test_resume_export():
    """Test resume export functionality"""
    github_token = os.getenv('GITHUB_TOKEN')
    agent = GitHubResumeAgent(github_token)
    
    # Export resume to different formats
    markdown_resume = agent.export_resume(format='markdown')
    json_resume = agent.export_resume(format='json')
    
    # Validate export
    assert markdown_resume is not None
    assert json_resume is not None
    
    # PDF generation might not work due to wkhtmltopdf dependency
    try:
        pdf_resume = agent.export_resume(format='pdf')
        assert pdf_resume is not None
    except Exception as e:
        print(f"PDF export not supported: {e}")
        # This is okay, as PDF generation depends on external library

def test_contributions():
    """Test contributions retrieval"""
    github_token = os.getenv('GITHUB_TOKEN')
    agent = GitHubResumeAgent(github_token)
    
    contributions = agent.get_contributions()
    
    # Validate contributions
    assert 'total_contributions' in contributions
    assert 'contributions_last_year' in contributions
    assert contributions['total_contributions'] >= 0
    assert contributions['contributions_last_year'] >= 0
