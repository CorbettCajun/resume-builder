import time
from functools import wraps
from typing import Callable, Any, Optional
from src.core.logging import error_logger

class CircuitBreaker:
    """
    Implement Circuit Breaker pattern for resilient API calls
    
    Principles:
    - Prevent cascading failures
    - Provide graceful degradation
    - Automatic recovery
    """
    def __init__(
        self, 
        failure_threshold: int = 3, 
        recovery_time: float = 60.0
    ):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.last_failure_time: Optional[float] = None
        self.state = 'CLOSED'

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Check if circuit is open
            if self.state == 'OPEN':
                if time.time() - self.last_failure_time > self.recovery_time:
                    self.state = 'HALF_OPEN'
                else:
                    error_logger.warning(f"Circuit OPEN for {func.__name__}")
                    raise CircuitBreakerError(f"Service {func.__name__} is temporarily unavailable")

            try:
                result = func(*args, **kwargs)
                # Reset on success
                if self.state == 'HALF_OPEN':
                    self.state = 'CLOSED'
                    self.failure_count = 0
                return result
            
            except Exception as e:
                self.failure_count += 1
                error_logger.error(f"Error in {func.__name__}: {e}")

                if self.failure_count >= self.failure_threshold:
                    self.state = 'OPEN'
                    self.last_failure_time = time.time()
                
                raise

        return wrapper

def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    Retry decorator with exponential backoff
    
    :param max_attempts: Maximum retry attempts
    :param delay: Initial delay between retries
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            current_delay = delay

            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    error_logger.warning(f"Attempt {attempts} failed: {e}")
                    
                    if attempts == max_attempts:
                        raise
                    
                    time.sleep(current_delay)
                    current_delay *= 2  # Exponential backoff
        
        return wrapper
    return decorator

class CircuitBreakerError(Exception):
    """Custom exception for circuit breaker state"""
    pass
