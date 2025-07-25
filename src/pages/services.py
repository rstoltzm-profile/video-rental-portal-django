"""
API service module for handling external API calls to the video rental backend.
"""
import logging
from typing import Dict, List, Optional, Tuple, Any
import requests

logger = logging.getLogger(__name__)


class APIConfig:
    """Configuration for API connections."""
    BASE_URL = "http://localhost:8080"
    HEADERS = {
        "Content-Type": "application/json",
        "X-API-Key": "secure-dev-key-123"
    }
    DEFAULT_TIMEOUT = 10


class APIService:
    """Service class for handling API requests to the video rental backend."""

    def __init__(self, config: APIConfig = None):
        self.config = config or APIConfig()

    def _make_request(
            self,
            endpoint: str,
            method: str = 'GET',
            data: Dict = None
            ) -> Tuple[Optional[Any], Optional[str]]:
        """
        Make a request to the API and handle common errors.
        
        Args:
            endpoint: API endpoint path (e.g., '/v1/films')
            method: HTTP method (GET, POST, PUT, DELETE)
            data: Request data for POST/PUT requests
            
        Returns:
            Tuple of (response_data, error_message)
            - response_data: Parsed JSON response or None if error
            - error_message: Error description or None if successful
        """
        url = f"{self.config.BASE_URL}{endpoint}"
        error_message = None
        response_data = None

        try:
            if method.upper() == 'GET':
                response = requests.get(
                    url,
                    headers=self.config.HEADERS,
                    timeout=self.config.DEFAULT_TIMEOUT
                )
            elif method.upper() == 'POST':
                response = requests.post(
                    url,
                    headers=self.config.HEADERS,
                    json=data,
                    timeout=self.config.DEFAULT_TIMEOUT
                )
            elif method.upper() == 'PUT':
                response = requests.put(
                    url,
                    headers=self.config.HEADERS,
                    json=data,
                    timeout=self.config.DEFAULT_TIMEOUT
                )
            elif method.upper() == 'DELETE':
                response = requests.delete(
                    url,
                    headers=self.config.HEADERS,
                    timeout=self.config.DEFAULT_TIMEOUT
                )
            else:
                error_message = f"Unsupported HTTP method: {method}"
                logger.error(error_message)
                return None, error_message

            if response.status_code == 200:
                response_data = response.json()
                logger.info("Successfully completed %s request to %s", method, endpoint)
            else:
                error_message = f"API returned status code: {response.status_code}"
                logger.error("API error for %s %s: %s", method, endpoint, error_message)

        except requests.exceptions.ConnectionError:
            error_message = f"Unable to connect to the API server at {self.config.BASE_URL}. \
                              Please ensure the API is running."
            logger.error("Connection error for %s %s: %s", method, endpoint, error_message)
        except requests.exceptions.Timeout:
            error_message = "Request timed out. The API server may be slow to respond."
            logger.error("Timeout error for %s %s: %s", method, endpoint, error_message)
        except requests.exceptions.RequestException as e:
            error_message = f"An error occurred while making the request: {str(e)}"
            logger.error("Request error for %s %s: %s", method, endpoint, error_message)
        except ValueError as e:
            error_message = f"Invalid JSON response: {str(e)}"
            logger.error("JSON parsing error for %s %s: %s", method, endpoint, error_message)

        return response_data, error_message

    def get_films(self) -> Tuple[List[Dict], Optional[str]]:
        """
        Get all films from the API.
        
        Returns:
            Tuple of (films_list, error_message)
        """
        response_data, error_message = self._make_request('/v1/films')

        if response_data is not None:
            if isinstance(response_data, list):
                logger.info("Retrieved %d films from API", len(response_data))
                return response_data, None
            else:
                error_message = "Expected list of films but received different format"
                logger.error(error_message)
                return [], error_message

        return [], error_message

    def get_film_by_id(self, film_id: int) -> Tuple[Optional[Dict], Optional[str]]:
        """
        Get a specific film by ID.
        
        Args:
            film_id: The ID of the film to retrieve
            
        Returns:
            Tuple of (film_data, error_message)
        """
        response_data, error_message = self._make_request(f'/v1/films/{film_id}')
        return response_data, error_message

    def search_films(self, query: str) -> Tuple[List[Dict], Optional[str]]:
        """
        Search for films.
        
        Args:
            query: Search query string
            
        Returns:
            Tuple of (films_list, error_message)
        """
        response_data, error_message = self._make_request(f'/v1/films/search?q={query}')

        if response_data is not None:
            if isinstance(response_data, list):
                return response_data, None
            else:
                error_message = "Expected list of films but received different format"
                logger.error(error_message)
                return [], error_message

        return [], error_message

    def get_customers(self) -> Tuple[List[Dict], Optional[str]]:
        """
        Get all customers from the API.
        
        Returns:
            Tuple of (customers_list, error_message)
        """
        response_data, error_message = self._make_request('/v1/customers')

        if response_data is not None:
            if isinstance(response_data, list):
                logger.info("Retrieved %d customers from API", len(response_data))
                return response_data, None
            else:
                error_message = "Expected list of customers but received different format"
                logger.error(error_message)
                return [], error_message

        return [], error_message

    def health_check(self) -> Tuple[bool, Optional[str]]:
        """
        Check if the API server is healthy.
        
        Returns:
            Tuple of (is_healthy, error_message)
        """
        response_data, error_message = self._make_request('/health')

        if response_data is not None:
            return True, None
        else:
            return False, error_message


# Global instance for use in views
api_service = APIService()
