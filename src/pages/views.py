import logging
from django.shortcuts import render
from .services import api_service
from .utils import log_user_action, format_error_message

logger = logging.getLogger(__name__)


def home(request):
    """Home page view."""
    log_user_action(None, "Accessed home page")
    return render(request, 'pages/home.html')


def films(request):
    """Films listing page view."""
    log_user_action(None, "Accessed films page")

    films_data, error_message = api_service.get_films()

    # Format error message if needed
    if error_message:
        error_message = format_error_message(error_message, "Films API")

    context = {
        'films': films_data,
        'error_message': error_message,
        'total_films': len(films_data)
    }

    return render(request, 'pages/films.html', context)


def customers(request):
    """Customers listing page view."""
    log_user_action(None, "Accessed customers page")

    customers_data, error_message = api_service.get_customers()

    # Format error message if needed
    if error_message:
        error_message = format_error_message(error_message, "Customers API")

    context = {
        'customers': customers_data,
        'error_message': error_message,
        'total_customers': len(customers_data)
    }

    return render(request, 'pages/customers.html', context)
