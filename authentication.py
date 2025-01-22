import firebase_admin
import pyrebase
import re
import json
import requests
import time
import os

# Get the current working directory of the script or executable
base_dir = os.path.dirname(os.path.abspath(__file__))

# Load the Firebase configuration JSON file
auth_key_path = os.path.join(base_dir, "AuthKey.json")
with open(auth_key_path, "r") as file:
    firebaseConfig = json.load(file)

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

#Needed API Endpoints
api_key = firebaseConfig["apiKey"]
update_email_url = "https://identitytoolkit.googleapis.com/v1/accounts:update"
send_verification_url = "https://identitytoolkit.googleapis.com/v1/accounts:sendOobCode"
#update_password_url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key" add this back after clean up from funs

# Helper Functions
def is_valid_email(email):
    """Check if the provided email is valid."""
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

def get_error_message(error_str):
    json_start = error_str.find("{") #Get start of json return
    json_data = json.loads(error_str [json_start:]) #convert and load data
    error_message = json_data.get("error", {}).get("message", "Unknown error") #Grab the message section of error json
    return error_message

# Core Functions
def signup(email, password):
    """Sign up a new user."""
    email = email.strip()
    password = password.strip()
    
    if not is_valid_email(email):
        message = "Invalid email format. Please try again."
        #return signup()
        return False, message, None

    if len(password) < 6:
        message = "Password must be at least 6 characters long. Please try again."
        #return signup()
        return False, message, None

    try:
        user = auth.create_user_with_email_and_password(email, password)
        print(f"Signup successful! Welcome, {email}")
        message = f"Signup successful! Welcome, {email}"
        return True, message, user
        #login()  # Prompt user to log in after signing up
    except Exception as e:
        error_str = str(e)
        print("TEST")
        error_message = get_error_message(error_str)
        print("ERROR MESSAGE")
        if "EMAIL_EXISTS" in error_message:
            message = "Email already exists. Please login instead."
            return False, message, None
        else:
            print(e)
            print("Error during signup:", error_message)
    


def login(email, password):
    """Login an existing user."""
    print(email)
    print(password)
    email = email.strip()
    password = password.strip()

    if not is_valid_email(email):
        message = "Invalid email format. Please try again."
        return False, message, None
#        return login()

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"Login successful! Welcome, {email}")
        message = f"Login successful! Welcome, {email}"
        return True, message, user
    except Exception as e:
        error_str  = str(e)
        error_message = get_error_message(error_str)

        if "INVALID_LOGIN_CREDENTIALS" in error_message:
            message = "Either Email or Password is incorrect. Please try again."
            print("Either Email or Password is incorrect. Please try again.")
            return False, message, None
        if "EMAIL_NOT_FOUND" in error_message:
            message = "Email is incorrect or not found. Please try again."
            print("Either Email or Password is incorrect. Please try again.")
            return False, message, None
        if "MISSING_PASSWORD":
            message = "You must enter a password. Please try again."
            return False, message, None
        else:
            print(e)
            print("Error during login:", error_message)





def reset_password():
    """Reset a user's password."""
    print("\n--- Reset Password ---")
    email = input("Enter your email: ").strip()

    if not is_valid_email(email):
        print("Invalid email format. Please try again.")
        return reset_password()

    try:
        auth.send_password_reset_email(email)
        print(f"Password reset email sent to {email}. Please check your inbox.")
    except Exception as e:
        print("Error during password reset:", str(e))


def logout():
    """Log out the user."""
    print("\nLogging out...")
    print("You have been logged out successfully.")

def get_user_account_info(user):
    return auth.get_account_info(user['idToken'])

def update_account(user):
    """Update a user's email or password."""
    print("\n--- Update Account ---")
    new_email = input("Enter your new email (leave blank to skip): ").strip()
    new_password = input("Enter your new password (leave blank to skip): ").strip()

    try:
        if new_email and is_valid_email(new_email):
            auth.update_user_email(user['idToken'], new_email)
            print(f"Email updated to {new_email}.")
        if new_password and len(new_password) >= 6:
            auth.update_user_password(user['idToken'], new_password)
            print("Password updated successfully.")
        if not new_email and not new_password:
            print("No changes made.")
    except Exception as e:
        print("Error during account update:", str(e))

def update_display_name(user, new_display_name):
    try:
        if new_display_name:
            auth.update_profile(user["idToken"], new_display_name)
            #auth.update_user_email(user['idToken'], new_email)
            print(f"Display Name updated to {new_display_name}.")
            
        if not new_display_name:
            print("No changes made.")
    except Exception as e:
        print("Error during account update:", str(e))


