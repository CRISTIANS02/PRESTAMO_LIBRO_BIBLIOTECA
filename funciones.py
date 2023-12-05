import sqlite3
from datetime import datetime
import orm

def conectar_bd():
    conexion = sqlite3.connect('biblioteca_jma_2023.db')
    cursor = conexion.cursor()

    # Crear tablas si no existen
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            dni TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS libros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT,
            autor TEXT,
            prestado BOOLEAN,
            id_alumno INTEGER,
            fecha_prestamo TEXT,
            fecha_devolucion TEXT,
            FOREIGN KEY (id_alumno) REFERENCES alumnos (id)
        )
    ''')

    conexion.commit()
    return conexion, cursor

def cerrar_bd(conexion):
    conexion.close()

def agregar_alumno(nombre, dni):
    conexion, cursor = conectar_bd()
    cursor.execute('INSERT INTO alumnos (nombre, dni) VALUES (?, ?)', (nombre, dni))
    conexion.commit()
    cerrar_bd(conexion)

def obtener_alumnos():
    conexion, cursor = conectar_bd()
    cursor.execute('SELECT * FROM alumnos')
    alumnos = cursor.fetchall()
    cerrar_bd(conexion)
    return alumnos

def agregar_libro(titulo, autor):
    conexion, cursor = conectar_bd()
    cursor.execute('INSERT INTO libros (titulo, autor, prestado) VALUES (?, ?, ?)', (titulo, autor, False))
    conexion.commit()
    cerrar_bd(conexion)

def obtener_libros():
    conexion, cursor = conectar_bd()
    cursor.execute('SELECT * FROM libros')
    libros = cursor.fetchall()
    cerrar_bd(conexion)
    return libros

def prestar_libro(id_libro, id_alumno):
    conexion, cursor = conectar_bd()
    fecha_prestamo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('UPDATE libros SET prestado = ?, id_alumno = ?, fecha_prestamo = ? WHERE id = ?', (True, id_alumno, fecha_prestamo, id_libro))
    conexion.commit()
    cerrar_bd(conexion)

def devolver_libro(id_libro):
    conexion, cursor = conectar_bd()
    fecha_devolucion = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute('UPDATE libros SET prestado = ?, id_alumno = NULL, fecha_devolucion = ? WHERE id = ?', (False, fecha_devolucion, id_libro))
    conexion.commit()
    cerrar_bd(conexion)


