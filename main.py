# main.py
from interfaz import InterfazBiblioteca
import tkinter as tk

if __name__ == '__main__':
    root = tk.Tk()
    interfaz = InterfazBiblioteca(root)
    root.mainloop()
