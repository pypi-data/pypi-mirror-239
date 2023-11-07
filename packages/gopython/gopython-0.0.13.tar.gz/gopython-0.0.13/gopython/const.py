BASE_URL = "http://127.0.0.1:8000"
HEADERS = {
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=OVwpp5rokWAkZ6OHFBXSKxoctE0uLFPl'
}

#User API endpoints
GET_USER_BY_ID_API = f"{BASE_URL}/get-user-by-id"
GET_USER_ROLE_BY_ID = f"{BASE_URL}/get-user-roles-by-user-id"
CREATE_USER_API = f"{BASE_URL}/create-user"
CREATE_USER_ROLE_API = f"{BASE_URL}/create-user-role"

# Auth API endpoints
USER_LOGIN_API = f"{BASE_URL}/user-login"
USER_SIGNUP_API = f"{BASE_URL}/create-user-role"
USER_ROLE_PERMISSIONS_API = f"{BASE_URL}/get-user-with-role-permissions"

#Role API endpoints
CREATE_ROLE_API = f"{BASE_URL}/create-role"
CREATE_ROLE_PERMISSIONS = f"{BASE_URL}/create-role-permissions"

# Permission API endpoints
CREATE_PERMISSION_API = f"{BASE_URL}/create-permission"



#
