import os
from typing import Dict, List, Any
from github import Github, Auth
from dotenv import load_dotenv
from datetime import datetime, timedelta

from src.core.config import config
from src.resume_exporter import ResumeExporter

# Load environment variables
load_dotenv()

class GitHubResumeAgent:
    def __init__(self, token: str = None):
        """
        Initialize GitHub Resume Agent

        :param token: GitHub Personal Access Token
        """
        # Use configuration or environment if token not provided
        self.token = token or os.getenv('GITHUB_TOKEN') or config.get('github.token')
        
        # Validate token
        if not self.token or len(self.token.strip()) < 20:
            raise ValueError("Invalid GitHub token")
        
        # Create GitHub authentication object
        auth = Auth.Token(self.token)
        
        # Initialize GitHub client with new authentication method
        self.github = Github(auth=auth)
        
        # Get authenticated user
        self.user = self.github.get_user()
        
        # Initialize resume exporter
        self.exporter = ResumeExporter()

    def get_repositories(self) -> List[Dict[str, Any]]:
        """
        Retrieve and analyze user's repositories
        
        :return: List of repository details
        """
        repos = self.user.get_repos()
        return [self._analyze_repo(repo) for repo in repos]
    
    def _analyze_repo(self, repo) -> Dict[str, Any]:
        """
        Extract detailed information about a repository
        
        :param repo: GitHub repository object
        :return: Dictionary of repository details
        """
        return {
            'name': repo.name,
            'description': repo.description or 'No description',
            'language': repo.language,
            'stars': repo.stargazers_count,
            'forks': repo.forks_count,
            'created_at': repo.created_at.isoformat(),
            'updated_at': repo.updated_at.isoformat(),
            'url': repo.html_url,
            'topics': repo.get_topics()
        }
    
    def generate_resume(self) -> Dict[str, Any]:
        """
        Generate resume from GitHub profile and repositories
        
        :return: Dictionary containing resume information
        """
        # Fetch repositories
        repositories = self.get_repositories()
        
        # Fetch contributions
        contributions = self.get_contributions()
        
        # Prepare resume structure
        resume = {
            'profile': {
                'name': self.user.name or self.user.login,
                'email': self.user.email,
                'location': self.user.location,
                'bio': self.user.bio,
                'total_repositories': contributions.get('total_repositories', 0),
                'total_contributions': contributions.get('total_contributions', 0)
            },
            'repositories': repositories,
            'skills': self._extract_skills(repositories),
            'contributions': contributions
        }
        
        return resume

    def export_resume(self, format: str = 'json') -> Any:
        """
        Export resume in specified format
        
        :param format: Export format (json, markdown, pdf)
        :return: Exported resume
        """
        resume = self.generate_resume()
        
        if format == 'json':
            return self.exporter.to_json(resume)
        elif format == 'markdown':
            return self.exporter.to_markdown(resume)
        elif format == 'pdf':
            return self.exporter.to_pdf(resume)
        else:
            raise ValueError(f"Unsupported export format: {format}")

    def get_contributions(self) -> Dict[str, int]:
        """
        Retrieve user's contribution statistics
        
        :return: Dictionary of contribution details
        """
        # Use GraphQL to fetch contribution data
        query = """
        query($username: String!) {
            user(login: $username) {
                contributionsCollection {
                    contributionCalendar {
                        totalContributions
                        weeks {
                            contributionDays {
                                contributionCount
                            }
                        }
                    }
                }
            }
        }
        """
        variables = {"username": self.user.login}
        
        try:
            # Assuming a GraphQL method exists in the GitHub class
            result = self.github.graphql(query, variables)
            
            # Extract total contributions
            total_contributions = result['data']['user']['contributionsCollection']['contributionCalendar']['totalContributions']
            
            # Calculate contributions in the last year (simplified)
            contributions_last_year = sum(
                day['contributionCount'] 
                for week in result['data']['user']['contributionsCollection']['contributionCalendar']['weeks']
                for day in week['contributionDays']
            )
            
            return {
                'total_contributions': total_contributions,
                'contributions_last_year': contributions_last_year,
                'total_repositories': len(self.get_repositories())
            }
        except Exception as e:
            # Fallback to a simple method if GraphQL fails
            return {
                'total_contributions': 0,
                'contributions_last_year': 0,
                'total_repositories': 0
            }

    def _extract_skills(self, repositories: List[Dict[str, Any]]) -> List[str]:
        """
        Extract skills from repositories
        
        :param repositories: List of repositories
        :return: List of skills
        """
        language_counts = {}
        for project in repositories:
            lang = project.get('language')
            if lang:
                language_counts[lang] = language_counts.get(lang, 0) + 1
        return sorted(language_counts, key=language_counts.get, reverse=True)[:10]  # Top 10 languages
