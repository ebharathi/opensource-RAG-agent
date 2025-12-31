import functools
from typing import Callable
from utils.logger import logger


def log_tool_call(func: Callable) -> Callable:
    """
    Decorator to automatically log tool calls.
    Logs [TOOL START], [TOOL END], and [TOOL ERROR] for all tool functions.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        tool_name = func.__name__
        
        # Format arguments for logging
        args_str = ", ".join([str(arg) for arg in args])
        kwargs_str = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        all_args = ", ".join(filter(None, [args_str, kwargs_str]))
        
        # Log tool start
        logger.info(f"[TOOL START] {tool_name}: {all_args}")
        
        try:
            # Execute the tool function
            result = func(*args, **kwargs)
            
            result_str = str(result)
            len_result_str = len(result_str)
            
            # Log tool end
            logger.info(f"[TOOL END] {tool_name}: {result_str[:100]}{' (truncated)' if len_result_str > 100 else ''}")
            
            return result
            
        except Exception as e:
            # Log tool error
            logger.error(f"[TOOL ERROR] {tool_name}: {str(e)}")
            raise
    
    return wrapper
