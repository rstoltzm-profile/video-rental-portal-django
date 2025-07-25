"""
Utility functions for the video rental portal application.
"""
import logging
from typing import Dict, Any, Optional
from django.conf import settings

logger = logging.getLogger(__name__)


def format_film_data(film: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format film data for display in templates.
    
    Args:
        film: Raw film data from API
        
    Returns:
        Formatted film data
    """
    if not film:
        return {}

    return {
        'title': film.get('title', 'N/A'),
        'description': film.get('description', ''),
        'release_year': film.get('release_year', 'N/A'),
        'language': film.get('language', 'N/A'),
        'rating': film.get('rating', 'N/A'),
        'categories': film.get('categories', []),
        'actors': film.get('actors', [])
    }


def format_customer_data(customer: Dict[str, Any]) -> Dict[str, Any]:
    """
    Format customer data for display in templates.
    
    Args:
        customer: Raw customer data from API
        
    Returns:
        Formatted customer data
    """
    if not customer:
        return {}

    return {
        'id': customer.get('id', 'N/A'),
        'first_name': customer.get('first_name', 'N/A'),
        'last_name': customer.get('last_name', 'N/A'),
        'email': customer.get('email', 'N/A'),
        'full_name': f"{customer.get('first_name', '')} {customer.get('last_name', '')}".strip()
    }


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to a maximum length with ellipsis.
    
    Args:
        text: Text to truncate
        max_length: Maximum length before truncation
        
    Returns:
        Truncated text with ellipsis if needed
    """
    if not text or len(text) <= max_length:
        return text

    return text[:max_length-3] + "..."


def get_pagination_info(total_items: int, page: int = 1, per_page: int = 20) -> Dict[str, Any]:
    """
    Calculate pagination information.
    
    Args:
        total_items: Total number of items
        page: Current page number (1-based)
        per_page: Items per page
        
    Returns:
        Dictionary with pagination info
    """
    total_pages = (total_items + per_page - 1) // per_page
    start_item = (page - 1) * per_page + 1
    end_item = min(page * per_page, total_items)

    return {
        'current_page': page,
        'total_pages': total_pages,
        'per_page': per_page,
        'total_items': total_items,
        'start_item': start_item,
        'end_item': end_item,
        'has_previous': page > 1,
        'has_next': page < total_pages,
        'previous_page': page - 1 if page > 1 else None,
        'next_page': page + 1 if page < total_pages else None
    }


def log_user_action(user_id: Optional[int], action: str, details: str = None):
    """
    Log user actions for audit purposes.
    
    Args:
        user_id: ID of the user performing the action
        action: Description of the action
        details: Additional details about the action
    """
    log_message = f"User {user_id or 'Anonymous'} performed action: {action}"
    if details:
        log_message += f" - {details}"

    logger.info(log_message)


def safe_get(data: Dict[str, Any], key: str, default: Any = None) -> Any:
    """
    Safely get a value from a dictionary with optional default.
    
    Args:
        data: Dictionary to get value from
        key: Key to look for
        default: Default value if key not found
        
    Returns:
        Value from dictionary or default
    """
    if not isinstance(data, dict):
        return default

    return data.get(key, default)


def format_error_message(error: str, context: str = None) -> str:
    """
    Format error messages for user display.
    
    Args:
        error: Raw error message
        context: Additional context about where the error occurred
        
    Returns:
        Formatted error message
    """
    if context:
        return f"{context}: {error}"
    return error


def is_debug_mode() -> bool:
    """
    Check if the application is running in debug mode.
    
    Returns:
        True if in debug mode, False otherwise
    """
    return getattr(settings, 'DEBUG', False)
