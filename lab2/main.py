import sys
from PyQt5.QtWidgets import QApplication
from currency_converter import CurrencyConverter

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    converter = CurrencyConverter()
    converter.show()
    
    sys.exit(app.exec_())