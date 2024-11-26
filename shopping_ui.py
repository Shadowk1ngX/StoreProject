from PyQt5 import QtWidgets, QtGui, QtCore

class ShoppingApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # Main Layout
        self.setWindowTitle("Shopping App")
        self.resize(800, 600)
        self.main_layout = QtWidgets.QVBoxLayout(self)

        # Filter Section
        self.filter_layout = QtWidgets.QHBoxLayout()
        self.filter_label = QtWidgets.QLabel("Filter by Category:")
        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.addItems(["All", "Electronics", "Clothing", "Furniture"])
        self.filter_button = QtWidgets.QPushButton("Apply Filter")
        self.filter_layout.addWidget(self.filter_label)
        self.filter_layout.addWidget(self.filter_combo)
        self.filter_layout.addWidget(self.filter_button)
        self.main_layout.addLayout(self.filter_layout)

        # Items and Cart Section
        self.items_cart_layout = QtWidgets.QHBoxLayout()

        # Items List Section
        self.items_layout = QtWidgets.QVBoxLayout()
        self.items_label = QtWidgets.QLabel("Items")
        self.items_list = QtWidgets.QListWidget()
        self.view_item_button = QtWidgets.QPushButton("View Item")
        self.add_to_cart_button = QtWidgets.QPushButton("Add to Cart")
        self.items_layout.addWidget(self.items_label)
        self.items_layout.addWidget(self.items_list)
        self.items_layout.addWidget(self.view_item_button)
        self.items_layout.addWidget(self.add_to_cart_button)

        # Cart Section
        self.cart_layout = QtWidgets.QVBoxLayout()
        self.cart_label = QtWidgets.QLabel("Cart")
        self.cart_list = QtWidgets.QListWidget()
        self.checkout_button = QtWidgets.QPushButton("Checkout")
        self.cart_layout.addWidget(self.cart_label)
        self.cart_layout.addWidget(self.cart_list)
        self.cart_layout.addWidget(self.checkout_button)

        self.items_cart_layout.addLayout(self.items_layout)
        self.items_cart_layout.addLayout(self.cart_layout)

        self.main_layout.addLayout(self.items_cart_layout)

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


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = ShoppingApp()
    window.show()
    sys.exit(app.exec_())
