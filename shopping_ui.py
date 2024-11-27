from PyQt5 import QtWidgets, QtCore, QtGui
import FirebaseScript
import requests

class ModernShoppingApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Main Window Settings
        self.setWindowTitle("Store Project")
        self.resize(1000, 700)
        self.current_theme = "dark"  # Default theme
        self.apply_dark_theme()

        # Initialize the cart as an empty list
        self.cart = []

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Header Section
        self.header_label = QtWidgets.QLabel("🛒 Temp Name")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #007bff; margin: 10px;")
        self.header_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.header_label)

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

        # Splitter for Items and Cart
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

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
        self.checkout_button = QtWidgets.QPushButton("Checkout")
        self.checkout_button.clicked.connect(self.checkout)
        self.cart_layout.addWidget(self.cart_label)
        self.cart_layout.addWidget(self.cart_list)
        self.cart_layout.addWidget(self.checkout_button)

        # Add Frames to Splitter
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
            item_price = "$" + item_parts[1].split(" - ")[0]  # Extract price
            display_text = f"{item_name} - {item_price}"  # Format for cart display

            # Add the formatted item to the cart list and cart storage
            self.cart_list.addItem(display_text)
            self.cart.append(display_text)
        else:
            QtWidgets.QMessageBox.warning(self, "Invalid Item", "Unable to extract item details. Please try again.")


    def checkout(self):
        """Handle checkout process."""
        if not self.cart:
            QtWidgets.QMessageBox.warning(self, "Cart Empty", "Your cart is empty. Add items to the cart first.")
            return
        total_price = sum(float(item.split("$")[1]) for item in self.cart)
        QtWidgets.QMessageBox.information(
            self,
            "Checkout",
            f"Thank you for your purchase! Your total is ${total_price:.2f}.",
        )
        self.cart_list.clear()
        self.cart.clear()

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
