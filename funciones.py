import sqlite3
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
    cursor.execute('UPDATE libros SET prestado = ?, id_alumno = ? WHERE id = ?', (True, id_alumno, id_libro))
    conexion.commit()
    cerrar_bd(conexion)

def devolver_libro(id_libro):
    conexion, cursor = conectar_bd()
    cursor.execute('UPDATE libros SET prestado = ?, id_alumno = NULL WHERE id = ?', (False, id_libro))
    conexion.commit()
    cerrar_bd(conexion)
