import pyrebase

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

def login():
    print("Login")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"Login successful! Welcome, {email}")
    except:
        print("Invalid email or password. Please try again.")

def signup():
    print("Sign Up")
    email = input("Enter Email: ")
    password = input("Enter Password: ")
    try:
        user = auth.create_user_with_email_and_password(email, password)
        print(f"Signup successful! Welcome, {email}")
    except Exception as e:
        print("Error during signup:", str(e))

# Main logic
ans = input("Are you a new user? [Yes/No]: ").strip().lower()

if ans == "no":
    login()
elif ans == "yes":
    signup()
else:
    print("Invalid input. Please enter 'Yes' or 'No'.")
