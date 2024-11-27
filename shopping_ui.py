from PyQt5 import QtWidgets, QtCore
import FirebaseScript

class ModernShoppingApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Main Window Settings
        self.setWindowTitle("Store Project")
        self.resize(1000, 700)
        self.current_theme = "dark"  # Default theme
        self.apply_dark_theme()

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


    def view_item(self):
        """View the details of the selected item."""
        selected_item = self.items_list.currentItem()
        if not selected_item:
            QtWidgets.QMessageBox.warning(self, "No Item Selected", "Please select an item to view.")
            return
        item_name = selected_item.text().split(" - $")[0]
        item = next((item for item in self.items if item["name"] == item_name), None)
        if item:
            QtWidgets.QMessageBox.information(
                self,
                "Item Details",
                f"Name: {item['name']}\nCategory: {item['category']}\nPrice: ${item['price']}",
            )

    def add_to_cart(self):
        """Add the selected item to the cart."""
        selected_item = self.items_list.currentItem()
        if not selected_item:
            QtWidgets.QMessageBox.warning(self, "No Item Selected", "Please select an item to add to the cart.")
            return
        self.cart_list.addItem(selected_item.text())
        self.cart.append(selected_item.text())

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
                    "stock": item.get("stock", 0)
                }
                for item in items
            ]
        except Exception as e:
            print(f"Error fetching items from Firebase: {e}")
            return []


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
            self.items_list.addItem(f"{item['name']} - Stock: {item['price']}")
