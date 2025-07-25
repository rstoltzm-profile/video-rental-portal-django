import logging
from django.shortcuts import render
from django.http import JsonResponse


# Import the API service from pages app
from pages.services import api_service

logger = logging.getLogger(__name__)


def health_check(request):
    """
    Health check endpoint that verifies API connectivity.
    Returns JSON response indicating system status.
    """
    is_healthy, error_message = api_service.health_check()

    status_code = 200 if is_healthy else 503

    response_data = {
        'status': 'ok' if is_healthy else 'error',
        'api_connection': 'connected' if is_healthy else 'disconnected',
        'api_url': api_service.config.BASE_URL,
        'message': 'All systems operational' if is_healthy else error_message
    }

    logger.info("Health check performed - Status: %s", response_data['status'])

    return JsonResponse(response_data, status=status_code)


def health_page(request):
    """
    Health check page for web interface.
    Shows system status in a user-friendly format.
    """
    is_healthy, error_message = api_service.health_check()

    context = {
        'is_healthy': is_healthy,
        'error_message': error_message,
        'api_url': api_service.config.BASE_URL,
        'status_text': 'Operational' if is_healthy else 'Error'
    }

    return render(request, 'up/health.html', context)
