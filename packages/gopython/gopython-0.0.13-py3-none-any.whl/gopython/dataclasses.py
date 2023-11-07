from typing import List
class User:
    def __init__(self, email: str = None, password: str = None, first_name:str  = None, last_name: str = None, user_id:int=None, status_code:int=None, message:str=None):
        self.email: str = email
        self.password: str = password
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.status_code = status_code
        self.message = message
        self.user_id = user_id

    def to_dict(self) -> dict:
        user_dict =  {
            "email": self.email,
            "password": self.password,
        }
        if self.user_id is not None:
            user_dict["id"] = self.user_id
    
        if self.first_name is not None:
            user_dict["first_name"] = self.first_name

        if self.last_name is not None:
            user_dict["last_name"] = self.last_name

        if self.status_code is not None:
            user_dict["status_code"] = self.status_code

        if self.message is not None:
            user_dict["message"] = self.message
        return user_dict

class UserRole:
    def __init__(self, user_id: int = None,user_rolde_id: int = None, user_roles: list = None ,status_code:int=None, message:str=None):
        self.user_id: int = user_id
        self.user_roles: list = user_roles
        self.status_code: int = status_code
        self.message: str = message

    def get_dict(self) -> dict:
        user_role_dict =  {
            "user_id": self.user_id,
            "user_roles": self.user_roles
        }
        
        if user_rolde_id is not None:
            user_role_dict["id"] = self.user_rolde_id
        if self.status_code is not None:
            user_role_dict["status_code"] = self.status_code
        if self.message is not None:
            user_role_dict["message"] = self.message
        return user_role_dict


class Role:
    def __init__(self, name: str, description: str, role_id:int = None ,status_code:int=None, message:str=None):
        #TODO: Short and Long Description can be added
        self.name = name
        self.description = description
        self.role_id = role_id
        self.status_code = status_code
        self.message = message

    def get_dict(self):
        role_dict =  {
            "name": self.name,
            "description": self.description
        }

        if self.id is not None:
            role_dict["id"] = self.id
        if self.status_code is not None:
            role_dict["status_code"] = self.status_code
        if self.message is not None:
            role_dict["message"] = self.message
        


class RolePermission:
    def __init__(self, role_permissions_id:int = None, role_id: int = None, role_permissions: List[int] = None, status_code:int=None, message:str=None):
        #TODO: Short and Long Description can be added
        self.id = role_permissions_id 
        self.role_id = role_id
        self.role_permissions = role_permissions
        self.status_code = status_code
        self.message = message


    def get_dict() -> dict:
        role_permisions_dict = {
            "role_id": self.role_id,
            "role_permissions": self.role_permissions
        }
        if self.id is not None:
            role_permisions_dict["id"] = self.id
        if self.status_code is not None:
            role_permisions_dict["status_code"] = self.status_code
        if self.message is not None:
            role_permisions_dict["message"] = self.message
        
        return role_permisions_dict


class Permission:
    def __init__(self, name: str, description: str):
        #TODO: Short and Long Description can be added
        self.name = name
        self.description = description

    def get_dict(self):
        return {
            "name": self.name,
            "description": self.description
        }