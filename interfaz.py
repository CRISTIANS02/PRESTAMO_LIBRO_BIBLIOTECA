# interfaz.py
import tkinter as tk
from funciones import agregar_alumno, obtener_alumnos, agregar_libro, obtener_libros, prestar_libro, devolver_libro

class InterfazBiblioteca:
    def __init__(self, master):
        self.master = master
        master.title('Biblioteca JMA 2023')

        # Sección para datos del alumno
        self.nombre_entry = tk.Entry(master)
        self.dni_entry = tk.Entry(master)

        self.nombre_label = tk.Label(master, text='Nombre:')
        self.dni_label = tk.Label(master, text='DNI:')

        self.nombre_label.grid(row=0, column=0, sticky=tk.E)
        self.dni_label.grid(row=1, column=0, sticky=tk.E)

        self.nombre_entry.grid(row=0, column=1)
        self.dni_entry.grid(row=1, column=1)

        self.agregar_alumno_button = tk.Button(master, text='Agregar Alumno', command=self.agregar_alumno)
        self.agregar_alumno_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Sección para datos del libro
        self.titulo_entry = tk.Entry(master)
        self.autor_entry = tk.Entry(master)

        self.titulo_label = tk.Label(master, text='Título:')
        self.autor_label = tk.Label(master, text='Autor:')

        self.titulo_label.grid(row=3, column=0, sticky=tk.E)
        self.autor_label.grid(row=4, column=0, sticky=tk.E)

        self.titulo_entry.grid(row=3, column=1)
        self.autor_entry.grid(row=4, column=1)

        self.agregar_libro_button = tk.Button(master, text='Agregar Libro', command=self.agregar_libro)
        self.agregar_libro_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Sección para préstamo y devolución de libros
        self.libros_label = tk.Label(master, text='Libros:')
        self.libros_label.grid(row=6, column=0, columnspan=2)

        self.lista_libros = tk.Listbox(master)
        self.lista_libros.grid(row=7, column=0, columnspan=2, pady=10)

        self.actualizar_lista_libros()

        self.prestar_button = tk.Button(master, text='Prestar Libro', command=self.prestar_libro)
        self.prestar_button.grid(row=8, column=0, pady=5)

        self.devolver_button = tk.Button(master, text='Devolver Libro', command=self.devolver_libro)
        self.devolver_button.grid(row=8, column=1, pady=5)

    def agregar_alumno(self):
        nombre = self.nombre_entry.get()
        dni = self.dni_entry.get()

        if nombre and dni:
            agregar_alumno(nombre, dni)
            self.actualizar_lista_libros()

    def agregar_libro(self):
        titulo = self.titulo_entry.get()
        autor = self.autor_entry.get()

        if titulo and autor:
            agregar_libro(titulo, autor)
            self.actualizar_lista_libros()

    def prestar_libro(self):
        selected_index = self.lista_libros.curselection()
        if selected_index:
            id_libro = int(selected_index[0]) + 1  # índice en la lista + 1
            self.prestar_libro_dialog(id_libro)

    def prestar_libro_dialog(self, id_libro):
        dialog = tk.Toplevel(self.master)
        dialog.title('Prestar Libro')

        label = tk.Label(dialog, text='Seleccione un alumno:')
        label.grid(row=0, column=0, columnspan=2)

        alumnos = obtener_alumnos()
        alumnos_names = [f'{alumno[1]} - {alumno[2]}' for alumno in alumnos]

        alumno_var = tk.StringVar(dialog)
        alumno_var.set(alumnos_names[0])

        alumnos_menu = tk.OptionMenu(dialog, alumno_var, *alumnos_names)
        alumnos_menu.grid(row=1, column=0, columnspan=2, pady=10)

        confirm_button = tk.Button(dialog, text='Confirmar', command=lambda: self.realizar_prestamo(id_libro, alumno_var.get()))
        confirm_button.grid(row=2, column=0, columnspan=2)

    def realizar_prestamo(self, id_libro, selected_alumno):
        nombre_alumno = selected_alumno.split('-')[0].strip()
        id_alumno = next((alumno[0] for alumno in obtener_alumnos() if alumno[1] == nombre_alumno), None)

        if id_alumno is not None:
            prestar_libro(id_libro, id_alumno)
            self.actualizar_lista_libros()
            self.master.destroy()

    def devolver_libro(self):
        selected_index = self.lista_libros.curselection()
        if selected_index:
            id_libro = int(selected_index[0]) + 1  # índice en la lista + 1
            devolver_libro(id_libro)
            self.actualizar_lista_libros()

    def actualizar_lista_libros(self):
        self.lista_libros.delete(0, tk.END)

        libros = obtener_libros()
        for libro in libros:
            estado = 'Disponible' if not libro[3] else f'Prestado a {libro[4]}'
            self.lista_libros.insert(tk.END, f'{libro[1]} - {libro[2]} ({estado})')

if __name__ == '__main__':
    root = tk.Tk()
    interfaz = InterfazBiblioteca(root)
    root.mainloop()
