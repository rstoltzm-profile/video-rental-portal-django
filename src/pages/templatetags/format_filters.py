"""
Custom template filters for the video rental portal.
"""
from django import template
import re
from datetime import datetime

register = template.Library()


@register.filter
def format_phone(phone):
    """
    Format phone number to a readable format.
    
    Examples:
    - "+1234567890" -> "+1 (234) 567-8900"
    - "1234567890" -> "(123) 456-7890"
    - "+12345678901" -> "+1 (234) 567-8901"
    """
    if not phone:
        return "N/A"
    
    # Remove all non-digit characters except +
    cleaned = re.sub(r'[^\d+]', '', str(phone))
    
    if not cleaned:
        return phone
    
    # Handle international format starting with +
    if cleaned.startswith('+'):
        if len(cleaned) == 12 and cleaned.startswith('+1'):  # US/Canada format
            # +1234567890 -> +1 (234) 567-8900
            return f"+1 ({cleaned[2:5]}) {cleaned[5:8]}-{cleaned[8:12]}"
        elif len(cleaned) >= 11:  # Other international formats
            country_code = cleaned[1:3] if len(cleaned) > 11 else cleaned[1:2]
            number = cleaned[len(country_code)+1:]
            if len(number) == 10:
                return f"+{country_code} ({number[:3]}) {number[3:6]}-{number[6:]}"
            else:
                return f"+{country_code} {number}"
        else:
            return phone
    
    # Handle domestic format (10 digits)
    elif len(cleaned) == 10:
        # 1234567890 -> (123) 456-7890
        return f"({cleaned[:3]}) {cleaned[3:6]}-{cleaned[6:]}"
    
    # Handle 11 digits starting with 1 (US format with country code)
    elif len(cleaned) == 11:
        # 11234567890 -> +1 (123) 456-7890
        return f"+ {cleaned[0:1]} ({cleaned[1:4]}) {cleaned[4:7]}-{cleaned[7:]}"
    
    # Handle 11 digits starting with 1 (US format with country code)
    elif len(cleaned) == 12:
        # 11234567890 -> +1 (123) 456-7890
        return f"+ {cleaned[0:2]} ({cleaned[2:5]}) {cleaned[5:8]}-{cleaned[8:]}"
    
    # Return original if doesn't match expected patterns
    return phone


@register.filter
def format_datetime(value, format_string="M d, Y g:i A"):
    """
    Format datetime with a default format that shows date and time.
    
    Args:
        value: datetime string or object
        format_string: Django date format string
    """
    if not value:
        return "N/A"
    
    # If it's already a datetime object, format it
    if hasattr(value, 'strftime'):
        return value.strftime('%b %d, %Y %I:%M %p')
    
    # If it's a string, try to parse it
    try:
        if isinstance(value, str):
            # Try common datetime formats
            formats_to_try = [
                '%Y-%m-%dT%H:%M:%S%z',        # 2022-02-14T08:16:03-07:00
                '%Y-%m-%dT%H:%M:%S.%f%z',     # With microseconds and timezone
                '%Y-%m-%dT%H:%M:%S.%fZ',      # UTC with microseconds
                '%Y-%m-%dT%H:%M:%SZ',         # UTC without microseconds
                '%Y-%m-%d %H:%M:%S',          # Simple format
            ]
            
            for fmt in formats_to_try:
                try:
                    dt = datetime.strptime(value, fmt)
                    return dt.strftime('%b %d, %Y %I:%M %p')
                except ValueError:
                    continue
        
        # Fall back to Django's date filter behavior
        return value
    except:
        return value


@register.filter
def format_date_short(value):
    """
    Format date in short format: Jan 15, 2025
    """
    if not value:
        return "N/A"
    
    if hasattr(value, 'strftime'):
        return value.strftime('%b %d, %Y')
    
    return value


@register.filter
def format_currency(value):
    """
    Format currency values.
    
    Examples:
    - 1234.56 -> $1,234.56
    - 1000 -> $1,000.00
    """
    if value is None or value == '':
        return "N/A"
    
    try:
        amount = float(value)
        return f"${amount:,.2f}"
    except (ValueError, TypeError):
        return value


@register.filter
def truncate_smart(value, length=50):
    """
    Smart truncate that tries to break at word boundaries.
    """
    if not value or len(value) <= length:
        return value
    
    truncated = value[:length]
    # Try to break at the last space
    last_space = truncated.rfind(' ')
    if last_space > length * 0.7:  # Only if we don't lose too much
        truncated = truncated[:last_space]
    
    return truncated + "..."


@register.filter
def format_boolean(value):
    """
    Format boolean values with icons.
    """
    if value is True:
        return "✅ Yes"
    elif value is False:
        return "❌ No"
    else:
        return "N/A"
