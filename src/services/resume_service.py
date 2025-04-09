from typing import Dict, Any, List
from src.services.github_service import GitHubService
from src.core.logging import app_logger

class ResumeService:
    """
    Resume generation service with advanced analysis
    
    Principles:
    - Comprehensive data extraction
    - Intelligent project ranking
    - Flexible resume generation
    """
    def __init__(self, github_service: GitHubService):
        """
        Initialize resume service with GitHub service
        
        :param github_service: Configured GitHub service
        """
        self.github_service = github_service

    def generate_resume(self, username: str) -> Dict[str, Any]:
        """
        Generate comprehensive resume from GitHub profile
        
        :param username: GitHub username
        :return: Structured resume dictionary
        """
        try:
            # Retrieve user profile and repositories
            profile = self.github_service.get_user_profile(username)
            repositories = self.github_service.get_repositories(username)
            contributions = self.github_service.get_contributions(username)

            # Analyze and rank projects
            ranked_projects = self._rank_projects(repositories)

            # Construct resume
            resume = {
                'basics': {
                    'name': profile.get('name') or username,
                    'username': profile.get('login'),
                    'email': profile.get('email'),
                    'bio': profile.get('bio'),
                    'location': profile.get('location'),
                    'avatar': profile.get('avatar_url')
                },
                'work': [],  # Placeholder for potential future work experience
                'projects': ranked_projects[:10],  # Top 10 projects
                'skills': self._extract_skills(repositories),
                'contributions': {
                    'total_repositories': contributions.get('total_repositories', 0),
                    'followers': contributions.get('followers', 0),
                    'following': contributions.get('following', 0)
                }
            }

            app_logger.info(f"Generated resume for {username}")
            return resume

        except Exception as e:
            app_logger.error(f"Resume generation error: {e}")
            raise

    def _rank_projects(self, repositories: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Rank projects based on multiple factors
        
        :param repositories: List of repositories
        :return: Ranked list of projects
        """
        def project_score(project: Dict[str, Any]) -> float:
            """Calculate project importance score"""
            stars_weight = 0.4
            forks_weight = 0.3
            language_bonus = 0.3

            # Base score calculation
            score = (
                project.get('stars', 0) * stars_weight +
                project.get('forks', 0) * forks_weight
            )

            # Language bonus for popular languages
            popular_languages = ['Python', 'JavaScript', 'TypeScript', 'Java', 'Go']
            if project.get('language') in popular_languages:
                score += language_bonus

            return score

        # Sort and rank projects
        return sorted(
            repositories, 
            key=project_score, 
            reverse=True
        )

    def _extract_skills(self, repositories: List[Dict[str, Any]]) -> Dict[str, List[str]]:
        """
        Extract and categorize skills from repositories
        
        :param repositories: List of repositories
        :return: Categorized skills dictionary
        """
        # Language extraction
        languages = {}
        for repo in repositories:
            lang = repo.get('language')
            if lang:
                languages[lang] = languages.get(lang, 0) + 1

        # Sort languages by frequency
        sorted_languages = sorted(
            languages.items(), 
            key=lambda x: x[1], 
            reverse=True
        )

        # Extract topics as additional skills
        topics = set()
        for repo in repositories:
            topics.update(repo.get('topics', []))

        return {
            'programming_languages': [lang for lang, _ in sorted_languages[:5]],
            'topics': list(topics)[:10]
        }
