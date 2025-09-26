import sys
import random
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QMessageBox, QGraphicsOpacityEffect
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QRegion


class ComplimentApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.shape_mode = False

        self.messages = [
            "Вы сегодня выглядите просто прекрасно!",
            "Ваша улыбка освещает комнату!",
            "У вас отличное чувство юмора!",
            "Вы очень талантливы!",
            "С вами приятно общаться!",
            "Вы вдохновляете окружающих!",
            "Ваша доброта не знает границ!",
            "Вы прекрасный собеседник!",
            "У вас замечательный вкус!",
            "Вы излучаете позитивную энергию!",
            "Вы умны и эрудированны!",
            "Ваша уверенность впечатляет!",
            "Вы прекрасно справляетесь с задачами!",
            "У вас доброе сердце!",
            "Вы творческий человек!",
            "Ваша настойчивость восхищает!",
            "Вы отлично мотивируете других!",
            "У вас прекрасное чувство стиля!",
            "Вы надежный друг и партнер!",
            "Ваша улыбка заразительна!"
        ]

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Генератор комплиментов")
        self.resize(600, 600)

        container = QWidget()
        self.setCentralWidget(container)

        container.setStyleSheet("""
            QWidget {
                background-color: #ffe6f0;
            }
            QPushButton {
                background-color: #ff66b2;
                color: white;
                border: none;
                padding: 10px 18px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #ff4da6;
            }
            QPushButton:pressed {
                background-color: #e60073;
            }
            QLabel {
                font-size: 15px;
                font-weight: bold;
                color: #660033;
            }
        """)

        self.bg = QLabel(container)
        self.bg.setScaledContents(True)
        self.bg.setVisible(False)
        self.bg.setAttribute(Qt.WA_TransparentForMouseEvents)

        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(30)

        self.text = QLabel("Нажмите кнопку, чтобы получить комплимент")
        self.text.setAlignment(Qt.AlignCenter)
        self.text.setWordWrap(True)
        layout.addWidget(self.text)

        btns = QHBoxLayout()
        btns.setAlignment(Qt.AlignCenter)
        btns.setSpacing(15)

        self.btn_compliment = QPushButton("Сказать комплимент")
        self.btn_form = QPushButton("Сменить форму")

        self.btn_compliment.clicked.connect(self.show_compliment)
        self.btn_form.clicked.connect(self.toggle_shape)

        btns.addWidget(self.btn_compliment)
        btns.addWidget(self.btn_form)
        layout.addLayout(btns)

    def show_compliment(self):
        msg = random.choice(self.messages)
        self.text.setText(f"«{msg}»")

    def toggle_shape(self):
        if not self.shape_mode:
            try:
                mask_img, bg_img = self.load_mask_and_bg("image.png")
            except FileNotFoundError as e:
                QMessageBox.critical(self, "Ошибка", str(e))
                return

            mask = mask_img.mask()
            region = QRegion(mask)
            offset_x = (self.width() - mask_img.width()) // 2
            offset_y = (self.height() - mask_img.height()) // 2
            region.translate(offset_x, offset_y)

            self.setMask(region)
            self.setWindowOpacity(0.9)

            self.bg.setPixmap(bg_img.scaled(
                self.centralWidget().size(),
                Qt.KeepAspectRatioByExpanding,
                Qt.SmoothTransformation
            ))

            effect = QGraphicsOpacityEffect()
            effect.setOpacity(0.55)
            self.bg.setGraphicsEffect(effect)
            self.bg.setVisible(True)

            self.shape_mode = True
            self.btn_form.setText("Обычное окно")
        else:
            self.clearMask()
            self.setWindowOpacity(1.0)
            self.bg.setVisible(False)
            self.bg.setPixmap(QPixmap())
            self.bg.setGraphicsEffect(None)

            self.shape_mode = False
            self.btn_form.setText("Сменить форму")

    def load_mask_and_bg(self, filename: str):
        if not os.path.exists(filename):
            raise FileNotFoundError(f"Файл {filename} не найден.")

        pixmap = QPixmap(filename)
        if pixmap.isNull():
            raise FileNotFoundError(f"Файл {filename} поврежден или не может быть загружен.")

        size = int(min(self.width(), self.height()) * 0.8)
        size = max(size, 200)

        mask_img = pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        bg_img = pixmap.scaled(self.centralWidget().size(), Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        return mask_img, bg_img

    def resizeEvent(self, event):
        self.bg.setGeometry(0, 0, self.centralWidget().width(), self.centralWidget().height())
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = ComplimentApp()
    win.show()
    sys.exit(app.exec_())