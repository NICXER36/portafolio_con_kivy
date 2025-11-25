import sqlite3

DB_NAME = "tareas.db"

def crear_tabla():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT UNIQUE,
            estado TEXT
        )
    """)
    conn.commit()
    conn.close()

def agregar_tarea(nombre):
    if not nombre.strip():
        return
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO tareas (titulo, estado) VALUES (?, ?)", (nombre, "pendiente"))
    conn.commit()
    conn.close()

def listar_tareas():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, titulo, estado FROM tareas")
    tareas = [{"id": row[0], "titulo": row[1], "estado": row[2]} for row in cursor.fetchall()]
    conn.close()
    return tareas

def completar_tarea(id_tarea):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE tareas SET estado = 'completada' WHERE id = ?", (id_tarea,))
    conn.commit()
    conn.close()
