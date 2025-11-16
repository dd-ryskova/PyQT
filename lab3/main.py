import sys
import sqlite3
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTabWidget, QTableWidget, 
                             QTableWidgetItem, QComboBox, QMessageBox, QLabel,
                             QFileDialog, QLineEdit, QGroupBox, QRadioButton,
                             QButtonGroup)
from PyQt5.QtCore import Qt

class DatabaseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.connection = None
        self.db_path = None    
        self.init_ui()
        
    def init_ui(self):
        """Инициализация пользовательского интерфейса"""
        self.setWindowTitle('Обозреватель базы данных Shop')
        self.setGeometry(100, 100, 1200, 700)
        
        # Создаем центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        self.create_connection_panel(main_layout)       # Панель управления соединением с БД
        self.create_control_panel(main_layout)          # Панель элементов управления запросами
        self.create_price_filter_group(main_layout)     # Группа фильтра по цене для Tab4
        self.create_stats_group(main_layout)            # Группа статистики для Tab5
        

        self.status_label = QLabel('Соединение с БД не установлено') # Метка статуса
        main_layout.addWidget(self.status_label)
        
        # Создаем вкладки
        self.create_tabs(main_layout)
        
        # Инициализируем таблицы во вкладках
        self.init_tab_tables()
        
    def create_connection_panel(self, layout):
        """Создает панель управления подключением к БД"""
        connection_layout = QHBoxLayout()
        
        self.btn_connect = QPushButton('Установить соединение с БД')
        self.btn_connect.clicked.connect(self.set_connection)
        
        self.btn_disconnect = QPushButton('Закрыть соединение')
        self.btn_disconnect.clicked.connect(self.close_connection)
        self.btn_disconnect.setEnabled(False)
        
        connection_layout.addWidget(self.btn_connect)
        connection_layout.addWidget(self.btn_disconnect)
        connection_layout.addStretch()
        
        layout.addLayout(connection_layout)
    
    def create_control_panel(self, layout):
        """Создает панель основных элементов управления"""
        control_layout = QHBoxLayout()
        
        # bt1 - Кнопка для показа названий товаров
        self.bt1 = QPushButton('Показать названия товаров')
        self.bt1.clicked.connect(self.execute_bt1)
        self.bt1.setEnabled(False)
        
        # Выпадающий список для выбора колонок
        self.combo_columns = QComboBox()
        self.combo_columns.setEnabled(False)
        self.combo_columns.currentTextChanged.connect(self.execute_combo_query)
        
        control_layout.addWidget(self.bt1)
        control_layout.addWidget(QLabel('Колонки:'))
        control_layout.addWidget(self.combo_columns)
        control_layout.addStretch()
        
        layout.addLayout(control_layout)
    
    def create_price_filter_group(self, layout):
        """Создает группу фильтрации по цене"""
        price_group = QGroupBox("Фильтр по цене для Tab4")
        price_layout = QHBoxLayout()
        
        # Поля ввода для минимальной и максимальной цены
        self.min_price_input = QLineEdit()
        self.min_price_input.setPlaceholderText("Мин. цена")
        self.min_price_input.setMaximumWidth(100)
        
        self.max_price_input = QLineEdit()
        self.max_price_input.setPlaceholderText("Макс. цена")
        self.max_price_input.setMaximumWidth(100)
        
        # bt2 - Кнопка применения фильтра
        self.bt2 = QPushButton('Применить фильтр по цене')
        self.bt2.clicked.connect(self.execute_bt2)
        self.bt2.setEnabled(False)
        
        price_layout.addWidget(QLabel("Диапазон цен:"))
        price_layout.addWidget(self.min_price_input)
        price_layout.addWidget(QLabel("-"))
        price_layout.addWidget(self.max_price_input)
        price_layout.addWidget(self.bt2)
        price_layout.addStretch()
        
        price_group.setLayout(price_layout)
        layout.addWidget(price_group)
    
    def create_stats_group(self, layout):
        """Создает группу для статистических запросов"""
        stats_group = QGroupBox("Статистика для Tab5")
        stats_layout = QHBoxLayout()
        self.stats_group = QButtonGroup(self)
        
        # Варианты статистики
        self.radio_category = QRadioButton("По категориям")
        self.radio_category.setChecked(True)  # Выбрано по умолчанию
        self.radio_supplier = QRadioButton("По поставщикам")
        self.radio_price_ranges = QRadioButton("По ценовым диапазонам")
        self.radio_top_products = QRadioButton("Топ товаров")
    
        for radio in [self.radio_category, self.radio_supplier, 
                     self.radio_price_ranges, self.radio_top_products]:
            self.stats_group.addButton(radio)
            stats_layout.addWidget(radio)
        
        # bt3 - Кнопка генерации отчета
        self.bt3 = QPushButton('Показать статистику')
        self.bt3.clicked.connect(self.execute_bt3)
        self.bt3.setEnabled(False)
        
        stats_layout.addWidget(self.bt3)
        stats_layout.addStretch()
        
        stats_group.setLayout(stats_layout)
        layout.addWidget(stats_group)
    
    def create_tabs(self, layout):
        """Создает вкладки приложения"""
        self.tab_widget = QTabWidget()
        
        # Создаем вкладки
        self.tabs = {}
        tab_names = [
            ("Tab1 - Все товары", "tab1"),
            ("Tab2 - Названия", "tab2"), 
            ("Tab3 - Колонки", "tab3"),
            ("Tab4 - Фильтр по цене", "tab4"),
            ("Tab5 - Статистика", "tab5")
        ]
        
        for name, key in tab_names:
            tab = QWidget()
            self.tabs[key] = tab
            self.tab_widget.addTab(tab, name)
        
        layout.addWidget(self.tab_widget)
    
    def init_tab_tables(self):
        """Инициализирует таблицы во всех вкладках"""
        self.tables = {}
        
        for key in self.tabs:
            # Создаем layout для вкладки
            layout = QVBoxLayout(self.tabs[key])
            
            # Создаем таблицу и добавляем в layout
            table = QTableWidget()
            self.tables[key] = table
            layout.addWidget(table)
    
    def set_connection(self):
        """Устанавливает соединение с базой данных"""
        try:
            # Запрашиваем у пользователя файл базы данных
            db_path, _ = QFileDialog.getOpenFileName(
                self, 
                'Выберите файл базы данных Shop', 
                '', 
                'SQLite Database (*.db *.sqlite);;All Files (*)'
            )
            
            if not db_path:
                return
                
            # Подключаемся к базе данных
            self.connection = sqlite3.connect(db_path)
            self.db_path = db_path
            
            # Проверяем наличие таблицы shop
            cursor = self.connection.cursor()
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='shop'")
            if not cursor.fetchone():
                raise Exception("Таблица 'shop' не найдена в базе данных")
            
            # Активируем элементы управления
            self.set_controls_enabled(True)
            
            # Выполняем начальные действия
            self.execute_default_query()  # Загружаем данные в Tab1
            self.populate_combo_box()     # Заполняем список колонок
            
            self.status_label.setText(f'Соединение с БД установлено: {os.path.basename(db_path)}')
            QMessageBox.information(self, 'Успех', 'Соединение с базой данных установлено!')
            
        except Exception as e:
            # В случае ошибки закрываем соединение и показываем сообщение
            if self.connection:
                self.connection.close()
                self.connection = None
            QMessageBox.critical(self, 'Ошибка', f'Не удалось подключиться к БД: {str(e)}')
            
    def close_connection(self):
        """Закрывает соединение с базой данных"""
        if self.connection:
            self.connection.close()
            self.connection = None
            
        # Отключаем элементы управления
        self.set_controls_enabled(False)
        
        # Очищаем данные
        self.clear_all_tables()
        self.min_price_input.clear()
        self.max_price_input.clear()
        self.combo_columns.clear()
        
        self.status_label.setText('Соединение с БД закрыто')
        QMessageBox.information(self, 'Информация', 'Соединение с базой данных закрыто')
    
    def set_controls_enabled(self, enabled):
        """Включает/отключает элементы управления"""
        self.btn_connect.setEnabled(not enabled)
        self.btn_disconnect.setEnabled(enabled)
        self.bt1.setEnabled(enabled)
        self.bt2.setEnabled(enabled)
        self.bt3.setEnabled(enabled)
        self.combo_columns.setEnabled(enabled)
        
    def populate_combo_box(self):
        """Заполняет выпадающий список названиями колонок таблицы shop"""
        if not self.connection:
            return
            
        cursor = self.connection.cursor()
        cursor.execute("PRAGMA table_info(shop)")  # Получаем информацию о колонках
        columns = cursor.fetchall()
        
        self.combo_columns.clear()
        for column in columns:
            self.combo_columns.addItem(column[1])  # column[1] - название колонки
                
    def execute_default_query(self):
        """Выполняет запрос по умолчанию - все товары в Tab1"""
        if not self.connection:
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM shop")
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]  # Получаем названия колонок
            
            self.display_in_table(self.tables['tab1'], data, columns)
            
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка запроса: {str(e)}')
            
    def execute_bt1(self):
        """Показывает только названия товаров в Tab2"""
        if not self.connection:
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT product_name FROM shop")
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            self.display_in_table(self.tables['tab2'], data, columns)
            
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка запроса: {str(e)}')
            
    def execute_combo_query(self, column_name):
        """Показывает данные выбранной колонки в Tab3"""
        if not self.connection or not column_name:
            return
            
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT {column_name} FROM shop")
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            self.display_in_table(self.tables['tab3'], data, columns)
            
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка запроса: {str(e)}')
            
    def execute_bt2(self):
        """Фильтрует товары по цене и показывает в Tab4"""
        if not self.connection:
            return
            
        try:
            # Получаем значения из полей ввода
            min_price = self.min_price_input.text().strip()
            max_price = self.max_price_input.text().strip()
            
            # Проверяем корректность введенных данных
            if min_price and not self.is_float(min_price):
                raise ValueError("Минимальная цена должна быть числом")
            if max_price and not self.is_float(max_price):
                raise ValueError("Максимальная цена должна быть числом")
            
            # Формируем запрос в зависимости от введенных данных
            if min_price and max_price:
                query = "SELECT * FROM shop WHERE price BETWEEN ? AND ? ORDER BY price"
                params = (float(min_price), float(max_price))
            elif min_price:
                query = "SELECT * FROM shop WHERE price >= ? ORDER BY price"
                params = (float(min_price),)
            elif max_price:
                query = "SELECT * FROM shop WHERE price <= ? ORDER BY price"
                params = (float(max_price),)
            else:
                query = "SELECT * FROM shop ORDER BY price"
                params = ()
            
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            self.display_in_table(self.tables['tab4'], data, columns)
            
        except ValueError as e:
            QMessageBox.warning(self, 'Ошибка ввода', str(e))
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка запроса: {str(e)}')
            
    def execute_bt3(self):
        """Показывает статистику в Tab5 в зависимости от выбранного варианта"""
        if not self.connection:
            return
            
        try:
            cursor = self.connection.cursor()
            
            # Выбираем запрос в зависимости от выбранной радиокнопки
            if self.radio_category.isChecked():
                query = """
                SELECT 
                    category as Категория,
                    COUNT(*) as 'Кол-во товаров',
                    ROUND(AVG(price), 2) as 'Средняя цена',
                    MAX(price) as 'Макс. цена',
                    MIN(price) as 'Мин. цена',
                    SUM(quantity) as 'Общее кол-во'
                FROM shop 
                GROUP BY category 
                ORDER BY COUNT(*) DESC
                """
                
            elif self.radio_supplier.isChecked():
                query = """
                SELECT 
                    supplier as Поставщик,
                    COUNT(*) as 'Кол-во товаров',
                    ROUND(AVG(price), 2) as 'Средняя цена',
                    ROUND(SUM(price * quantity), 2) as 'Общая стоимость',
                    SUM(quantity) as 'Общее кол-во'
                FROM shop 
                WHERE supplier IS NOT NULL
                GROUP BY supplier 
                ORDER BY COUNT(*) DESC
                """
                
            elif self.radio_price_ranges.isChecked():
                query = """
                SELECT 
                    CASE 
                        WHEN price < 100 THEN 'До 100'
                        WHEN price BETWEEN 100 AND 500 THEN '100-500'
                        WHEN price BETWEEN 500 AND 1000 THEN '500-1000' 
                        WHEN price BETWEEN 1000 AND 2000 THEN '1000-2000'
                        ELSE 'Выше 2000'
                    END as 'Ценовой диапазон',
                    COUNT(*) as 'Кол-во товаров',
                    ROUND(AVG(price), 2) as 'Средняя цена',
                    ROUND(SUM(price * quantity), 2) as 'Общая стоимость'
                FROM shop 
                GROUP BY 1
                ORDER BY MIN(price)
                """
                
            else:  # Топ товаров
                query = """
                SELECT 
                    product_name as 'Название товара',
                    category as Категория,
                    price as Цена,
                    rating as Рейтинг,
                    quantity as 'Кол-во на складе',
                    supplier as Поставщик
                FROM shop 
                WHERE rating IS NOT NULL
                ORDER BY rating DESC, price DESC
                LIMIT 15
                """
            
            cursor.execute(query)
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]
            
            self.display_in_table(self.tables['tab5'], data, columns)
            
        except Exception as e:
            QMessageBox.critical(self, 'Ошибка', f'Ошибка запроса: {str(e)}')
    
    def is_float(self, value):
        """Проверяет, можно ли преобразовать строку в число"""
        try:
            float(value)
            return True
        except ValueError:
            return False
            
    def display_in_table(self, table_widget, data, columns):
        """Отображает данные в таблице"""
        table_widget.clear()
        
        if not data:
            table_widget.setRowCount(0)
            table_widget.setColumnCount(0)
            return
            
        # Устанавливаем размеры таблицы
        table_widget.setRowCount(len(data))
        table_widget.setColumnCount(len(columns))
        table_widget.setHorizontalHeaderLabels(columns)
        
        # Заполняем таблицу данными
        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(str(value) if value is not None else 'N/A')
                table_widget.setItem(row_idx, col_idx, item)
                
        # Подгоняем размер колонок под содержимое
        table_widget.resizeColumnsToContents()
        
    def clear_all_tables(self):
        """Очищает все таблицы"""
        for table in self.tables.values():
            table.clear()
            table.setRowCount(0)
            table.setColumnCount(0)

def main():
    app = QApplication(sys.argv)
    window = DatabaseApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()