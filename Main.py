import sys
from PyQt5 import QtWidgets
from shopping_ui import ModernShoppingApp

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ModernShoppingApp()
    window.show()
    sys.exit(app.exec_())