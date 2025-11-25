-- autenticación
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
);

-- perfil (separado)
CREATE TABLE IF NOT EXISTS perfil (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER UNIQUE NOT NULL,
    nombre TEXT,
    apellido TEXT,
    foto TEXT,
    descripcion TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- contactos
CREATE TABLE IF NOT EXISTS contactos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    tipo TEXT,
    valor TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- redes 
CREATE TABLE IF NOT EXISTS redes_sociales (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    plataforma TEXT,
    link TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- educacion
CREATE TABLE IF NOT EXISTS educacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    institucion TEXT,
    titulo TEXT,
    fecha_inicio TEXT,
    fecha_fin TEXT,
    descripcion TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

--formacion
CREATE TABLE IF NOT EXISTS formacion (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    nombre_curso TEXT,
    institucion TEXT,
    fecha_inicio TEXT,
    fecha_fin TEXT,
    descripcion TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

-- habilidades
CREATE TABLE IF NOT EXISTS habilidades (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    nombre TEXT,
    nivel TEXT,
    categoria TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

--experiencia
CREATE TABLE IF NOT EXISTS experiencia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    empresa TEXT,
    cargo TEXT,
    duracion TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

--recomendaciones
CREATE TABLE IF NOT EXISTS recomendaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    nombre TEXT,
    cargo TEXT,
    comentario TEXT,
    contacto TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

--proyectos
CREATE TABLE IF NOT EXISTS proyectos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER NOT NULL,
    nombre TEXT,
    descripcion TEXT,
    imagen TEXT,
    url TEXT,
    fecha TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);
