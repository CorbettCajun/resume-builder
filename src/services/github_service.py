from typing import Dict, List, Any
import requests
import os
from src.core.config import config
from src.core.logging import github_logger
from src.core.error_handling import CircuitBreaker, retry
from github import Github, Auth

class GitHubService:
    """
    Advanced GitHub data retrieval service
    
    Principles:
    - Robust API interaction
    - Comprehensive error handling
    - Efficient data extraction
    """
    def __init__(self, token: str = None, base_url: str = 'https://api.github.com'):
        """
        Initialize GitHub Service

        :param token: GitHub API token
        :param base_url: Base URL for GitHub API
        :raises ValueError: If token is invalid
        """
        # Attempt to get token from multiple sources
        if token is not None:
            self.token = token.strip()
        else:
            # Try to get token from environment or configuration
            env_token = os.getenv('GITHUB_TOKEN')
            config_token = config.get('github.token')
            
            # Prioritize non-None tokens
            self.token = (env_token or config_token or '').strip()
        
        # Validate token
        if not self.token or len(self.token) < 20:
            raise ValueError("Invalid GitHub token")
        
        # Create GitHub authentication object
        self.auth = Auth.Token(self.token)
        
        # Initialize GitHub client with new authentication method
        self.github_client = Github(auth=self.auth)
        
        self.base_url = base_url or config.get('github.api_base_url', 'https://api.github.com')
        self.logger = github_logger
        
        # Configure headers for API requests
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }

    @CircuitBreaker()
    @retry(max_attempts=3)
    def get_user_profile(self, username: str) -> Dict[str, Any]:
        """
        Retrieve comprehensive GitHub user profile
        
        :param username: GitHub username
        :return: User profile information
        """
        try:
            response = requests.get(
                f'{self.base_url}/users/{username}', 
                headers=self.headers
            )
            response.raise_for_status()
            
            profile = response.json()
            github_logger.info(f"Retrieved profile for {username}")
            
            return {
                'name': profile.get('name'),
                'login': profile.get('login'),
                'email': profile.get('email'),
                'bio': profile.get('bio'),
                'location': profile.get('location'),
                'public_repos': profile.get('public_repos'),
                'followers': profile.get('followers'),
                'following': profile.get('following'),
                'avatar_url': profile.get('avatar_url')
            }
        
        except requests.RequestException as e:
            github_logger.error(f"GitHub API error: {e}")
            raise

    @CircuitBreaker()
    @retry(max_attempts=3)
    def get_repositories(self, username: str, max_repos: int = 50) -> List[Dict[str, Any]]:
        """
        Retrieve user's repositories with detailed information
        
        :param username: GitHub username
        :param max_repos: Maximum number of repositories to retrieve
        :return: List of repository details
        """
        try:
            response = requests.get(
                f'{self.base_url}/users/{username}/repos', 
                headers=self.headers,
                params={'per_page': max_repos, 'sort': 'updated'}
            )
            response.raise_for_status()
            
            repos = response.json()[:max_repos]
            github_logger.info(f"Retrieved {len(repos)} repositories for {username}")
            
            return [
                {
                    'name': repo.get('name'),
                    'full_name': repo.get('full_name'),
                    'description': repo.get('description'),
                    'language': repo.get('language'),
                    'stars': repo.get('stargazers_count'),
                    'forks': repo.get('forks_count'),
                    'created_at': repo.get('created_at'),
                    'updated_at': repo.get('updated_at'),
                    'html_url': repo.get('html_url'),
                    'topics': self._get_repository_topics(repo.get('full_name'))
                }
                for repo in repos
            ]
        
        except requests.RequestException as e:
            github_logger.error(f"GitHub repositories retrieval error: {e}")
            raise

    def _get_repository_topics(self, full_name: str) -> List[str]:
        """
        Retrieve repository topics

        :param full_name: Full repository name (owner/repo)
        :return: List of repository topics
        """
        headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.mercy-preview+json'
        }

        try:
            response = requests.get(
                f'{self.base_url}/repos/{full_name}/topics',
                headers=headers
            )
            response.raise_for_status()
            
            # Handle both dictionary and list responses
            topics_data = response.json()
            if isinstance(topics_data, dict):
                return topics_data.get('names', [])
            elif isinstance(topics_data, list):
                return topics_data
            else:
                return []
        except Exception as e:
            # Log the error and return an empty list
            github_logger.error(f"Error retrieving topics for {full_name}: {e}")
            return []

    def get_contributions(self, username: str) -> Dict[str, Any]:
        """
        Retrieve user's contribution statistics
        
        :param username: GitHub username
        :return: Contribution statistics
        """
        # Note: GitHub GraphQL API would be more suitable for detailed contributions
        # This is a simplified implementation
        profile = self.get_user_profile(username)
        return {
            'total_repositories': profile.get('public_repos', 0),
            'followers': profile.get('followers', 0),
            'following': profile.get('following', 0)
        }
