# import requests

# BASE_URL = "http://127.0.0.1:5000"

# # Test User Registration
# def test_register():
#     response = requests.post(BASE_URL + "/register", json={
#         "email": "testuser2@example.com",
#         "name": "Test User",
#         "mobile": "1234567890",
#         "city": "Test City",
#         "password": "securepassword"
#     })
#     print("Register Response:", response.json())

# # Test User Login
# def test_login():
#     response = requests.post(BASE_URL + "/login", json={
#         "email": "testuser2@example.com",
#         "password": "securepassword"
#     })
#     print("Login Response:", response.json())

# # Run tests
# if __name__ == "__main__":
#     test_register()
#     test_login()


import requests

BASE_URL = "http://127.0.0.1:5000"

# Test User Registration
def test_register():
    response = requests.post(BASE_URL + "/register", json={
        "email": "newuser1@example.com",
        "name": "Test User",
        "mobile": "1234567890",
        "city": "Test City",
        "password": "securepassword",
        "referral_code": "VQB2MC1M"
    })
    print("Register Response:", response.json())

# Test User Login
def test_login():
    response = requests.post(BASE_URL + "/login", json={
        "email": "newuser1@example.com",
        "password": "securepassword"
    })
    
    json_response = response.json()
    print("Login Response:", json_response)

    # Extract user_id from response
    if "user_id" in json_response:
        return json_response["user_id"]
    else:
        print("Login Failed, Cannot Proceed to Get Referrals Test")
        return None

# Test Get Referrals
def test_get_referrals(user_id):
    if user_id is None:
        print("Skipping referrals test as login failed.")
        return
    
    response = requests.get(BASE_URL + f"/referrals/{user_id}")
    print("Get Referrals Response:", response.json())

# Run tests
if __name__ == "__main__":
    test_register()
    user_id = test_login()
    test_get_referrals(user_id)
