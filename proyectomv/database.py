# database.py
import sqlite3
import os
import hashlib
import binascii

DB_NAME = "portafolio.db"


def crear_bd():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    
    # Leer y ejecutar el archivo schema.sql usando ruta relativa
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    schema_path = os.path.join(base_dir, 'schema.sql')
    
    # Si no existe en la ruta relativa, intentar otras rutas posibles
    if not os.path.exists(schema_path):
        posibles_rutas = [
            'kivy_mov/share/proyectomv/schema.sql',
            os.path.join(os.getcwd(), 'schema.sql'),
            os.path.join(os.path.dirname(os.getcwd()), 'schema.sql')
        ]
        for ruta in posibles_rutas:
            if os.path.exists(ruta):
                schema_path = ruta
                break
    
    if os.path.exists(schema_path):
        try:
            with open(schema_path, 'r', encoding='utf-8') as f:
                script = f.read()
                cursor.executescript(script)
        except Exception as e:
            print(f"Error al leer schema.sql: {e}")
            # Crear tablas básicas si falla
            _crear_tablas_manual(cursor)
    else:
        # Crear tablas directamente si no se encuentra el archivo
        _crear_tablas_manual(cursor)
    
    conn.commit()
    conn.close()

def _crear_tablas_manual(cursor):
    """Crea las tablas manualmente si no se encuentra schema.sql"""
    tablas = [
        """CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )""",
        """CREATE TABLE IF NOT EXISTS perfil (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER UNIQUE NOT NULL,
            nombre TEXT,
            apellido TEXT,
            foto TEXT,
            descripcion TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )""",
        """CREATE TABLE IF NOT EXISTS contactos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            tipo TEXT,
            valor TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )""",
        """CREATE TABLE IF NOT EXISTS redes_sociales (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            plataforma TEXT,
            link TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )""",
        """CREATE TABLE IF NOT EXISTS educacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            institucion TEXT,
            titulo TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT,
            descripcion TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )""",
        """CREATE TABLE IF NOT EXISTS formacion (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nombre_curso TEXT,
            institucion TEXT,
            fecha_inicio TEXT,
            fecha_fin TEXT,
            descripcion TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )""",
        """CREATE TABLE IF NOT EXISTS habilidades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nombre TEXT,
            nivel TEXT,
            categoria TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )""",
        """CREATE TABLE IF NOT EXISTS experiencia (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            empresa TEXT,
            cargo TEXT,
            duracion TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )""",
        """CREATE TABLE IF NOT EXISTS recomendaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nombre TEXT,
            cargo TEXT,
            comentario TEXT,
            contacto TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )""",
        """CREATE TABLE IF NOT EXISTS proyectos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            nombre TEXT,
            descripcion TEXT,
            imagen TEXT,
            url TEXT,
            fecha TEXT,
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )"""
    ]
    for tabla in tablas:
        cursor.execute(tabla)


