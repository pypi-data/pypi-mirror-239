"""
MIT License

Copyright (c) 2023 Alexandre Meline <alexandre.meline.dev@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from keycloak import KeycloakOpenID
from starlette.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from typing import Type
from pydantic import BaseModel

class KeycloakFastSSOMiddleware(BaseHTTPMiddleware):
    """
    This is a middleware class for integrating Keycloak with FastAPI for Single-Sign-On (SSO) Authentication. 
    Any incoming requests will be passed through this middleware to check for the necessary authentication details
    provided by Keycloak.
    
    This class also offers optional functionalities related to User Model initialization and to user verification.
    """
    def __init__(self, app, server_url, client_id, realm_name, client_secret_key, user_model: Type[BaseModel] = None, 
                 create_user: bool = False, enable_user_verification=False):
        """
        Constructor for KeycloakFastSSOMiddleware class. Initializes Keycloak middleware and checks if middleware
        was initialized successfully.

        Args:
            app (`obj`): The instantiated FastAPI application.
            server_url (`str`): The URL to Keycloak server.
            client_id (`str`): The client ID of the Keycloak client.
            realm_name (`str`): The realm name of the Keycloak server.
            client_secret_key (`str`): The client secret key provided by Keycloak server for authentication.
            user_model (`obj`, optional): User model class. Defaults to None.
            create_user (`bool`, optional): Flag to decide if creating user is allowed. Defaults to False.
            enable_user_verification (`bool`, optional): Flag to decide if user's email verification is enabled or not.\n Defaults to False.

        Raises:
            Exception: Raises an exception if failed to initialize the Keycloak middleware.
        """
        super().__init__(app)
        try:
            self.keycloak_openid = KeycloakOpenID(server_url=server_url, 
                                                client_id=client_id, 
                                                realm_name=realm_name, 
                                                client_secret_key=client_secret_key) 

        except Exception as _:
            raise Exception('Keycloak middleware failed to initialize.')
        
        self.user_model = user_model
        self.create_user = create_user
        self.enable_user_verification = enable_user_verification

    async def dispatch(self, request, call_next):
        """
        Async function that processes incoming HTTP request and if necessary verifies the user.

        Args:
            request (`obj`): The incoming HTTP request
            call_next (`obj`): The middleware to be launched after this one

        Returns:
            `obj`: Returns the response that was created by this middleware or in case of failed
            authentication, return respective HTTPException.

        Raises:
            HTTPException: If user verification failed.
        """
        if request.url.path in ['/docs', '/openapi.json', '/redoc', '/get-login-url']:
            return await call_next(request)

        auth_header = None
        # Check for token in headers, query params, cookies, and body
        for source in ['headers', 'query_params', 'body']:
            attribute = getattr(request, source)
            token_value = attribute.get('token')
            if token_value:
                auth_header = f'Bearer {token_value}'
                break
        
        if not auth_header:
            return self.unauthorized_response()

        scheme, token = auth_header.split()
        if scheme.lower() != "bearer":
            return self.unauthorized_response()

        try:
            self.token_info = self.keycloak_openid.introspect(token)
            assert self.token_info['active']
        except Exception as _:
            return self.invalid_token_response()

        self.set_request_state(request)

        response = await call_next(request)

        return response
    
    def get_token(self, request):
         # Check for token in headers, query params, cookies, and body
        for source in ['headers', 'query_params']:
            attribute = getattr(request, source)
            token_value = attribute.get('token')
            if token_value:
                auth_header = f'Bearer {token_value}'
                return auth_header
            else:
                return None
        

    def unauthorized_response(self):
        """
        Creates a JSONResponse object indicating unauthorized response.
        
        Returns:
            JSONResponse object with 401 status and detail of "Non autorisé".
        """
        return JSONResponse({"detail": "Non autorisé"}, status_code=401)

    def invalid_token_response(self):
        """
        Creates a JSONResponse object indicating response for invalid token.
        
        Returns:
            JSONResponse object with 401 status and detail of "Token invalide".
        """
        return JSONResponse({"detail": "Token invalide"}, status_code=401)

    def unverified_user_response(self):
        """
        Return an unverified user response.
        
        Returns:
            A JSON response with a 401 status code.
        """
        return JSONResponse({"detail": "Utilisateur non vérifié"}, status_code=401)

    def set_request_state(self, request):
        """
        Update the state of the given request with information extracted from the token.
        
        Args:
            request (`obj`): The incoming request.
        """
        request.state.token_info = self.token_info
        # roles
        request.state.user_roles = self.get_roles()
        # groups
        request.state.user_groups = self.get_groups()
        # scope
        request.state.user_scope = self.get_scope()

        if self.user_model and self.create_user:
            user_data = request.state.token_info
            # A minimal data set to create a user
            user_data.update({
                'username': user_data.get('preferred_username'),
                'email': user_data.get('email')
            })
            user = self.user_model(**user_data)
            user.save()
            request.state.user = user

    def email_verified(self):
        """
        Check whether the user email is verified or not.
        
        Returns:
            `bool`: Returns True if the email for user is verified, False otherwise.
        """
        return self.token_info.get('email_verified')

    def get_roles(self):
        """
        Extract roles of the user from the token.
        
        Returns:
            `list`: A list of roles extracted from the token of the user.
        """
        return list(self.token_info.get('resource_access', {}).get(self.keycloak_openid.client_id, {}).get('roles', []))

    def get_groups(self):
        """
        Extract groups of the user from the token.
        
        Returns:
            `list`: A list of groups extracted from the token of the user.
        """
        return self.token_info.get('groups', [])
    
    def get_scope(self):
        """
        Extract the scope of the user from the token.
        
        Returns:
            `list`: A list of user's scopes extracted from the token.
        """
        return self.token_info.get('scope', [])

    def get_user_info(self, attr):
        """
        Extract user information of specific attribute from the token. 
        
        Args:
            attr (`str`): The attribute to extract user info for.
            
        Returns:
            `str` or `None`: User information of the given attribute if it exists, otherwise None.
        """
        return self.token_info.get(attr, None)