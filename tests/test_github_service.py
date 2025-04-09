import os
import sys
import pytest
from unittest.mock import patch
import os

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.services.github_service import GitHubService
from src.core.config import config

class TestGitHubService:
    @pytest.fixture
    def github_service(self):
        """Create a GitHub service instance for testing"""
        return GitHubService()

    def test_initialization(self, github_service):
        """Test service initialization"""
        assert github_service is not None
        assert github_service.token is not None

    @patch('requests.get')
    def test_get_user_profile(self, mock_get, github_service):
        """Test user profile retrieval"""
        # Mock successful response
        mock_response = mock_get.return_value
        mock_response.json.return_value = {
            'name': 'Test User',
            'login': 'testuser',
            'email': 'test@example.com',
            'bio': 'Test bio',
            'location': 'Test Location',
            'public_repos': 10,
            'followers': 5,
            'following': 3,
            'avatar_url': 'https://example.com/avatar.jpg'
        }
        mock_response.raise_for_status.return_value = None

        # Test profile retrieval
        profile = github_service.get_user_profile('testuser')
        
        assert profile['name'] == 'Test User'
        assert profile['login'] == 'testuser'
        assert 'email' in profile
        assert 'bio' in profile

    @patch('requests.get')
    def test_get_repositories(self, mock_get, github_service):
        """Test repository retrieval"""
        # Mock successful response
        mock_response = mock_get.return_value
        mock_response.json.return_value = [
            {
                'name': 'test-repo',
                'full_name': 'testuser/test-repo',
                'description': 'Test repository',
                'language': 'Python',
                'stargazers_count': 10,
                'forks_count': 5,
                'created_at': '2023-01-01T00:00:00Z',
                'updated_at': '2023-04-01T00:00:00Z',
                'html_url': 'https://github.com/testuser/test-repo'
            }
        ]
        
        # Mock topics response
        def side_effect(url, *args, **kwargs):
            if 'topics' in url:
                mock_topics_response = type('MockResponse', (), {
                    'json': lambda self: {'names': ['python', 'test']},
                    'raise_for_status': lambda self: None
                })()
                return mock_topics_response
            return mock_response
        
        mock_get.side_effect = side_effect
        mock_response.raise_for_status.return_value = None

        # Test repository retrieval
        repos = github_service.get_repositories('testuser')
        
        assert len(repos) > 0
        assert repos[0]['name'] == 'test-repo'
        assert repos[0]['topics'] == ['python', 'test']

    def test_error_handling(self):
        """Test error scenarios"""
        # Test empty token
        with pytest.raises(ValueError, match="Invalid GitHub token"):
            GitHubService(token="")
        
        # Test extremely short token
        with pytest.raises(ValueError, match="Invalid GitHub token"):
            GitHubService(token="short")
        
        # Test None token with mocked config and environment
        with patch.object(config, 'get', return_value=None), \
             patch.object(os, 'getenv', return_value=None):
            with pytest.raises(ValueError, match="Invalid GitHub token"):
                GitHubService(token=None)

    def test_configuration(self):
        """Test configuration settings"""
        # Check that a GitHub token is available (either from config or environment)
        token = os.getenv('GITHUB_TOKEN') or config.get('github.token')
        assert token is not None, "No GitHub token found. Please set GITHUB_TOKEN or github.token in config"
        
        # Verify token meets minimum length requirement
        assert len(token) >= 20, "GitHub token is too short"
