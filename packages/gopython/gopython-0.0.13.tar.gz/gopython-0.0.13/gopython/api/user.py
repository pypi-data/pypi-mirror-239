
import json
from gopython import const
from gopython.utils import Log
from gopython.dataclasses import User, UserRole
dataclasses
from requests import requests
from typing import List






class UserAPI:
    
    def __init__(self):
        #TODO: Token Field here to user auth
        self.headers: dict = const.HEADERS
        self.log = Log()

    def get_user_by_id(self,user_id:int) -> User:
        #TODO: Need to udpate from POST to GET

        url = const.GET_USER_BY_ID_API
        payload = json.dumps({"id": user_id})
        response = requests.request("POST", url, headers=self.headers, data=payload)

        data  = response.json().get('user')

        if response.status_code == 200:
            user_obj: User = User(
                user_id = data.get('id'),
                email= data.get('email'),
                password=date.get('password'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                status_code= response.status_code,
                message = "User Found!!"
            )
            self.log.print_log(user_obj)
            return user_obj

        user_obj: User = User(
            status_code= response.status_code,
            message = "User Not Found!!"
        )
        self.log.print_log(user_obj)
        return user_obj


    def get_user_role_by_id(self,user_id:int) -> User:
        #TODO: Need to udpate from POST to GET
        # TODO: Need to find how many roles are can be added and response

        url = const.GET_USER_ROLE_BY_ID
        payload = json.dumps({"id": user_id})
        response = requests.request("POST", url, headers=self.headers, data=payload)

        
        if response.status_code == 200:
            user_role_res = response.json().get('roles')
            user_obj: User = UserRole(
                user_id = user_role_res.get('user_id'),
                user_roles=user_role_res.get('user_roles'),
                status_code= response.status_code,
                message = "User Role Found!!"

            )
            self.log.print_log(user_obj)
            return user_obj

        user_obj: User = User(
            status_code= response.status_code,
            message = "User Role Not Found!!"
        )
        self.log.print_log(user_obj)
        return user_obj



    def create_user(self,email: str, password: str, first_name: str, last_name: str) -> User:
        #TODO: Need to add token here to call create user

        user_obj: User = User(
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        url = const.CREATE_USER
        payload = json.dumps(user_obj.get_dict())
        response = requests.request("POST", url, headers=self.headers, data=payload)


        if response.status_code == 200:
            user_data  = response.json().get('user')
            user_obj.user_id = user_data.get('id')
            user_ubj.msg = "User Created!!"
        else:
            user_ubj.msg = "User Creation Failed!!"

        user_obj.status_code = response.status_code
        self.log.print_log(user_obj)

        return user_obj

    def create_user_role(self,user_id: int,user_roles: List[int]) -> UserRole:

        #TODO: Need to add token here to call create user role and need proper message from api
        
        user_role_obj:UserRole = UserRole(
            user_id=user_id,
            user_roles=user_roles
        )
        url = const.CREATE_USER_ROLE_API
        payload = json.dumps(user_role_obj.get_dict())
        response = requests.request("POST", url, headers=self.headers, data=payload)

        if response.status_code == 200:
            user_role_data = response.json().get('user_role')
            user_role_obj.id = user_role_data.get("id")
            user_role_obj.message = "User Role Created!!"
        else:
            user_role_obj.message = "User Role Creation Failed!!"

        user_role_obj.status_code = response.status_code
        self.log.print_log(user_role_obj)
        return user_role_obj