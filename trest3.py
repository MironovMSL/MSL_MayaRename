import tkinter as tk
from tkinter import ttk

class NumberSliderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Number Position Slider")

        # Текст, в который будем вставлять число
        self.text = "This is a number: ____ and it can move."
        self.number = 42  # Число, которое будем двигать
        self.number_position = 16  # Начальная позиция для числа в строке

        # Метка с текстом
        self.label_var = tk.StringVar()
        self.update_label_text()

        self.label = ttk.Label(self.root, textvariable=self.label_var, font=("Arial", 16))
        self.label.pack(pady=20)

        # Слайдер для управления позицией числа
        self.slider = ttk.Scale(self.root, from_=0, to=len(self.text)-len(str(self.number)), orient="horizontal", command=self.slider_moved)
        self.slider.set(self.number_position)  # Устанавливаем начальную позицию слайдера
        self.slider.pack(pady=20)

    def update_label_text(self):
        # Обновляем текст метки с учётом новой позиции числа
        number_str = str(self.number)
        updated_text = self.text[:self.number_position] + number_str + self.text[self.number_position + len(number_str):]
        self.label_var.set(updated_text)

    def slider_moved(self, value):
        # Когда слайдер двигается, меняем позицию числа
        self.number_position = int(float(value))  # Позиция на основе слайдера
        self.update_label_text()  # Обновляем метку


if __name__ == "__main__":
    root = tk.Tk()
    app = NumberSliderApp(root)
    root.mainloop()
