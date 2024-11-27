import pyrebase
import re

# Firebase configuration
config = {
    "apiKey": "YOUR_FIREBASE_API_KEY",
    "authDomain": "YOUR_FIREBASE_PROJECT.firebaseapp.com",
    "databaseURL": "https://YOUR_FIREBASE_PROJECT.firebaseio.com",
    "storageBucket": "YOUR_FIREBASE_PROJECT.appspot.com",
}

# Initialize Firebase
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

def is_valid_email(email):
    """Check if the provided email is valid."""
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)

def login():
    print("Login")
    email = input("Enter Email: ").strip()
    password = input("Enter Password: ").strip()
    
    if not is_valid_email(email):
        print("Invalid email format. Please try again.")
        return

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"Login successful! Welcome, {email}")
    except Exception as e:
        error_message = str(e)
        if "EMAIL_NOT_FOUND" in error_message:
            print("Email not registered. Please sign up first.")
        elif "INVALID_PASSWORD" in error_message:
            print("Incorrect password. Please try again.")
        else:
            print("Error during login:", error_message)

def signup():
    print("Sign Up")
    email = input("Enter Email: ").strip()
    password = input("Enter Password: ").strip()
    
    if not is_valid_email(email):
        print("Invalid email format. Please try again.")
        return
    
    if len(password) < 6:
        print("Password must be at least 6 characters long.")
        return

    try:
        user = auth.create_user_with_email_and_password(email, password)
        print(f"Signup successful! Welcome, {email}")
    except Exception as e:
        error_message = str(e)
        if "EMAIL_EXISTS" in error_message:
            print("Email already exists. Please login instead.")
        else:
            print("Error during signup:", error_message)

# Main logic
ans = input("Are you a new user? [Yes/No]: ").strip().lower()

if ans == "no":
    login()
elif ans == "yes":
    signup()
else:
    print("Invalid input. Please enter 'Yes' or 'No'.")
