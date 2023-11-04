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
from starlette.requests import Request


class KeycloakUtils:
    """
    This is a utility class for Keycloak integration with FastAPI. It provides methods to retrieve data from the authenticated request at any point in the application. The methods in this class will retrieve various details from the request such as user info, roles, groups, etc. from the token contained in the authenticated request.
    """

    @staticmethod
    def is_authenticated(request: Request):
        """
        Returns a flag indicating whether the request is authenticated or not.

        Args:
            request (`Request`): The request the user wants to check authentication status for.

        Returns:
            bool: True if request is authenticated, False otherwise.

        Example:
            >>> KeycloakUtils.is_authenticated(request)
            True
        """
        return bool(request.state.token_info)   
    
    @staticmethod
    def get_user_info(request: Request, attr: str):
        """
        Returns the user info for a given attribute from the authenticated request.

        Args:
            request (`Request`): The request the user wants to get the info from.
            attr (`str`): The attribute the user wants to get the info for.

        Returns:
            `str`: The info of the user for the given attribute.

        Example:
            >>> KeycloakUtils.get_user_info(request, "name")
            'John Smith'
        """
        user_info = request.state.token_info.get(attr) if KeycloakUtils.is_authenticated(request) else None
        return user_info if KeycloakUtils.is_authenticated(request) else None

    @staticmethod
    def has_role(request: Request, role: str):
        """
        Checks the request if the user has the specified role.

        Args:
            request (`Request`): The request where to extract user's roles.
            role (`str`): The role to check if the user has.

        Returns:
            bool: True if user has specified role, False otherwise.

        Example:
            >>> KeycloakUtils.has_role(request, "admin")
            True
        """
        roles = request.state.user_roles
        return role in roles if KeycloakUtils.is_authenticated(request) else False

    @staticmethod
    def is_in_group(request: Request, group: str):
        """
        Checks the request if the user is in the specified group.

        Args:
            request (`Request`): The request to check if a user is in a group.
            group (`str`): The group to check if the user is a member of.

        Returns:
            bool: True if user is in specified group, False otherwise.
        
        Example:
            >>> KeycloakUtils.is_in_group(request, "test_group")
            False
        """
        groups = request.state.token_info.get('groups', [])
        return group in groups if KeycloakUtils.is_authenticated(request) else False

    @staticmethod
    def get_user_id(request: Request):
        """
        Returns the user id from the authenticated request.

        Args:
            request (`Request`): The request which carries user's details.

        Returns:
            str: The user id of the authenticated user.

        Example:
            >>> KeycloakUtils.get_user_id(request)
            '123456'
        """
        user_id = request.state.token_info.get('sub') if KeycloakUtils.is_authenticated(request) else None
        return user_id if KeycloakUtils.is_authenticated(request) else None

    @staticmethod
    def get_user_email(request: Request):
        """
        Returns the user's email from the authenticated request.

        Args:
            request (`Request`): The request which carries user's details.

        Returns:
            str: The email of the authenticated user.

        Example:
            >>> KeycloakUtils.get_user_email(request)
            'user@example.com'
        """
        user_email = request.state.token_info.get('email') if KeycloakUtils.is_authenticated(request) else None
        return user_email if KeycloakUtils.is_authenticated(request) else None

    @staticmethod
    def get_user_first_name(request: Request):
        """
        Extracts the first name ('given_name') of the authenticated user from the request state.

        Args:
            request: The incoming server request.

        Returns:
            The first name of the user authenticated via Keycloak if authenticated, else None.
            
        Examples:
            first_name = KeycloakUtils.get_user_first_name(request)
        """
        user_first_name = request.state.token_info.get('given_name') if KeycloakUtils.is_authenticated(request) else None
        return user_first_name if KeycloakUtils.is_authenticated(request) else None

    @staticmethod
    def get_user_last_name(request: Request):
        """
        Extracts the last name ('family_name') of the authenticated user from the request state.

        Args:
            request: The incoming server request.

        Returns:
            The last name of the user authenticated via Keycloak if authenticated, else None.
            
        Examples:
            last_name = KeycloakUtils.get_user_last_name(request)
        """
        user_last_name = request.state.token_info.get('family_name') if KeycloakUtils.is_authenticated(request) else None
        return user_last_name if KeycloakUtils.is_authenticated(request) else None

    @staticmethod
    def get_user_full_name(request: Request):
        """
        Extracts the full name ('name') of the authenticated user from the request state.

        Args:
            request: The incoming server request.

        Returns:
            The full name of the user authenticated via Keycloak if authenticated, else None.
            
        Examples:
            full_name = KeycloakUtils.get_user_full_name(request)
        """
        user_full_name = request.state.token_info.get('name') if KeycloakUtils.is_authenticated(request) else None
        return user_full_name if KeycloakUtils.is_authenticated(request) else None
    
    @staticmethod
    def get_scope(request: Request):
        """
        Extracts the scope of the authenticated user from the request state.

        Args:
            request: The incoming server request.

        Returns:
            The scope of the user authenticated via Keycloak if authenticated, else None.
            
        Examples:
            scope = KeycloakUtils.get_scope(request)
        """
        scope = request.state.user_scope
        return scope if KeycloakUtils.is_authenticated(request) else None
    
    @staticmethod
    def get_user_verified(request: Request):
        """
        Extracts the verification status ('email_verified') of the authenticated user from the request state.

        Args:
            request: The incoming server request.

        Returns:
            The verification status of the user authenticated via Keycloak if authenticated, else None.
            
        Examples:
            is_verified = KeycloakUtils.get_user_verified(request)
        """
        user_verified = request.state.token_info.get('email_verified') if KeycloakUtils.is_authenticated(request) else None
        return user_verified if KeycloakUtils.is_authenticated(request) else None
    
    @staticmethod
    def get_active_user(request: Request):
        """
        Extracts the activity status ('active') of the authenticated user from the request state.

        Args:
            request: The incoming server request.

        Returns:
            The activity status of the user authenticated via Keycloak if authenticated, else None.
            
        Examples:
            is_active = KeycloakUtils.get_active_user(request)
        """
        active_user = request.state.token_info.get('active') if KeycloakUtils.is_authenticated(request) else None
        return active_user if KeycloakUtils.is_authenticated(request) else None
    
    @staticmethod
    def get_token_type(request: Request):
        """
        Extracts the token type ('typ') of the authenticated user from the request state.

        Args:
            request: The incoming server request.

        Returns:
            The token type of the user authenticated via Keycloak if authenticated, else None.
            
        Examples:
            token_type = KeycloakUtils.get_token_type(request)
        """
        token_type = request.state.token_info.get('typ') if KeycloakUtils.is_authenticated(request) else None
        return token_type if KeycloakUtils.is_authenticated(request) else None
    
    @staticmethod
    def get_resource_access(request: Request):
        """
        Extracts the resource access details of the authenticated user from the request state.

        Args:
            request: The incoming server request.

        Returns:
            The resource access details of the user authenticated via Keycloak if authenticated, else None.
            
        Examples:
            resource_access = KeycloakUtils.get_resource_access(request)
        """
        resource_access = request.state.token_info.get('resource_access') if KeycloakUtils.is_authenticated(request) else None
        return resource_access if KeycloakUtils.is_authenticated(request) else None