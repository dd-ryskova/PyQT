import sys
import os
import base64
from datetime import datetime
from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQml import QQmlApplicationEngine


class Interface(QObject):
    @pyqtSlot(str, str)
    def saveCanvas(self, image_data_base64, save_type="auto"):
        """Сохранить canvas из QML"""
        try:
            # Создаем папку для сохранения
            save_dir = "saved_canvases"
            if not os.path.exists(save_dir):
                os.makedirs(save_dir)
            
            # Генерируем имя файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            prefix = "manual" if save_type == "manual" else "auto"
            filename = f"{save_dir}/{prefix}_canvas_{timestamp}.png"
            
            # Декодируем base64 и сохраняем
            image_data = base64.b64decode(image_data_base64)
            with open(filename, 'wb') as f:
                f.write(image_data)
            
            print(f"✓ Сохранено: {filename}")
            return True
            
        except Exception as e:
            print(f"✗ Ошибка сохранения: {e}")
            return False


if __name__ == '__main__':
    app = QApplication(sys.argv)
    
    interface = Interface()
    engine = QQmlApplicationEngine()
    
    # Регистрируем объект для доступа из QML
    engine.rootContext().setContextProperty("_backend", interface)
    
    engine.load("mainWindow.qml")
    
    if not engine.rootObjects():
        print("Ошибка загрузки QML файла")
        sys.exit(-1)
    
    sys.exit(app.exec())