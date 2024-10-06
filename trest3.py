try:
    from PySide2 import QtWidgets, QtGui, QtCore
except:
    from PySide6 import QtWidgets, QtGui, QtCore
import sys

class SharedData:
    _instance = None

    @staticmethod
    def get_instance():
        if SharedData._instance is None:
            SharedData._instance = SharedData()
        return SharedData._instance

    def __init__(self):
        self.some_data = None


class SenderWidget(QtWidgets.QWidget):
    # Определяем сигнал с использованием правильного синтаксиса
    data_sent = QtCore.Signal(str)

    def __init__(self):
        super().__init__()
        button = QtWidgets.QPushButton("Send Data", self)
        button.clicked.connect(self.send_data)

    def send_data(self):
        data = "Hello from Sender"
        SharedData.get_instance().some_data = data
        print("Data sent!")
        self.data_sent.emit(data)  # Испускаем сигнал с данными


class ReceiverWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.button = QtWidgets.QPushButton("Get Data", self)
        self.button.clicked.connect(self.get_data)

    def get_data(self):
        data = SharedData.get_instance().some_data
        print(f"Received Data: {data}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    sender = SenderWidget()
    receiver = ReceiverWidget()

    # Подключаем сигнал из SenderWidget к слоту в ReceiverWidget
    sender.data_sent.connect(receiver.get_data)

    sender.show()
    receiver.show()

    sys.exit(app.exec_())
