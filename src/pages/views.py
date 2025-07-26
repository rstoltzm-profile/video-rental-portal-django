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
    """Films listing page view with optional search by film ID."""
    log_user_action(None, "Accessed films page")
    
    films_data = []
    error_message = None
    search_film_id = request.GET.get('film_id')
    
    if search_film_id:
        # Search for specific film by ID
        try:
            film_id = int(search_film_id)
            film_data, error_message = api_service.get_film_by_id(film_id)
            
            if film_data and not error_message:
                films_data = [film_data]  # Put single film in a list for template consistency
                log_user_action(None, f"Searched for film ID: {film_id}")
            elif not error_message:
                error_message = f"No film found with ID: {film_id}"
        except ValueError:
            error_message = "Please enter a valid film ID number"
    else:
        # Get all films
        films_data, error_message = api_service.get_films()
    
    # Format error message if needed
    if error_message:
        error_message = format_error_message(error_message, "Films API")
    
    context = {
        'films': films_data,
        'error_message': error_message,
        'total_films': len(films_data),
        'search_film_id': search_film_id,
        'is_search': bool(search_film_id)
    }
    
    return render(request, 'pages/films.html', context)


def customers(request):
    """Customers listing page view with optional search by customer ID."""
    log_user_action(None, "Accessed customers page")
    
    customers_data = []
    error_message = None
    search_customer_id = request.GET.get('customer_id')
    
    if search_customer_id:
        # Search for specific customer by ID
        try:
            customer_id = int(search_customer_id)
            customer_data, error_message = api_service.get_customer_by_id(customer_id)
            
            if customer_data and not error_message:
                customers_data = [customer_data]  # Put single customer in a list for template consistency
                log_user_action(None, f"Searched for customer ID: {customer_id}")
            elif not error_message:
                error_message = f"No customer found with ID: {customer_id}"
        except ValueError:
            error_message = "Please enter a valid customer ID number"
    else:
        # Get all customers
        customers_data, error_message = api_service.get_customers()
    
    # Format error message if needed
    if error_message:
        error_message = format_error_message(error_message, "Customers API")
    
    context = {
        'customers': customers_data,
        'error_message': error_message,
        'total_customers': len(customers_data),
        'search_customer_id': search_customer_id,
        'is_search': bool(search_customer_id)
    }

    return render(request, 'pages/customers.html', context)

def rentals(request):
    """Rentals listing page"""
    log_user_action(None, "Accessed rentals page")

    rentals_data = []
    error_message = None
    rentals_data, error_message = api_service.get_rentals()

    context = {
        'rentals': rentals_data,
        'error_message': error_message,
        'total_rentals': len(rentals_data),
    }

    return render(request, 'pages/rentals.html', context)

def stores(request):
    """stores listing page"""
    log_user_action(None, "Accessed stores page")

    return render(request, 'pages/stores.html')

def payments(request):
    """payments listing page"""
    log_user_action(None, "Accessed payments page")

    return render(request, 'pages/payments.html')
