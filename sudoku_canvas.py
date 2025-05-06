from tkinter import *


def finish():
    """Функция, вызов который происходит при закрытии окна, сопровождающийся закрытием всего приложения"""
    main.destroy()


def click_button():
    """Функция обработки событий при нажатии кнопки"""
    pass


# создаём окно
main = Tk()
# создаём заголовок окна
main.title("Sudoku")
# устанавливаем размер окна
size = "300x500"
main.geometry(size)
#Устанавливаем фото на иконку
icon = PhotoImage(file = "sudoku_canvas.png")
main.iconphoto(False, icon)
# вызов функции закрытия приложения при закрытии окна
main.protocol("WM_DELETE_WINDOW", finish)

# текстовая метка
label = Label(text="Sudokuuuuu")
# размещаем метку в окне
label.pack()

# создаём кнопку с цифрой 1
button_one = Button(text='1', command=click_button)
button_two = Button(text='2', command=click_button)
button_three = Button(text='3', command=click_button)
button_four = Button(text='4', command=click_button)
# размещаем кнопки в окне
button_one.pack(ipadx=5, ipady=5, padx=50, pady=50, anchor="sw")
button_two.pack(ipadx=5, ipady=5, padx=5, pady=5, anchor="sw")
button_three.pack(ipadx=5, ipady=5, padx=5, pady=5, anchor="sw")
button_four.pack(ipadx=5, ipady=5, padx=5, pady=5, anchor="sw")

# запускаем цикл
main.mainloop()
