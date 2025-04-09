import logging
import sys
from logging.handlers import RotatingFileHandler
from src.core.config import config

class LoggerFactory:
    """
    Advanced logging configuration with multiple handlers
    
    Principles:
    - Structured logging
    - Configurable log levels
    - Rotation and archiving
    """
    @staticmethod
    def create_logger(name: str, level: str = 'INFO') -> logging.Logger:
        """
        Create a configured logger with file and console output
        
        :param name: Logger name
        :param level: Logging level
        :return: Configured logger
        """
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, level.upper()))
        
        # Prevent duplicate handlers
        if logger.handlers:
            return logger
        
        # Console Handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        
        # File Handler with Rotation
        file_handler = RotatingFileHandler(
            f'logs/{name}.log', 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        
        # Formatters
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
        )
        
        console_handler.setFormatter(console_formatter)
        file_handler.setFormatter(file_formatter)
        
        # Add handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)
        
        return logger

# Create application-wide loggers
github_logger = LoggerFactory.create_logger('github_resume_agent')
app_logger = LoggerFactory.create_logger('resume_app')
error_logger = LoggerFactory.create_logger('errors', level='ERROR')