def check_email_verified(id_token):
    """
    Check if the updated email is verified.
    Args:
        id_token (str): The user's ID token.
    Returns:
        bool: True if the email is verified, False otherwise.
    """
    account_info_url = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={api_key}"
    payload = {"idToken": id_token}
    response = requests.post(account_info_url, json=payload)

    if response.status_code == 200:
        account_info = response.json()
        email_verified = account_info["users"][0].get("emailVerified", False)
        return email_verified
    else:
        print(f"Error checking email verification status: {response.json()}")
        return False

def wait_for_email_verification(id_token, timeout=300, interval=10):
    """
    Wait for the new email to be verified.
    Args:
        id_token (str): The user's ID token.
        timeout (int): Maximum time to wait for verification in seconds (default: 300).
        interval (int): Time to wait between checks in seconds (default: 10).
    
    Returns:
        bool: True if email is verified within the timeout, False otherwise.
    """
    start_time = time.time()
    
    while time.time() - start_time < timeout:
        if check_email_verified(id_token):
            return True
        print("Waiting for email verification...")
        time.sleep(interval)  # Wait for the specified interval before checking again
    
    return False


def send_verification_email(id_token):

    payload = {
        "requestType": "VERIFY_EMAIL",
        "idToken": id_token
    }

    response = requests.post(f"{send_verification_url}?key={api_key}", json=payload)
    # Check the response
    if response.status_code == 200:
        print(f"Verification email sent successfully. Please check your inbox.")
    else:
        print(f"Error sending verification email: {response.json()}")

def update_email(id_token, new_email):
    """
    Update the user's email.
    Args:
        id_token (str): The user's ID token.
        new_email (str): The new email to update.
    """
    payload = {
        "idToken": id_token,
        "email": new_email,
        "returnSecureToken": True
    }
    response = requests.post(f"{update_email_url}?key={api_key}", json=payload)

    if response.status_code == 200:
        print(f"Email successfully updated to {new_email}.")
    else:
        error_message = response.json().get("error", {}).get("message", "Unknown error")
        if "EMAIL_EXISTS" in error_message:
            print(f"Error: The email '{new_email}' is already in use by another account.")
        else:
            print(f"Error during email update: {error_message}")



def refresh_id_token(user):
    payload = {"grant_type": "refresh_token", "refresh_token": user["refreshToken"]}
    response = requests.post(f"https://securetoken.googleapis.com/v1/token?key={api_key}", json=payload)
    if response.status_code == 200:
        refreshed_data = response.json()
        return refreshed_data["id_token"]
    else:
        print(f"Error refreshing ID token: {response.json()}")
        return None


def update_email_and_verify(user, new_email):
    """
    Update the user's email and send a verification email.
    Args:
        user (dict): The authenticated user object.
        new_email (str): The new email to update.
    """
    id_token = user["idToken"]
    try:
        # Step 1: Validate the new email
        if not is_valid_email(new_email):
            print("Invalid email address provided.")
            return
        
        CurrentEmailIsVerified = check_email_verified(id_token)
        if CurrentEmailIsVerified:
            print("Current user is already verified!")
        else:
            print("User not verified, Please verify")
            send_verification_email(id_token)
            wait_for_email_verification(id_token)

        id_token = refresh_id_token(user)
        if not id_token:
            print("Failed to refresh ID token. Cannot proceed.")
            return
        
        # Step 2: Update the email
        update_email(id_token, new_email)
        #CurrentEmailIsVerified = check_email_verified(id_token) #Vefify new email
      
    except Exception as e:
        print(f"Error during email update and verification: {e}")



def update_password(user, new_password):
    """Update the user's password."""
    id_token = user["idToken"]
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:update?key={api_key}"
    data = {
        "idToken": id_token,
        "password": new_password,
        "returnSecureToken": True
    }
    try:
        response = requests.post(url, json=data)
        response_data = response.json()
        if response.status_code == 200:
            print("Password updated successfully.")
            #return response_data
        else:
            print(f"Error updating password: {response_data['error']['message']}")
            #return None
    except Exception as e:
        print(f"Request failed: {e}")
        #return None


def delete_account(user):
    """Delete a user's account."""
    print("\n--- Delete Account ---")
    confirm = input("Are you sure you want to delete your account? [Yes/No]: ").strip().lower()
    if confirm == "yes":
        try:
            auth.delete_user_account(user['idToken'])
            print("Your account has been deleted successfully.")
        except Exception as e:
            print("Error deleting account:", str(e))
    else:
        print("Account deletion canceled.")


