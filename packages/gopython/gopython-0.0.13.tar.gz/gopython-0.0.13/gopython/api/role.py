import json
from gopython import const
from requests import requests
from gopython.utils import Log
from gopython.dataclasses import Role, RolePermission


class RoleAPI:
    def __init__(self):
        self.headers = const.HEADERS
        self.log = Log()
        

    def create_role(self) -> Role:
        url = const.CREATE_ROLE_API

        role_obj:Role = Role(name=name,description=description)
        payload = json.dumps(self.self.role_obj.get_dict())
        response = requests.request("POST", url, headers=self.headers, data=payload)

        if response.status_code == 200:
            role_data = response.json()['role']
            role_obj.id = role_data.get("id")
            role_obj.message = "Role Created!!"
        else:
            role_obj.message = "Role Creation Failed!!"
        
        role_obj.status_code = response.status_code
        self.log.print_log(role_obj)
        return role_obj

    def create_role_permissions(self,role_id:int, role_permissions:List[int]) -> RolePermission:
        url = const.CREATE_ROLE_PERMISSIONS
        role_permission_obj:RolePermission = RolePermission(
            role_id=role_id,
            role_permissions=role_permissions
        )
        payload = json.dumps(self.role_permission_obj.get_dict())
        response = requests.request("POST", url, headers=self.headers, data=payload)

        if response.status_code == 200:
            role_permission_data = response.json().get('role_permissions')
            role_permission_obj.id = role_permission_data.get("id")
            role_permission_obj.message = "Role Permission Created!!"
        else:
            role_permission_obj.message = "Role Permission Creation Failed!!"
        
        role_permission_obj.status_code = response.status_code

        self.log.print_log(role_permission_obj)
        return role_permission_obj