# USUARIOS
def registrar_usuario(email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("INSERT INTO usuarios (email, password) VALUES (?, ?)", (email, password))
    usuario_id = c.lastrowid
    
    c.execute("INSERT INTO perfil (usuario_id) VALUES (?)", (usuario_id,))
    conn.commit()
    conn.close()
    return usuario_id

def verificar_usuario(email, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("SELECT id, email, password FROM usuarios WHERE email=?", (email,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    
    if row[2] == password:
        return {"id": row[0], "email": row[1]}
    
    return None


# PERFILES 
def obtener_perfil(usuario_id):
    if usuario_id is None:
        return None
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""SELECT id, usuario_id, nombre, apellido, descripcion, foto
                 FROM perfil WHERE usuario_id=?""", (usuario_id,))
    row = c.fetchone()
    conn.close()
    if not row:
        return None
    keys = ["id", "usuario_id", "nombre", "apellido", "descripcion", "foto"]
    return dict(zip(keys, row))

def actualizar_perfil(usuario_id, nombre=None, apellido=None, descripcion=None, foto=None):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        UPDATE perfil SET nombre=?, apellido=?, descripcion=?, foto=?
        WHERE usuario_id=?
    """, (nombre, apellido, descripcion, foto, usuario_id))
    conn.commit()
    conn.close()
    return c.rowcount > 0

# ---------------- CONTACTOS ----------------
def agregar_contacto(usuario_id, tipo, valor):
    if usuario_id is None:
        return None
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO contactos (usuario_id, tipo, valor) VALUES (?, ?, ?)",
        (usuario_id, tipo, valor)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid

def editar_contacto(contacto_id, tipo, valor):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE contactos SET tipo=?, valor=? WHERE id=?",
        (tipo, valor, contacto_id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def obtener_contactos(usuario_id):
    if usuario_id is None:
        return []
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, tipo, valor FROM contactos WHERE usuario_id=?",
        (usuario_id,)
    )
    contactos = cursor.fetchall()
    conn.close()
    return contactos

# ---------------- REDES SOCIALES ----------------
def agregar_red(usuario_id, plataforma, link):
    if usuario_id is None:
        return None
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO redes_sociales (usuario_id, plataforma, link) VALUES (?, ?, ?)",
        (usuario_id, plataforma, link)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid

def editar_red(red_id, plataforma, link):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE redes_sociales SET plataforma=?, link=? WHERE id=?",
        (plataforma, link, red_id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def obtener_redes(usuario_id):
    if usuario_id is None:
        return []
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, plataforma, link FROM redes_sociales WHERE usuario_id=?",
        (usuario_id,)
    )
    redes = cursor.fetchall()
    conn.close()
    return redes

# ---------------- EDUCACION ----------------
def agregar_educacion(usuario_id, institucion, titulo, fecha_inicio=None, fecha_fin=None, descripcion=None):
    if usuario_id is None:
        return None
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO educacion (usuario_id, institucion, titulo, fecha_inicio, fecha_fin, descripcion) VALUES (?, ?, ?, ?, ?, ?)",
        (usuario_id, institucion, titulo, fecha_inicio, fecha_fin, descripcion)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid
    
def eliminar_educacion(educacion_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM educacion WHERE id=?", (educacion_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


def editar_educacion(edu_id, institucion, titulo, fecha_inicio, fecha_fin, descripcion):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE educacion SET institucion=?, titulo=?, fecha_inicio=?, fecha_fin=?, descripcion=? WHERE id=?",
        (institucion, titulo, fecha_inicio, fecha_fin, descripcion, edu_id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def obtener_educacion(usuario_id):
    if usuario_id is None:
        return []
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, institucion, titulo, fecha_inicio, fecha_fin, descripcion FROM educacion WHERE usuario_id=?",
        (usuario_id,)
    )
    educacion = cursor.fetchall()
    conn.close()
    return educacion

# ---------------- HABILIDADES ----------------
def agregar_habilidad(usuario_id, nombre, nivel, categoria=None):
    if usuario_id is None:
        return None
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO habilidades (usuario_id, nombre, nivel, categoria) VALUES (?, ?, ?, ?)",
        (usuario_id, nombre, nivel, categoria)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid

def editar_habilidad(hab_id, nombre=None, nivel=None, categoria=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    campos = []
    valores = []

    if nombre is not None:
        campos.append("nombre=?")
        valores.append(nombre)
    if nivel is not None:
        campos.append("nivel=?")
        valores.append(nivel)
    if categoria is not None:
        campos.append("categoria=?")
        valores.append(categoria)

    if not campos:
        conn.close()
        return False  # nada que actualizar

    query = f"UPDATE habilidades SET {', '.join(campos)} WHERE id=?"
    valores.append(hab_id)
    cursor.execute(query, valores)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

    
def eliminar_habilidad(habilidad_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM habilidades WHERE id=?", (habilidad_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def obtener_habilidades(usuario_id):
    if usuario_id is None:
        return []
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, nivel, categoria FROM habilidades WHERE usuario_id=?",
        (usuario_id,)
    )
    habilidades = cursor.fetchall()
    conn.close()
    return habilidades

# ---------------- EXPERIENCIA ----------------
def agregar_experiencia(usuario_id, empresa, cargo, duracion):
    if usuario_id is None:
        return None
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO experiencia (usuario_id, empresa, cargo, duracion) VALUES (?, ?, ?, ?)",
        (usuario_id, empresa, cargo, duracion)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid
def eliminar_experiencia(experiencia_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM experiencia WHERE id=?", (experiencia_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def editar_experiencia(exp_id, empresa, cargo, duracion):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE experiencia SET empresa=?, cargo=?, duracion=? WHERE id=?",
        (empresa, cargo, duracion, exp_id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def obtener_experiencia(usuario_id):
    if usuario_id is None:
        return []
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, empresa, cargo, duracion FROM experiencia WHERE usuario_id=?",
        (usuario_id,)
    )
    experiencia = cursor.fetchall()
    conn.close()
    return experiencia



# ---------------- RECOMENDACIONES ----------------
def agregar_recomendacion(usuario_id, nombre, cargo, comentario, contacto=None):
    if usuario_id is None:
        return None
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO recomendaciones (usuario_id, nombre, cargo, comentario, contacto) VALUES (?, ?, ?, ?, ?)",
        (usuario_id, nombre, cargo, comentario, contacto)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid

def editar_recomendacion(rec_id, nombre, cargo, comentario, contacto):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE recomendaciones SET nombre=?, cargo=?, comentario=?, contacto=? WHERE id=?",
        (nombre, cargo, comentario, contacto, rec_id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def obtener_recomendaciones(usuario_id):
    if usuario_id is None:
        return []
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, cargo, comentario, contacto FROM recomendaciones WHERE usuario_id=?",
        (usuario_id,)
    )
    recomendaciones = cursor.fetchall()
    conn.close()
    return recomendaciones
    
def eliminar_recomendacion(recomendacion_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM recomendaciones WHERE id=?", (recomendacion_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0


# ---------------- PROYECTOS ----------------
def agregar_proyecto(usuario_id, nombre, descripcion, imagen=None, url=None, fecha=None):
    if usuario_id is None:
        return None
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO proyectos (usuario_id, nombre, descripcion, imagen, url, fecha) VALUES (?, ?, ?, ?, ?, ?)",
        (usuario_id, nombre, descripcion, imagen, url, fecha)
    )
    conn.commit()
    conn.close()
    return cursor.lastrowid

def editar_proyecto(proy_id, nombre, descripcion, imagen, url, fecha):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE proyectos SET nombre=?, descripcion=?, imagen=?, url=?, fecha=? WHERE id=?",
        (nombre, descripcion, imagen, url, fecha, proy_id)
    )
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

def obtener_proyectos(usuario_id):
    if usuario_id is None:
        return []
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, nombre, descripcion, imagen, url, fecha FROM proyectos WHERE usuario_id=?",
        (usuario_id,)
    )
    proyectos = cursor.fetchall()
    conn.close()
    return proyectos
    
# Obtener todas las formaciones de un usuario
def obtener_formacion(usuario_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, nombre_curso, institucion, fecha_inicio, fecha_fin, descripcion
        FROM formacion
        WHERE usuario_id=?
    """, (usuario_id,))
    formacion = cursor.fetchall()
    conn.close()
    return formacion

# Agregar una nueva formación
def agregar_formacion(usuario_id, nombre_curso, institucion, fecha_inicio, fecha_fin, descripcion):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO formacion (usuario_id, nombre_curso, institucion, fecha_inicio, fecha_fin, descripcion)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (usuario_id, nombre_curso, institucion, fecha_inicio, fecha_fin, descripcion))
    conn.commit()
    conn.close()
    return cursor.lastrowid

# Editar una formación existente
def editar_formacion(formacion_id, nombre_curso=None, institucion=None, fecha_inicio=None, fecha_fin=None, descripcion=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    campos = []
    valores = []

    if nombre_curso is not None:
        campos.append("nombre_curso=?")
        valores.append(nombre_curso)
    if institucion is not None:
        campos.append("institucion=?")
        valores.append(institucion)
    if fecha_inicio is not None:
        campos.append("fecha_inicio=?")
        valores.append(fecha_inicio)
    if fecha_fin is not None:
        campos.append("fecha_fin=?")
        valores.append(fecha_fin)
    if descripcion is not None:
        campos.append("descripcion=?")
        valores.append(descripcion)

    if not campos:
        conn.close()
        return False

    query = f"UPDATE formacion SET {', '.join(campos)} WHERE id=?"
    valores.append(formacion_id)
    cursor.execute(query, valores)
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

# Eliminar una formación
def eliminar_formacion(formacion_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM formacion WHERE id=?", (formacion_id,))
    conn.commit()
    conn.close()
    return cursor.rowcount > 0

