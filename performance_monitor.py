import time
import tracemalloc
import logging
from functools import wraps

class PerformanceMonitor:
    """
    Advanced performance monitoring and profiling utility
    
    Principles:
    - Track memory usage
    - Measure execution time
    - Log performance metrics
    """
    @staticmethod
    def track_performance(logger=None):
        """
        Decorator to monitor function performance
        
        :param logger: Optional logger instance
        :return: Decorated function
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Start memory tracing
                tracemalloc.start()
                start_time = time.time()
                
                try:
                    # Execute function
                    result = func(*args, **kwargs)
                    
                    # Capture performance metrics
                    end_time = time.time()
                    current, peak = tracemalloc.get_traced_memory()
                    
                    # Log performance details
                    performance_log = {
                        'function': func.__name__,
                        'execution_time_ms': (end_time - start_time) * 1000,
                        'memory_current_bytes': current,
                        'memory_peak_bytes': peak
                    }
                    
                    if logger:
                        logger.info(f"Performance Metrics: {performance_log}")
                    
                    return result
                
                finally:
                    # Stop memory tracing
                    tracemalloc.stop()
            
            return wrapper
        return decorator

# Example usage in services
from src.core.logging import github_logger

class GitHubServicePerformance:
    @PerformanceMonitor.track_performance(logger=github_logger)
    def get_user_repositories(self, username):
        # Existing repository retrieval logic
        pass
