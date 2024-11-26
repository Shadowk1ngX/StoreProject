import pyrebase
import re

# Firebase configuration
firebaseConfig = {
    'apiKey': "AIzaSyARRGwaVVWQhI9OOseqf1vn_ZYRFl8EDHA",
    'authDomain': "storeproject-123cd.firebaseapp.com",
    'databaseURL': "https://storeproject-123cd-default-rtdb.firebaseio.com",
    'projectId': "storeproject-123cd",
    'storageBucket': "storeproject-123cd.firebasestorage.app",
    'messagingSenderId': "444334516644",
    'appId': "1:444334516644:web:087b22b900626684113931",
    'measurementId': "G-NHX4PDKTJL"
}

# Initialize Firebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()


# Helper Functions
def is_valid_email(email):
    """Check if the provided email is valid."""
    regex = r'^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.match(regex, email)


# Core Functions
def signup():
    """Sign up a new user."""
    print("\n--- Sign Up ---")
    email = input("Enter Email: ").strip()
    password = input("Enter Password: ").strip()

    if not is_valid_email(email):
        print("Invalid email format. Please try again.")
        return signup()

    if len(password) < 6:
        print("Password must be at least 6 characters long. Please try again.")
        return signup()

    try:
        auth.create_user_with_email_and_password(email, password)
        print(f"Signup successful! Welcome, {email}")
        login()  # Prompt user to log in after signing up
    except Exception as e:
        error_message = str(e)
        if "EMAIL_EXISTS" in error_message:
            print("Email already exists. Please login instead.")
        else:
            print("Error during signup:", error_message)


def login():
    """Login an existing user."""
    print("\n--- Login ---")
    email = input("Enter Email: ").strip()
    password = input("Enter Password: ").strip()

    if not is_valid_email(email):
        print("Invalid email format. Please try again.")
        return login()

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        print(f"Login successful! Welcome, {email}")
        main_menu(user)  # Proceed to main menu
    except Exception as e:
        error_message = str(e)
        if "EMAIL_NOT_FOUND" in error_message:
            print("Email not registered. Please sign up first.")
        elif "INVALID_PASSWORD" in error_message:
            print("Incorrect password.")
            reset = input("Forgot your password? [Yes/No]: ").strip().lower()
            if reset == "yes":
                reset_password()
        else:
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
def main():
    print("Welcome to the Membership Portal!")
    while True:
        ans = input("Are you a new user? [Yes/No]: ").strip().lower()
        if ans == "yes":
            signup()
            break
        elif ans == "no":
            login()
            break
        else:
            print("Invalid input. Please enter 'Yes' or 'No'.")


# Start the Program
if __name__ == "__main__":
    main()
