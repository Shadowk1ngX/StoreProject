import pyrebase
import re
import json
import requests

# Firebase configuration (Dont upload keys online or others can acsess our databases) Moved to offline file
# Load Firebase configuration from a JSON file
with open("AuthKey.json", "r") as file:
    firebaseConfig = json.load(file)

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


# Helper Functions
def is_valid_email(email):
    """Check if the provided email is valid."""
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)


# Core Functions
def signup(email, password):
    """Sign up a new user."""
    email = email.strip()
    password = password.strip()
    
    if not is_valid_email(email):
        print("Invalid email format. Please try again.")
        #return signup()
        return False, message

    if len(password) < 6:
        print("Password must be at least 6 characters long. Please try again.")
        #return signup()

    try:
        auth.create_user_with_email_and_password(email, password)
        print(f"Signup successful! Welcome, {email}")
        #login()  # Prompt user to log in after signing up
    except Exception as e:
        error_message = str(e)
        if "EMAIL_EXISTS" in error_message:
            print("Email already exists. Please login instead.")
        else:
            print("Error during signup:", error_message)
    


def login(email, password):
    """Login an existing user."""
    email = email.strip()
    password = password.strip()

    if not is_valid_email(email):
        print("Invalid email format. Please try again.")
        message = "Invalid email format. Please try again."
        return False, message, None
#        return login()

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"Login successful! Welcome, {email}")
        message = f"Login successful! Welcome, {email}"
        return True, message , user
#        main_menu(user)  # Proceed to main menu
    except Exception as e:
        error_str  = str(e)
        json_start = error_str .find("{") #Get start of json return
        json_data = json.loads(error_str [json_start:]) #convert and load data
        error_message = json_data.get("error", {}).get("message", "Unknown error") #Grab the message section of error json

        if "INVALID_LOGIN_CREDENTIALS" in error_message:
            message = "Either Email or Password is incorrect. Please try again."
            print("Either Email or Password is incorrect. Please try again.")
            return False, message, None
 #           reset = input("Forgot your password? [Yes/No]: ").strip().lower()
 #           if reset == "yes":
 #               reset_password()
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


def update_email(user, new_email):
    """Update a user's email"""
    try:
        if new_email and is_valid_email(new_email):
            auth.update_profile(user["idToken"])
            #auth.update_user_email(user['idToken'], new_email)
            print(f"Email updated to {new_email}.")
        
        if not new_email:
            print("No changes made.")
    except Exception as e:
        print("Error during account update:", str(e))

def update_password(user, new_password):
    """Update the user's password."""
    try:
        if new_password and len(new_password) >= 6:
            auth.update_user_password(user['idToken'], new_password)
            print("Password updated successfully.")
        if not new_password:
            print("No changes made.")
    except Exception as e:
        print("Error during account update:", str(e))


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


def main_menu(user):
    """Main menu for logged-in users."""
    while True:
        print("\n--- Main Menu ---")
        print("1. Logout")
        print("2. Update Account")
        print("3. Delete Account")
        print("4. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == "1":
            logout()
            break
        elif choice == "2":
            update_account(user)
        elif choice == "3":
            delete_account(user)
            break
        elif choice == "4":
            print("Exiting. Goodbye!")
            exit()
        else:
            print("Invalid choice. Please try again.")


# Main Program Flow
#def main():
#    print("Welcome to the Membership Portal!")
#    while True:
#        ans = input("Are you a new user? [Yes/No]: ").strip().lower()
#        if ans == "yes":
#            signup()
#            break
#        elif ans == "no":
#            login()
#            break
#        else:
#            print("Invalid input. Please enter 'Yes' or 'No'.")


# Start the Program
#if __name__ == "__main__":
#    main()
