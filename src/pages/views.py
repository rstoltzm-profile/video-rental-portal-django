from django.shortcuts import render
import logging
import requests

logger = logging.getLogger(__name__)

def home(request):
    return render(request, 'pages/home.html')

def films(request):
    BASE_URL = "http://localhost:8080"
    HEADERS = {
        "Content-Type": "application/json",
        "X-API-Key": "secure-dev-key-123"
    }
    
    films_data = []
    error_message = None
    
    try:
        url = f"{BASE_URL}/v1/films"
        response = requests.get(url, headers=HEADERS, timeout=10)
        
        if response.status_code == 200:
            films_data = response.json()
            logger.info("Successfully retrieved %d films", len(films_data))
        else:
            error_message = f"API returned status code: {response.status_code}"
            logger.error(error_message)
            
    except requests.exceptions.ConnectionError:
        error_message = "Unable to connect to the API server. Please ensure the API is running on localhost:8080"
        logger.error(error_message)
    except requests.exceptions.Timeout:
        error_message = "Request timed out. The API server may be slow to respond."
        logger.error(error_message)
    except requests.exceptions.RequestException as e:
        error_message = f"An error occurred while fetching films: {str(e)}"
        logger.error(error_message)
    
    context = {
        'films': films_data,
        'error_message': error_message,
        'total_films': len(films_data)
    }
    
    return render(request, 'pages/films.html', context)

def customers(request):
    return render(request, 'pages/customers.html')
