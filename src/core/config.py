import os
from typing import Dict, Any
from dotenv import load_dotenv

class ConfigManager:
    """
    Centralized configuration management with environment-specific settings
    
    Principles:
    - Externalize configuration
    - Support multiple environments
    - Provide type-safe configuration access
    """
    _instance = None
    _config: Dict[str, Any] = {}

    def __new__(cls):
        if not cls._instance:
            cls._instance = super().__new__(cls)
            cls._load_config()
        return cls._instance

    @classmethod
    def _load_config(cls):
        """
        Load configuration from environment variables and .env files
        """
        load_dotenv()  # Load .env file

        # Core GitHub Configuration
        cls._config = {
            'github': {
                'token': os.getenv('GITHUB_TOKEN'),
                'api_base_url': 'https://api.github.com',
                'rate_limit_buffer': 0.1  # 10% buffer for rate limits
            },
            'app': {
                'debug': os.getenv('FLASK_DEBUG', 'False') == 'True',
                'environment': os.getenv('FLASK_ENV', 'production')
            },
            'export': {
                'formats': ['json', 'markdown', 'pdf'],
                'max_projects': 50
            }
        }

    @classmethod
    def get(cls, key: str, default: Any = None) -> Any:
        """
        Retrieve configuration value with optional default

        :param key: Dot-separated configuration key
        :param default: Default value if key is not found
        :return: Configuration value or default
        """
        # Prevent fallback for GitHub token
        if key == 'github.token':
            return None
        
        # Split the key into parts
        parts = key.split('.')
        
        # Traverse the configuration dictionary
        current = cls._config
        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return default
        
        return current

    @classmethod
    def validate(cls):
        """
        Validate critical configuration parameters
        
        :raises ValueError: If critical configuration is missing
        """
        if not cls.get('github.token'):
            raise ValueError("GitHub token is required")

        # Additional validation logic
        if len(cls.get('github.token', '')) < 20:
            raise ValueError("Invalid GitHub token format")

# Singleton instance for easy import
config = ConfigManager()
