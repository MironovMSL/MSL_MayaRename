from PySide6 import QtWidgets, QtCore
import sys

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # Инициализация интерфейса
        self.initUI()

        # Текущая тема: 0 = светлая, 1 = темная
        self.current_theme = 0

    def initUI(self):
        # Создаем кнопку для переключения тем
        self.button = QtWidgets.QPushButton("Переключить тему", self)
        self.button.setGeometry(50, 50, 200, 50)
        self.button.clicked.connect(self.switch_theme)

        # Устанавливаем начальную светлую тему
        self.set_light_theme()

        # Настраиваем главное окно
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("Переключение тем")
        self.show()

    def switch_theme(self):
        """Функция для переключения тем"""
        if self.current_theme == 0:
            self.set_dark_theme()
            self.current_theme = 1
        else:
            self.set_light_theme()
            self.current_theme = 0

    def set_light_theme(self):
        """Устанавливаем светлую тему"""
        light_theme_stylesheet = """
            QMainWindow {
                background-color: #f0f0f0;
            }
            QPushButton {
                background-color: #e0e0e0;
                color: #000000;
                border: 1px solid #c0c0c0;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #d0d0d0;
            }
        """
        self.setStyleSheet(light_theme_stylesheet)

    def set_dark_theme(self):
        """Устанавливаем темную тему"""
        dark_theme_stylesheet = """
            QMainWindow {
                background-color: #2d2d2d;
            }
            QPushButton {
                background-color: #555555;
                color: #ffffff;
                border: 1px solid #333333;
                padding: 5px;
            }
            QPushButton:hover {
                background-color: #444444;
            }
        """
        self.setStyleSheet(dark_theme_stylesheet)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())