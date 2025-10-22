from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QLabel, QPushButton)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from currency_input_field import CurrencyInputField
from conversion_service import ConversionService

class CurrencyConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.conversion_service = ConversionService()
        self.init_ui()          
        
    def init_ui(self):
        self.setWindowTitle('Конвертер валют')
        self.setFixedSize(750, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        self.create_title(layout)
        self.create_input_fields(layout)
        self.create_reset_button(layout)
        self.create_rates_display(layout)

    def create_title(self, layout):
        title = QLabel('Конвертер валют')
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont('Arial', 20, QFont.Bold))
        title.setStyleSheet('color: #2c3e50; margin: 20px;')
        layout.addWidget(title)

    def create_input_fields(self, layout):
        self.usd_input = CurrencyInputField('Доллары (USD)', '$', 'USD')
        self.eur_input = CurrencyInputField('Евро (EUR)', '€', 'EUR')
        self.rub_input = CurrencyInputField('Рубли (RUB)', '₽', 'RUB')
        
        self.connect_input_signals()
        
        layout.addWidget(self.usd_input)
        layout.addWidget(self.eur_input)
        layout.addWidget(self.rub_input)

    def connect_input_signals(self):
        self.usd_input.signals.usdValueChanged.connect(
            lambda value: self.conversion_service.convert_from_usd(
                value, self.eur_input, self.rub_input
            )
        )
        
        self.eur_input.signals.eurValueChanged.connect(
            lambda value: self.conversion_service.convert_from_eur(
                value, self.usd_input, self.rub_input
            )
        )
        
        self.rub_input.signals.rubValueChanged.connect(
            lambda value: self.conversion_service.convert_from_rub(
                value, self.usd_input, self.eur_input
            )
        )

    def create_reset_button(self, layout):
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
        ''')
        reset_btn.clicked.connect(self.reset_fields)
        layout.addWidget(reset_btn, alignment=Qt.AlignCenter)

    def create_rates_display(self, layout):
        rates_label = QLabel()
        rates_label.setAlignment(Qt.AlignLeft)
        rates_label.setFont(QFont('Arial', 11))
        rates_label.setStyleSheet('color: #34495e; margin: 15px; line-height: 1.8;')
        rates_label.setTextFormat(Qt.RichText)

        rates_text = f"""
        <div style="text-align: left;">
            <div><b>Курсы валют:</b></div>
            <div style="margin-top: 10px;">1 USD = {self.conversion_service.usd_to_eur:.6f} EUR | 1 USD = {self.conversion_service.usd_to_rub:.6f} RUB</div>
            <div>1 EUR = {self.conversion_service.eur_to_usd:.6f} USD | 1 EUR = {self.conversion_service.eur_to_rub:.6f} RUB</div>
            <div>1 RUB = {self.conversion_service.rub_to_usd:.6f} USD | 1 RUB = {self.conversion_service.rub_to_eur:.6f} EUR</div>
        </div>
        """
        rates_label.setText(rates_text)
        layout.addWidget(rates_label)
            
    def reset_fields(self):
        self.usd_input.update_value('')
        self.eur_input.update_value('')
        self.rub_input.update_value('')