from PyQt5.QtWidgets import QFrame, QHBoxLayout, QLineEdit, QLabel
from PyQt5.QtCore import Qt, QLocale
from PyQt5.QtGui import QFont, QDoubleValidator
from currency_signals import RUBSignals, USDSignals, EURSignals


class CurrencyInputField(QFrame):
    def __init__(self, label_text, currency_symbol, currency_type):
        super().__init__()
        self.is_updating = False
        self.currency_symbol = currency_symbol
        self.label_text = label_text
        self.currency_type = currency_type
        
        if currency_type == 'USD':
            self.signals = USDSignals()
        elif currency_type == 'EUR':
            self.signals = EURSignals()
        elif currency_type == 'RUB':
            self.signals = RUBSignals()
        
        self.init_ui()
        
    def init_ui(self):
        self.setup_frame_style()
        layout = self.create_layout()
        self.create_label(layout)
        self.create_input_field(layout)
        self.create_currency_symbol(layout)
        
    def setup_frame_style(self):
        self.setFrameStyle(QFrame.StyledPanel)
        self.setStyleSheet('''
            QFrame {
                background-color: white;
                margin: 5px;
            }
        ''')
        
    def create_layout(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(15, 10, 15, 10)
        self.setLayout(layout)
        return layout
        
    def create_label(self, layout):
        label = QLabel(self.label_text)
        label.setFont(QFont('Arial', 12, QFont.Bold))
        label.setStyleSheet('color: #2c3e50; min-width: 120px;')
        layout.addWidget(label)
        
    def create_input_field(self, layout):
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText('0.00')
        self.input_field.setFont(QFont('Arial', 14))
        self.input_field.setAlignment(Qt.AlignRight)
        self.input_field.setStyleSheet('''
            QLineEdit {
                border: none;
                background: transparent;
                padding: 8px 5px;
                selection-background-color: #3498db;
            }
        ''')
        
        validator = QDoubleValidator()
        validator.setBottom(0)
        validator.setTop(1000000000)
        validator.setDecimals(2)
        validator.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.input_field.setValidator(validator)
        
        self.input_field.textChanged.connect(self.on_text_changed)
        
        layout.addWidget(self.input_field)
        
    def create_currency_symbol(self, layout):
        symbol_label = QLabel(self.currency_symbol)
        symbol_label.setFont(QFont('Arial', 14, QFont.Bold))
        symbol_label.setStyleSheet('color: #e74c3c; min-width: 30px;')
        layout.addWidget(symbol_label)
        
    def on_text_changed(self, text):
        if not self.is_updating:
            if self.currency_type == 'USD':
                self.signals.usdValueChanged.emit(text)
            elif self.currency_type == 'EUR':
                self.signals.eurValueChanged.emit(text)
            elif self.currency_type == 'RUB':
                self.signals.rubValueChanged.emit(text)
            
    def update_value(self, value):
        self.is_updating = True
        self.input_field.setText(value)
        self.is_updating = False