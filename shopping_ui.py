from PyQt5 import QtWidgets, QtGui, QtCore

class ModernShoppingApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Main Window Settings
        self.setWindowTitle("Modern Shopping App")
        self.resize(1000, 700)
        self.current_theme = "light"  # Default theme
        self.apply_light_theme()

        # Main Layout
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Header Section
        self.header_label = QtWidgets.QLabel("🛒 Temp Name")
        self.header_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #007bff; margin: 10px;")
        self.header_label.setAlignment(QtCore.Qt.AlignCenter)
        self.main_layout.addWidget(self.header_label)

        # Theme Toggle
        self.theme_toggle_button = QtWidgets.QPushButton("Switch to Dark Theme")
        self.theme_toggle_button.setStyleSheet("background-color: #007bff; color: white; padding: 5px 10px; border-radius: 5px;")
        self.theme_toggle_button.clicked.connect(self.toggle_theme)
        self.main_layout.addWidget(self.theme_toggle_button)

        # Filter Section
        self.filter_frame = QtWidgets.QFrame()
        self.filter_frame.setStyleSheet("background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 8px; padding: 10px;")
        self.filter_layout = QtWidgets.QHBoxLayout(self.filter_frame)
        self.filter_label = QtWidgets.QLabel("Filter by Category:")
        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.addItems(["All", "Electronics", "Clothing", "Furniture"])
        self.filter_combo.setStyleSheet("padding: 5px;")
        self.filter_button = QtWidgets.QPushButton("Apply Filter")
        self.filter_button.setStyleSheet("background-color: #007bff; color: white; padding: 5px 10px; border-radius: 5px;")
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_combo)
        self.filter_layout.addWidget(self.filter_button)
        self.main_layout.addWidget(self.filter_frame)

        # Splitter for Items and Cart
        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)

        # Items Section
        self.items_frame = QtWidgets.QFrame()
        self.items_frame.setStyleSheet("background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 8px; padding: 10px;")
        self.items_layout = QtWidgets.QVBoxLayout(self.items_frame)
        self.items_label = QtWidgets.QLabel("🛍️ Items")
        self.items_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.items_list = QtWidgets.QListWidget()
        self.items_list.setStyleSheet("border: 1px solid #dee2e6; border-radius: 5px; padding: 5px;")
        self.view_item_button = QtWidgets.QPushButton("View Item")
        self.view_item_button.setStyleSheet("background-color: #28a745; color: white; padding: 5px 10px; border-radius: 5px; margin-top: 5px;")
        self.add_to_cart_button = QtWidgets.QPushButton("Add to Cart")
        self.add_to_cart_button.setStyleSheet("background-color: #ffc107; color: white; padding: 5px 10px; border-radius: 5px; margin-top: 5px;")
        self.items_layout.addWidget(self.items_label)
        self.items_layout.addWidget(self.items_list)
        self.items_layout.addWidget(self.view_item_button)
        self.items_layout.addWidget(self.add_to_cart_button)

        # Cart Section
        self.cart_frame = QtWidgets.QFrame()
        self.cart_frame.setStyleSheet("background-color: #ffffff; border: 1px solid #dee2e6; border-radius: 8px; padding: 10px;")
        self.cart_layout = QtWidgets.QVBoxLayout(self.cart_frame)
        self.cart_label = QtWidgets.QLabel("🛒 Cart")
        self.cart_label.setStyleSheet("font-size: 18px; font-weight: bold; margin-bottom: 10px;")
        self.cart_list = QtWidgets.QListWidget()
        self.cart_list.setStyleSheet("border: 1px solid #dee2e6; border-radius: 5px; padding: 5px;")
        self.checkout_button = QtWidgets.QPushButton("Checkout")
        self.checkout_button.setStyleSheet("background-color: #dc3545; color: white; padding: 5px 10px; border-radius: 5px; margin-top: 5px;")
        self.cart_layout.addWidget(self.cart_label)
        self.cart_layout.addWidget(self.cart_list)
        self.cart_layout.addWidget(self.checkout_button)

        # Add Frames to Splitter
        self.splitter.addWidget(self.items_frame)
        self.splitter.addWidget(self.cart_frame)

        # Add Splitter to Main Layout
        self.main_layout.addWidget(self.splitter)

        # Signals
        self.filter_button.clicked.connect(self.filter_items)
        self.view_item_button.clicked.connect(self.view_item)
        self.add_to_cart_button.clicked.connect(self.add_to_cart)
        self.checkout_button.clicked.connect(self.checkout)

        # Sample Items
        self.items = [
            {"name": "PlayStation 5", "category": "Electronics", "price": 499.99},
            {"name": "Xbox Series X", "category": "Electronics", "price": 499.99},
            {"name": "Office Chair", "category": "Furniture", "price": 89.99},
            {"name": "T-shirt", "category": "Clothing", "price": 19.99},
        ]
        self.cart = []
        self.load_items()

    def load_items(self):
        """Load items into the list widget."""
        self.items_list.clear()
        for item in self.items:
            self.items_list.addItem(f"{item['name']} - ${item['price']}")

    def filter_items(self):
        """Filter items based on the selected category."""
        selected_category = self.filter_combo.currentText()
        self.items_list.clear()

        filtered_items = [
            item for item in self.items if selected_category == "All" or item["category"] == selected_category
        ]
        for item in filtered_items:
            self.items_list.addItem(f"{item['name']} - ${item['price']}")

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
        self.setStyleSheet("""
            background-color: #f8f9fa; color: #343a40; font-family: Arial; font-size: 14px;
            QPushButton { border-radius: 5px; padding: 5px 10px; }
        """)
        self.current_theme = "light"

    def apply_dark_theme(self):
        """Apply dark theme styles."""
        self.setStyleSheet("""
            background-color: #2b2b2b; color: #f5f5f5; font-family: Arial; font-size: 14px;
            QPushButton { background-color: #444; color: white; border-radius: 5px; padding: 5px 10px; }
            QListWidget { background-color: #3b3b3b; color: white; border-radius: 5px; padding: 5px; }
        """)
       
