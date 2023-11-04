from typing import Dict, Any, Optional
import requests
from ..configuration import Config, ConfigVariable

# class APIResponse:
#     def __init__(
#         self, 
#         status_code: int, 
#         headers:     Dict[str, Any], 
#         content:     Optional[bytes] = None,
#         body:        Optional[Dict[str, Any]] = None
#     ):
#         self.status_code = status_code
#         self.headers     = headers
#         self.content     = content
#         self.body        = body

def profile():
    profile = Config.get_variable(ConfigVariable.PROFILE) or 'default'
    return profile

def api_key():
        api_key = Config.get_variable(ConfigVariable.API_KEY, profile())

        # Throw error if no API key is found
        if api_key is None:
            raise Exception('No Cortex credentials found.')
        
        return api_key

def api_url():
        api_url = Config.get_variable(ConfigVariable.API_URL, profile())

        # Throw error if no API URL is found
        if api_url is None:
            raise Exception('No Cortex credentials found.')
        
        return api_url

class APIResource:
    """
    Base class for Cortex API resources.
    """
    
    @classmethod
    def _to_strong_type(
        cls,
        json,
        return_type,
        collection_field: str = 'documents'
    ):
        """
        Helper to return a typed result from a Cortex API call.
        """
        
        # This relies on the API returning things in a consistent format
        if {'documents', 'totalDocuments'} <= json.keys() and return_type is not None:
            typed_objects = []
            for resource in json[collection_field]:
                typed_objects.append(return_type(**resource))

            return typed_objects

        return return_type(**json)

    @classmethod
    def _request_raw(
        cls,
        method:  str,
        url:     str,
        params:  Optional[Dict[str, Any]] = None,
        json:    Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        data:    Optional[Any]            = None
    ) -> requests.Response: # pyright: ignore[reportGeneralTypeIssues]
        """
        Raw HTTP request.
        
        This is essentially just a straight HTTP request that raises exceptions
        on non-200 status codes.
        """
        response = requests.request(
            method  = method,
            url     = url,
            params  = params,
            json    = json,
            headers = headers,
            data    = data,
            timeout = 15
        )

        if response.status_code >= 200 and response.status_code <= 299:
            return response

        # This seems to cause a false positive linting, as this will raise
        # an exception if the status code is not in the 200 range, but it can't
        # be inferred that it terminates control flow.
        response.raise_for_status()

    @classmethod
    def _request(
        cls,
        method:  str,
        path:    str,
        params:  Optional[Dict[str, Any]] = None,
        json:    Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, Any]] = None,
        data:    Optional[Any] = None
    ):
        """
        Wrapper for a Cortex HTTP request. Implicitly handles API authorization.
        """

        # Allows passing just the paths instead of full API endpoints
        if not path.startswith('https://'):
            url = f'{api_url()}{path}'
        else:
            url = path

        # Strips out any None values from the JSON payload and appends Cortex
        # authorization headers
        return cls._request_raw(
            method  = method,
            url     = url,
            params  = params,
            data    = data,
            json    = json if json is None else {k: v for k, v in json.items() if v is not None},  # noqa: E501
            headers = headers or {} | {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {api_key()}',
            }
        )

    @classmethod
    def _generic_get(
        cls,
        path:             str,
        params:           Optional[Dict[str, Any]] = None,
        return_type:      Any                      = None,  # Fix
        collection_field: str                      = 'documents'
    ):
        """
        Wrapper around GET requests to the Cortex API.

        Args:
            path (str):
            The path of the endpoint.

            params (Optional[Dict[str, Any]]):
            The query parameters to include in the request.

            return_type (Any):
            The JSON payload to include in the request.
        """
        response      = cls._request(method='get', path=path, params=params)
        # TODO: Catch 'status' errors here
        typed_objects = cls._to_strong_type(
            json             = response.json(),
            return_type      = return_type,
            collection_field = collection_field
        )

        return typed_objects

    @classmethod
    def _generic_post(
        cls,
        path:   str,
        params: Optional[Dict[str, Any]] = None,
        json:   Optional[Dict[str, Any]] = None
    ):
        """
        Wrapper around POST requests to the Cortex API.

        Args:
            path (str):
            The path of the endpoint.

            params (Optional[Dict[str, Any]]):
            The query parameters to include in the request.

            json (Optional[Dict[str, Any]]):
            The JSON payload to include in the request.
        """
        return cls._request(
            method = 'post',
            path   = path,
            params = params,
            json   = json
        )

    @classmethod
    def _generic_put(
        cls,
        path:   str,
        params: Optional[Dict[str, Any]] = None,
        json:   Optional[Dict[str, Any]] = None
    ):
        """
        Wrapper around PUT requests to the Cortex API.

        Args:
            path (str):
            The path of the endpoint.

            params (Optional[Dict[str, Any]]):
            The query parameters to include in the request.

            json (Optional[Dict[str, Any]]):
            The JSON payload to include in the request.
        """
        return cls._request(
            method = 'put',
            path   = path,
            params = params,
            json   = json
        )

    @classmethod
    def _generic_delete(
        cls,
        path: str
    ):
        """
        Wrapper around DELETE requests to the Cortex API.

        Args:
            path (str):
            The path of the endpoint.

            params (str):
            The value of the secret.
        """
        return cls._request(
            method = 'delete',
            path   = path
        )
