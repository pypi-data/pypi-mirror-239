import json
from gopython import const
from requests import requests
from gopython.dataclasses import Permission


class PermissionAPI:
    def __init__(self,name: str, description: str):
        self.permission = Permission(
            name=name,
            description=description
        )
    
    def create_permission(self) -> dict:
        url = const.CREATE_PERMISSION_API
        headers = const.HEADERS

        payload = json.dumps(self.self.permission.get_dict())
        response = requests.request("POST", url, headers=headers, data=payload)

        if response.status_code == 200:
            print("Permission Created!!")
            return response.json()
        
        print("Permission Creation Failed!!")
        return response.json
