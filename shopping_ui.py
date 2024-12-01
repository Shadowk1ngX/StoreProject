from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, pyqtSignal
import FirebaseScript
import requests
import authentication


class VerificationThread(QThread):
    finished = pyqtSignal(bool)  # Signal to indicate verification result

    def __init__(self, user_id_token):
        super().__init__()
        self.user_id_token = user_id_token

    def run(self):
        # Perform the verification check
        #result = authentication.check_email_verified(self.user_id_token)
        result = authentication.wait_for_email_verification(self.user_id_token)
        if not result:
            ...# handle timeouts or whatever returns false
        else:
            self.finished.emit(result)  # Emit the result when done



class ModernShoppingApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Main Window Settings
        self.setWindowTitle("Store Project")
        self.resize(1000, 700)
        self.current_theme = "dark"  # Default theme
        self.apply_dark_theme()
        self.user = None

        # Initialize the cart as an empty list
        self.cart = []
        self.total_price = 0.0

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Header Section
        self.header_frame = QtWidgets.QFrame()  # A frame to house header and button
        self.header_layout = QtWidgets.QHBoxLayout(self.header_frame)  # Horizontal layout for the header
        self.header_label = QtWidgets.QLabel("🛒 Temp Name")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #007bff; margin: 10px;")
        self.header_label.setAlignment(QtCore.Qt.AlignCenter)
        #self.main_layout.addWidget(self.header_label)

         # Login/Sign Up Button
        self.login_button = QtWidgets.QPushButton("Login / Sign Up")
        self.login_button.setStyleSheet("background-color: #007bff; color: white; padding: 5px 10px; border-radius: 5px;")
        self.login_button.clicked.connect(self.show_login_dialog)

        # Add widgets to the header layout
        self.header_layout.addWidget(self.header_label)
        self.header_layout.addStretch()  # Push the login button to the far right
        self.header_layout.addWidget(self.login_button)

        # Add the header frame to the main layout
        self.main_layout.addWidget(self.header_frame)

        # Theme Toggle
        self.theme_toggle_button = QtWidgets.QPushButton("Switch to Light Theme")
        self.theme_toggle_button.setStyleSheet("background-color: #007bff; color: white; padding: 5px 10px; border-radius: 5px;")
        self.theme_toggle_button.clicked.connect(self.toggle_theme)
        self.main_layout.addWidget(self.theme_toggle_button)

        # Filter Section
        self.filter_frame = QtWidgets.QFrame()
        self.filter_layout = QtWidgets.QHBoxLayout(self.filter_frame)
        self.filter_label = QtWidgets.QLabel("Filter by Category:")
        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.addItems(["All", "Electronics", "Clothing", "Furniture"])
        self.filter_button = QtWidgets.QPushButton("Apply Filter")
        self.filter_button.clicked.connect(self.filter_items)
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_combo)
        self.filter_layout.addWidget(self.filter_button)
        self.main_layout.addWidget(self.filter_frame)

        # Items Section
        self.items_frame = QtWidgets.QFrame()
        self.items_layout = QtWidgets.QVBoxLayout(self.items_frame)
        self.items_label = QtWidgets.QLabel("🛍️ Items")
        self.items_list = QtWidgets.QListWidget()
        self.view_item_button = QtWidgets.QPushButton("View Item")
        self.view_item_button.clicked.connect(self.view_item)
        self.add_to_cart_button = QtWidgets.QPushButton("Add to Cart")
        self.add_to_cart_button.clicked.connect(self.add_to_cart)
        self.items_layout.addWidget(self.items_label)
        self.items_layout.addWidget(self.items_list)
        self.items_layout.addWidget(self.view_item_button)
        self.items_layout.addWidget(self.add_to_cart_button)

        # Cart Section
        self.cart_frame = QtWidgets.QFrame()
        self.cart_layout = QtWidgets.QVBoxLayout(self.cart_frame)
        self.cart_label = QtWidgets.QLabel("🛒 Cart")
        self.cart_list = QtWidgets.QListWidget()
        self.total_price_label = QtWidgets.QLabel("Total: $0.00")  # Label to display the total price
        self.checkout_button = QtWidgets.QPushButton("Checkout")
        self.checkout_button.clicked.connect(self.checkout)

        # Add widgets to the cart layout
        self.cart_layout.addWidget(self.cart_label)
        self.cart_layout.addWidget(self.cart_list)
        self.cart_layout.addWidget(self.total_price_label)
        self.cart_layout.addWidget(self.checkout_button)

        # Splitter for Items and Cart
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.addWidget(self.items_frame)
        self.splitter.addWidget(self.cart_frame)

        # Add Splitter to Main Layout
        self.main_layout.addWidget(self.splitter)

        # Fetch and Load Items from Firebase
        self.items = self.fetch_items_from_firebase("products") 
        self.load_items()

        # Fetch categories from the database and update the combo box
        self.update_categories()


    def view_item(self):
        """View the details of the selected item, including the image."""
        selected_item = self.items_list.currentItem()
        if not selected_item:
            QtWidgets.QMessageBox.warning(self, "No Item Selected", "Please select an item to view.")
            return

        # Extract the item name from the selected list item
        item_name = selected_item.text().split(" - $")[0]
        # Find the corresponding item in self.items
        item = next((item for item in self.items if item["name"] == item_name), None)

        if item:
            # Create a pop-up dialog
            dialog = QtWidgets.QDialog(self)
            dialog.setWindowTitle(f"Item Details: {item['name']}")
            dialog_layout = QtWidgets.QVBoxLayout(dialog)

            # Load and display the image
            image_label = QtWidgets.QLabel()
            try:
                if "image" in item and item["image"]:
                    pixmap = QtGui.QPixmap()
                    image_data = self.fetch_image_data(item["image"])
                    if image_data and pixmap.loadFromData(image_data):
                        image_label.setPixmap(pixmap.scaled(300, 300, QtCore.Qt.KeepAspectRatio))
                    else:
                        image_label.setText("Image failed to load.")
                else:
                    image_label.setText("No image available.")
            except Exception as e:
                print(f"Error loading image: {e}")  # Log the error for debugging
                image_label.setText("No image available at the moment.")

            # Display the item name and category
            name_label = QtWidgets.QLabel(f"Name: {item['name']}")
            category_label = QtWidgets.QLabel(f"Category: {item['category']}")
            price_label = QtWidgets.QLabel(f"Price: ${item['price']:.2f}")
            
            # Add widgets to the dialog layout
            dialog_layout.addWidget(name_label)
            dialog_layout.addWidget(category_label)
            dialog_layout.addWidget(price_label)
            dialog_layout.addWidget(image_label)

            # Add a close button
            close_button = QtWidgets.QPushButton("Close")
            close_button.clicked.connect(dialog.close)
            dialog_layout.addWidget(close_button)

            # Show the dialog
            dialog.exec_()

    def show_login_dialog(self):
        """Show a login/sign-up dialog."""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Login / Sign Up")
        dialog_layout = QtWidgets.QVBoxLayout(dialog)

        # Username and Password Fields
        dialog.username_label = QtWidgets.QLabel("Email:")
        dialog.username_field = QtWidgets.QLineEdit()
        dialog.password_label = QtWidgets.QLabel("Password:")
        dialog.password_field = QtWidgets.QLineEdit()
        dialog.password_field.setEchoMode(QtWidgets.QLineEdit.Password)

        # Error Message Label
        dialog.error_message_label = QtWidgets.QLabel("")
        dialog.error_message_label.setStyleSheet("color: red;")  # Red text for errors
        dialog.error_message_label.setAlignment(QtCore.Qt.AlignCenter)

        # Buttons
        login_button = QtWidgets.QPushButton("Login")
        signup_button = QtWidgets.QPushButton("Sign Up")
        close_button = QtWidgets.QPushButton("Close")

        #Button actions
        close_button.clicked.connect(dialog.close)
        login_button.clicked.connect(lambda: self.login(dialog.username_field.text(), dialog.password_field.text(), dialog))
        signup_button.clicked.connect(lambda: self.signup(dialog.username_field.text(), dialog.password_field.text(), dialog))

        # Add widgets to the dialog layout
        dialog_layout.addWidget(dialog.username_label)
        dialog_layout.addWidget(dialog.username_field)
        dialog_layout.addWidget(dialog.password_label)
        dialog_layout.addWidget(dialog.password_field)
        dialog_layout.addWidget(dialog.error_message_label)
        dialog_layout.addWidget(login_button)
        dialog_layout.addWidget(signup_button)
        dialog_layout.addWidget(close_button)

        # Show the dialog
        dialog.exec_()


    def login(self, username, password, dialog):
        successful, message, user = authentication.login(username, password)
        print(f"Attempt returned: {successful}.\nMessage: {message}")
        if successful:
            QtWidgets.QMessageBox.information(self, "Login Successful", "Welcome back!")
            dialog.close()
            self.user = user
            self.update_header_for_logged_in_user(username)
            
        else:
            error_message_label = dialog.error_message_label
            username_field = dialog.username_field
            password_field = dialog.password_field
            
            error_message_label.setText(message)
            username_field.setStyleSheet("border: 1px solid red;")  # Highlight field in red
            password_field.setStyleSheet("border: 1px solid red;")
        
    
    def signup(self, email, password, dialog):
        successful, message, user = authentication.signup(email, password)
        print(f"Signup attempt returned:")
        if successful:
            QtWidgets.QMessageBox.information(self,"Success!", message)
            dialog.close()
            self.user = user
            self.update_header_for_logged_in_user(email)
        else:
            error_message_label = dialog.error_message_label
            username_field = dialog.username_field
            password_field = dialog.password_field
            
            error_message_label.setText(message)
            username_field.setStyleSheet("border: 1px solid red;")  # Highlight field in red
            password_field.setStyleSheet("border: 1px solid red;")

    def verify_email_and_update(self, idToken):
        authentication.send_verification_email(idToken)
        
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Email Verification")
        dialog.setModal(True)  # Make it a modal dialog (blocks interaction with other windows)
        dialog.setWindowFlags(dialog.windowFlags() & ~QtCore.Qt.WindowCloseButtonHint)
        layout = QtWidgets.QVBoxLayout(dialog)
        message_label = QtWidgets.QLabel("Please check your email for the verification link.")
        message_label.setAlignment(QtCore.Qt.AlignCenter)
        message_label.setStyleSheet("font-size: 14px; margin: 10px;")
        layout.addWidget(message_label)
        
        # Waiting Spinner (Optional, for UX improvement)
        spinner = QtWidgets.QLabel()
        spinner.setAlignment(QtCore.Qt.AlignCenter)
        spinner_movie = QtGui.QMovie("assets/loading.gif")  # Use QMovie to load the animated GIF
        if not spinner_movie.isValid():
            print("ERROR: Spinner GIF not found or invalid!")
        else:
            spinner.setMovie(spinner_movie)  # Set the spinner's movie
            spinner_movie.start()  # Start the animation
            layout.addWidget(spinner)
        # Make sure the window cannot be exited
        dialog.setWindowModality(QtCore.Qt.ApplicationModal)  # Blocks interaction with the app
        QtCore.QTimer.singleShot(0, dialog.show)
        
        self.verification_thread = VerificationThread(self.user["idToken"])
        self.verification_thread.finished.connect(lambda is_verified: self.on_verification_finished(dialog, is_verified))
        self.verification_thread.start()

        #Add a succsful verification window
       
        
    def show_profile_dialog(self):
        """Show a dialog for editing the user's profile."""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Edit Profile")
        dialog_layout = QtWidgets.QVBoxLayout(dialog)

        # Username Field
        username_label = QtWidgets.QLabel("New Username (Optional):")
        username_field = QtWidgets.QLineEdit()

        # Email Field
        email_label = QtWidgets.QLabel("New Email (Optional):")
        email_field = QtWidgets.QLineEdit()

        # Password Field
        password_label = QtWidgets.QLabel("New Password (Optional):")
        password_field = QtWidgets.QLineEdit()
        password_field.setEchoMode(QtWidgets.QLineEdit.Password)

        # Confirm Password Field
        confirm_password_label = QtWidgets.QLabel("Confirm Password:")
        confirm_password_field = QtWidgets.QLineEdit()
        confirm_password_field.setEchoMode(QtWidgets.QLineEdit.Password)

        # Buttons
        IsVerified = authentication.check_email_verified(self.user["idToken"])
        if not IsVerified:
            self.verify_email_button = QtWidgets.QPushButton("Verify Email")
            self.verify_email_button.clicked.connect(lambda: self.verify_email_and_update(self.user["idToken"]))
        save_button = QtWidgets.QPushButton("Save Changes")
        cancel_button = QtWidgets.QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.close)
        logout_button = QtWidgets.QPushButton("Log Out")
        
        save_button.clicked.connect(lambda: self.update_profile(
            dialog, 
            username_field.text(), 
            email_field.text(), 
            password_field.text(), 
            confirm_password_field.text()
        ))
        cancel_button.clicked.connect(dialog.close)
        logout_button.clicked.connect(lambda: self.confirm_logout(dialog))

        # Add widgets to the dialog layout
        dialog_layout.addWidget(username_label)
        dialog_layout.addWidget(username_field)
        dialog_layout.addWidget(email_label)
        dialog_layout.addWidget(email_field)
        dialog_layout.addWidget(password_label)
        dialog_layout.addWidget(password_field)
        dialog_layout.addWidget(confirm_password_label)
        dialog_layout.addWidget(confirm_password_field)
        if not IsVerified:
            dialog_layout.addWidget(self.verify_email_button)
        dialog_layout.addWidget(save_button)
        dialog_layout.addWidget(logout_button)
        dialog_layout.addWidget(cancel_button)

        dialog.exec_()
    
    def get_display_name(self):
        NewInfo = authentication.get_user_account_info(self.user)
        try:
            print("Get Display name")
            if 'users' in NewInfo and len(NewInfo['users']) > 0:
                print(f"Found: {NewInfo['users'][0].get('displayName', '')}")
                return NewInfo['users'][0].get('displayName', "")
            else:
                print("Error: Unable to find displayName in the response.")
                return ""
        except:
            print("Failed")
            ...

    def on_verification_finished(self, window, verified):
        """Handle the result of the verification."""
        if verified:
            self.verified_label.setText("✅ Verified")
            self.verified_label.setStyleSheet("font-size: 12px; color: green; margin: 0; padding: 0;")
            self.verify_email_button.deleteLater()
            self.verify_email_button = None
        else:
            self.verified_label.setText("❌ Not Verified")
            self.verified_label.setStyleSheet("font-size: 12px; color: red; margin: 0; padding: 0;")
            
        window.close()

         


    def update_header_for_logged_in_user(self, user_email):
        """Update the header to show the user's email and add a profile button after login."""
        # Hide the login button
        self.login_button.hide()

        # Create a vertical layout for the user info (email and verified)
        user_info_layout = QtWidgets.QVBoxLayout()

        # Display the user's email or display name
        DisplayName = self.get_display_name()
        if DisplayName:
            self.user_email_label = QtWidgets.QLabel(f"Logged in as: {DisplayName}")
        else:
            self.user_email_label = QtWidgets.QLabel(f"Logged in as: {user_email}")

        self.user_email_label.setStyleSheet("font-size: 14px; color: #007bff; margin: 5px;")
        user_info_layout.addWidget(self.user_email_label)

        # Update or create the "Verified" label
        if hasattr(self, "verified_label") and self.verified_label:
            if authentication.check_email_verified(self.user["idToken"]):
                self.verified_label.setText("✅ Verified")
                self.verified_label.setStyleSheet("font-size: 12px; color: green; margin: 0; padding: 0;")
            else:
                self.verified_label.setText("❌ Not Verified")
                self.verified_label.setStyleSheet("font-size: 12px; color: red; margin: 0; padding: 0;")
        else:
            if authentication.check_email_verified(self.user["idToken"]):
                self.verified_label = QtWidgets.QLabel("✅ Verified")
                self.verified_label.setStyleSheet("font-size: 12px; color: green; margin: 0; padding: 0;")
            else:
                self.verified_label = QtWidgets.QLabel("❌ Not Verified")
                self.verified_label.setStyleSheet("font-size: 12px; color: red; margin: 0; padding: 0;")
            user_info_layout.addWidget(self.verified_label)

        # Add the user info layout to the header layout
        self.header_layout.addLayout(user_info_layout)

        # Create a vertical layout for buttons
        button_layout = QtWidgets.QVBoxLayout()

        # Add a profile button
        self.profile_button = QtWidgets.QPushButton("Edit Profile")
        self.profile_button.setStyleSheet("background-color: #007bff; color: white; padding: 5px 10px; border-radius: 5px;")
        self.profile_button.clicked.connect(self.show_profile_dialog)
        button_layout.addWidget(self.profile_button)

        # Add the Log Out button
        self.logout_button = QtWidgets.QPushButton("Log Out")
        self.logout_button.setStyleSheet("background-color: #d9534f; color: white; padding: 5px 10px; border-radius: 5px;")
        self.logout_button.clicked.connect(self.confirm_logout)
        button_layout.addWidget(self.logout_button)

        # Add the button layout to the header layout
        self.header_layout.addLayout(button_layout)




    def update_profile(self, dialog, new_username, new_email, new_password, confirm_password):
        """Update the user's profile."""
        if new_password and new_password != confirm_password:
            QtWidgets.QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
        
        try:
            # Update username (this may involve your own backend logic)
            if new_username:
                print(f"Updating username to: {new_username}")
                authentication.update_display_name(self.user, new_username)
                DisplayName = self.get_display_name()      
                self.user_email_label.setText(f"Logged in as: {DisplayName}")

            # Update email
            if new_email:
                print(f"Updating email to: {new_email}")
                print()
                authentication.update_email_and_verify(self.user, new_email)  # Replace with your logic

            # Update password
            if new_password:
                print(f"Updating password.")
                authentication.update_password(self.user,new_password)  # Replace with your logic

            QtWidgets.QMessageBox.information(self, "Profile Updated", "Your profile has been updated successfully.")
            dialog.close()
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to update profile: {str(e)}")


    def confirm_logout(self, dialog):
        """Open a confirmation dialog to log out."""
        confirmation = QtWidgets.QMessageBox.question(
            self,
            "Confirm Logout",
            "Are you sure you want to log out?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )

        if confirmation == QtWidgets.QMessageBox.Yes:
            # Perform log-out actions
            print("Logging out...")
            self.user = None  # Clear the current user
            self.reset_ui_to_logged_out_state()
            if dialog:
                dialog.close()  # Close the profile dialog
        else:
            print("Logout canceled.")


    def add_to_cart(self):
        """Add the selected item to the cart."""
        selected_item = self.items_list.currentItem()
        if not selected_item:
            QtWidgets.QMessageBox.warning(self, "No Item Selected", "Please select an item to add to the cart.")
            return

        # Extract the name and price from the selected item's text
        item_text = selected_item.text()
        item_parts = item_text.split(" - $")  # Split to separate name and price
        if len(item_parts) >= 2:  # Ensure both name and price exist
            item_name = item_parts[0]
            item_price = float(item_parts[1].split(" - ")[0])  # Extract price as float

            # Create a custom widget for the cart item with a "Remove X" button
            cart_item_widget = QtWidgets.QWidget()
            cart_item_layout = QtWidgets.QHBoxLayout(cart_item_widget)
            cart_item_label = QtWidgets.QLabel(f"{item_name} - ${item_price:.2f}")
            remove_button = QtWidgets.QPushButton("X")
            remove_button.setStyleSheet("color: red; font-weight: bold;")
            remove_button.clicked.connect(lambda: self.remove_from_cart(cart_item_widget, item_price))

            # Add the label and button to the layout
            cart_item_layout.addWidget(cart_item_label)
            cart_item_layout.addWidget(remove_button)
            cart_item_layout.setContentsMargins(0, 0, 0, 0)  # Remove extra spacing
            cart_item_widget.setLayout(cart_item_layout)

            # Add the custom widget to the cart list
            list_item = QtWidgets.QListWidgetItem(self.cart_list)
            list_item.setSizeHint(cart_item_widget.sizeHint())
            self.cart_list.addItem(list_item)
            self.cart_list.setItemWidget(list_item, cart_item_widget)

            # Update the total price
            self.cart.append((item_name, item_price))
            self.update_total_price(item_price)
        else:
            QtWidgets.QMessageBox.warning(self, "Invalid Item", "Unable to extract item details. Please try again.")
          


    def remove_from_cart(self, cart_item_widget, item_price):
        """Remove an item from the cart."""
        # Remove the widget from the cart_list visually
        for i in range(self.cart_list.count()):
            item = self.cart_list.item(i)
            if self.cart_list.itemWidget(item) == cart_item_widget:
                self.cart_list.takeItem(i)  # Remove the widget from the list
                break

        # Remove only one instance of the item from the cart list (not all instances)
        for cart_item in self.cart:
            if cart_item[1] == item_price:  # Match the price
                self.cart.remove(cart_item)  # Remove the first matching instance
                break

        # Update the total price
        self.update_total_price(-item_price)

    def reset_ui_to_logged_out_state(self):
        """Reset the UI to the logged-out state."""
        # Clear the user info and hide the user-specific widgets
        self.user = None

        # Remove the user email label if it exists
        if hasattr(self, "user_email_label") and self.user_email_label:
            self.header_layout.removeWidget(self.user_email_label)
            self.user_email_label.deleteLater()
            self.user_email_label = None

        # Remove the verified label if it exists
        if hasattr(self, "verified_label") and self.verified_label:
            self.header_layout.removeWidget(self.verified_label)
            self.verified_label.deleteLater()
            self.verified_label = None

        # Remove the profile button if it exists
        if hasattr(self, "profile_button") and self.profile_button:
            self.header_layout.removeWidget(self.profile_button)
            self.profile_button.deleteLater()
            self.profile_button = None

        # Remove the logout button if it exists
        if hasattr(self, "logout_button") and self.logout_button:
            self.header_layout.removeWidget(self.logout_button)
            self.logout_button.deleteLater()
            self.logout_button = None

        # Show the login button again
        self.login_button.show()


    def checkout(self):
        """Handle checkout process."""
        if not self.cart:
            QtWidgets.QMessageBox.warning(self, "Cart Empty", "Your cart is empty. Add items to the cart first.")
            return

        total_price = self.total_price
        QtWidgets.QMessageBox.information(
            self,
            "Checkout",
            f"Thank you for your purchase! Your total is ${total_price:.2f}.",
        )
        self.cart_list.clear()
        self.cart.clear()
        self.update_total_price(-self.total_price)  # Reset total price

    def toggle_theme(self):
        """Toggle between light and dark themes."""
        if self.current_theme == "light":
            self.apply_dark_theme()
            self.theme_toggle_button.setText("Switch to Light Theme")
        else:
            self.apply_light_theme()
            self.theme_toggle_button.setText("Switch to Dark Theme")

    def apply_light_theme(self):
        """Apply light theme styles."""
        self.current_theme = "light"
        self.setStyleSheet("""
            QWidget { background-color: #f8f9fa; color: #343a40; }
            QPushButton { background-color: #007bff; color: white; }
            QListWidget { background-color: #ffffff; color: #343a40; }
        """)

    def apply_dark_theme(self):
        """Apply dark theme styles."""
        self.current_theme = "dark"
        self.setStyleSheet("""
            QWidget { background-color: #2b2b2b; color: #f5f5f5; }
            QPushButton { background-color: #444; color: white; }
            QListWidget { background-color: #3b3b3b; color: white; }
        """)
    
    def fetch_items_from_firebase(self, collection_name):
        """Fetch items from Firebase and transform them into the required format."""
        try:
            items = FirebaseScript.GetAllItems(collection_name)
            # Transform the data into a format suitable for the app
            return [
                {
                    "name": item.get("name", "Unnamed"),  # Get name or default to "Unnamed"
                    "category": item.get("category", "Unknown"),  # Get category or default to "Unknown"
                    "price": item.get("price", 0.0),  # Get price or default to 0.0
                    "stock": item.get("stock", 0),
                    "image": item.get("image", ""),  # Include the image field
                }
                for item in items
            ]
        except Exception as e:
            print(f"Error fetching items from Firebase: {e}")
            return []


    def update_categories(self):
        """Fetch unique categories from the database and populate the combo box."""
        try:
            print("Running")
            # Example: Fetch all items from the database
            items = FirebaseScript.GetAllItems("products")

            # Extract unique categories from the items
            categories = set(item.get("category", "Unknown") for item in items)

            # Clear existing categories and update the combo box
            self.filter_combo.clear()
            self.filter_combo.addItem("All")  # Add "All" as the default option
            self.filter_combo.addItems(sorted(categories))  # Add categories alphabetically
        except Exception as e:
            print(f"Error fetching categories from Firebase: {e}")
            QtWidgets.QMessageBox.warning(self, "Error", "Unable to fetch categories from the database.")


    def load_items(self):
        """Load items into the list widget."""
        self.items_list.clear()
        for item in self.items:
            self.items_list.addItem(f"{item['name']} - ${item['price']} - Stock: {item['stock']}")

    def filter_items(self):
        """Filter items based on the selected category."""
        selected_category = self.filter_combo.currentText()
        self.items_list.clear()
        filtered_items = [
            item for item in self.items if selected_category == "All" or item["category"] == selected_category
        ]
        for item in filtered_items:
            self.items_list.addItem(f"{item['name']} - ${item['price']} - Stock: {item['stock']}")


    def fetch_image_data(self, image_url):
        """Fetch image data from a URL."""
        try:
            response = requests.get(image_url)
            if response.status_code == 200:
                return response.content
        except Exception as e:
            print(f"Failed to fetch image: {e}")
        return None
    
    def update_total_price(self, price_change):
        """Update the total price of the cart."""
        self.total_price += price_change
        self.total_price_label.setText(f"Total: ${self.total_price:.2f}")
