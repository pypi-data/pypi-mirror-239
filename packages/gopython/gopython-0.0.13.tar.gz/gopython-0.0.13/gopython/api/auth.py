import json
import requests
from requests import request
from gopython import const
from gopython.utils import Log
from gopython.dataclasses import User
from typing import List

class AuthAPI:
    def __init__(self):
        self.headers: dict = const.HEADERS
        self.log = Log()


    def signup(self,email: str, password: str, first_name: str, last_name: str) -> User:
        pass

    def login(self,email: str, password: str) -> User:
        #TODO: Need to add token here to call create user

        user_obj: User = User(
            email=email,
            password=password,
        )

        url = const.USER_LOGIN_API
        payload = json.dumps(user_obj.to_dict())
        response = request("POST", url, headers=self.headers, data=payload)


        if response.status_code == 200:
            user_data  = response.json().get('user')
            user_obj = User(
                user_id=user_data.get('id'),
                email=user_data.get('email'),
                first_name=user_data.get('first_name'),
                last_name=user_data.get('last_name'),
                status_code=response.status_code,
                password=password,
                message = "User Found!!"
            )
            self.log.print_log(user_obj)
            return user_obj
        
        user_obj.msg = "User Not Found!!"
        user_obj.status_code = response.status_code
        self.log.print_log(user_obj)

        return user_obj


    def _is_authorized(self, roles: List[str], permissions: List[str], user_id: str) -> bool:
    # Make a request to the API to get user roles and permissions
        try:
            url = const.USER_ROLE_PERMISSIONS_API
            payload = json.dumps({"id": user_id})
            response = request("POST", url, headers=self.headers, data=payload)

            print("_is_authorized", response.status_code)

            if response.status_code == 200:
                user_data = response.json()
                user_roles = user_data.get("user_roles", [])
                role_permissions = user_data.get("role_permissions", {})

                # Check if any role matches
                role_match = any(role in user_roles for role in roles)

                for role in roles:
                    # Check if any permission matches
                    permission_match = any(permission in role_permissions.get(role, []) for permission in permissions)

                # Return True if either role or permission matches
                if role_match and permission_match:
                    return True
        except requests.exceptions.RequestException as e:
            # Handle network or API request errors here
            print(f"Request error: {e}")
        return False
