import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLineEdit, QLabel, QFrame, QPushButton)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class CurrencyConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_exchange_rates()
        self.init_ui()          
        
    def init_ui(self):
        self.setWindowTitle('Конвертер валют')
        self.setFixedSize(700, 600)
        
        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Основной слой
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Заголовок
        title = QLabel('Конвертер валют')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setStyleSheet('color: #2c3e50; margin: 20px;')
        layout.addWidget(title)
        
        # Создаем поля для ввода
        self.usd_input = CurrencyInputField('Доллары (USD)', '$')
        self.eur_input = CurrencyInputField('Евро (EUR)', '€')
        self.rub_input = CurrencyInputField('Рубли (RUB)', '₽')
        
        # Подключаем сигналы
        self.usd_input.textChanged.connect(self.usd_changed)
        self.eur_input.textChanged.connect(self.eur_changed)
        self.rub_input.textChanged.connect(self.rub_changed)
        
        # Добавляем поля в слой
        layout.addWidget(self.usd_input)
        layout.addWidget(self.eur_input)
        layout.addWidget(self.rub_input)
        
        # Кнопка сброса
        reset_btn = QPushButton('Сбросить')
        reset_btn.setFont(QFont('Arial', 12))
        reset_btn.setFixedSize(120, 50)
        reset_btn.setStyleSheet('''
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 5px;
                border-radius: 5px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        ''')
        reset_btn.clicked.connect(self.reset_fields)
        layout.addWidget(reset_btn, alignment=Qt.AlignCenter)
        
        # Блок с курсами валют
        rates_label = QLabel()
        rates_label.setAlignment(Qt.AlignLeft)
        rates_label.setFont(QFont('Arial', 11))
        rates_label.setStyleSheet('color: #34495e; margin: 15px; line-height: 1.8;')
        rates_label.setTextFormat(Qt.RichText)

        # Формируем текст курсов
        rates_text = f"""
        <div style="text-align: left;">
            <div><b>Курсы валют:</b></div>
            <div style="margin-top: 10px;">1 USD = {self.usd_to_eur:.6f} EUR | 1 USD = {self.usd_to_rub:.6f} RUB</div>
            <div>1 EUR = {self.eur_to_usd:.6f} USD | 1 EUR = {self.eur_to_rub:.6f} RUB</div>
            <div>1 RUB = {self.rub_to_usd:.6f} USD | 1 RUB = {self.rub_to_eur:.6f} EUR</div>
        </div>
        """
        rates_label.setText(rates_text)
        layout.addWidget(rates_label)

    # Задаем курсы валют 
    def setup_exchange_rates(self):
        self.usd_to_eur = 0.862069
        self.usd_to_rub = 81.270000
        self.eur_to_usd = 1.160000
        self.eur_to_rub = 93.900000
        self.rub_to_usd = 0.012305
        self.rub_to_eur = 0.010650
        
    def usd_changed(self, value):
        if self.usd_input.is_updating:
            return
            
        try:
            usd_amount = float(value) if value else 0.0
            self.eur_input.update_value(str(round(usd_amount * self.usd_to_eur, 2)))
            self.rub_input.update_value(str(round(usd_amount * self.usd_to_rub, 2)))
        except ValueError:
            pass
            
    def eur_changed(self, value):
        if self.eur_input.is_updating:
            return
            
        try:
            eur_amount = float(value) if value else 0.0
            self.usd_input.update_value(str(round(eur_amount * self.eur_to_usd, 2)))
            self.rub_input.update_value(str(round(eur_amount * self.eur_to_rub, 2)))
        except ValueError:
            pass
            
    def rub_changed(self, value):
        if self.rub_input.is_updating:
            return
            
        try:
            rub_amount = float(value) if value else 0.0
            self.usd_input.update_value(str(round(rub_amount * self.rub_to_usd, 2)))
            self.eur_input.update_value(str(round(rub_amount * self.rub_to_eur, 2)))
        except ValueError:
            pass
            
    def reset_fields(self):
        self.usd_input.update_value('')
        self.eur_input.update_value('')
        self.rub_input.update_value('')

class CurrencyInputField(QFrame):
    textChanged = pyqtSignal(str)
    
    def __init__(self, label_text, currency_symbol):
        super().__init__()
        self.is_updating = False
        self.currency_symbol = currency_symbol
        self.init_ui(label_text)
        
    def init_ui(self, label_text):
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet('''
            QFrame {
                background-color: white;
                margin: 5px;
            }
        ''')
        
        layout = QHBoxLayout()
        self.setLayout(layout)
        
        # Метка с названием валюты
        label = QLabel(label_text)
        label.setFont(QFont('Arial', 12, QFont.Bold))
        label.setStyleSheet('color: #2c3e50; min-width: 100px;')
        layout.addWidget(label)
        
        # Поле для ввода
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('0.00')
        self.input_field.setFont(QFont('Arial', 14))
        self.input_field.setAlignment(Qt.AlignRight)
        self.input_field.setStyleSheet('''
            QLineEdit {
                border: none;
                background: transparent;
                padding: 10px 5px;
                selection-background-color: #3498db;
            }
        ''')
        self.input_field.textChanged.connect(self.on_text_changed)
        layout.addWidget(self.input_field)
        
        # Символ валюты
        symbol_label = QLabel(self.currency_symbol)
        symbol_label.setFont(QFont('Arial', 14, QFont.Bold))
        symbol_label.setStyleSheet('color: #e74c3c; min-width: 30px;')
        layout.addWidget(symbol_label)
        
    def on_text_changed(self, text):
        if not self.is_updating:
            self.textChanged.emit(text)
            
    def update_value(self, value):
        self.is_updating = True
        self.input_field.setText(value)
        self.is_updating = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    converter = CurrencyConverter()
    converter.show()
    
    sys.exit(app.exec_())