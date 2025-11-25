1. usuarios
Columnas:
    id: INTEGER, PK, AUTOINCREMENT, NOT NULL
    email: TEXT, UNIQUE, NOT NULL
    password: TEXT, NOT NULL
    Restricciones: email es UNIQUE y NOT NULL; password es NOT NULL
    Índices: implícito en PK y UNIQUE(email)
Cardinalidad: 1:N con todas las demás tablas (cada usuario puede tener múltiples registros relacionados)

2. perfil
Columnas:
    id: INTEGER, PK, AUTOINCREMENT, NOT NULL
    usuario_id: INTEGER, FK a usuarios(id), UNIQUE, NOT NULL
    nombre: TEXT
    apellido: TEXT
    foto: TEXT
    descripcion: TEXT
    PK: id
    FK: usuario_id → usuarios(id)
    Restricciones: usuario_id es UNIQUE y NOT NULL
    Índices: implícito en PK y UNIQUE(usuario_id)
Cardinalidad: 1:1 con usuarios

3. contactos
Columnas:
    id: INTEGER, PK, AUTOINCREMENT, NOT NULL
    usuario_id: INTEGER, FK a usuarios(id), NOT NULL
    tipo: TEXT
    valor: TEXT
    PK: id
    FK: usuario_id → usuarios(id)
    Restricciones: usuario_id es NOT NULL
    Índices: implícito en PK
Cardinalidad: 1:N con usuarios

4. redes_sociales
Columnas:
    id: INTEGER, PK, AUTOINCREMENT, NOT NULL
    usuario_id: INTEGER, FK a usuarios(id), NOT NULL
    plataforma: TEXT
    link: TEXT
    PK: id
    FK: usuario_id → usuarios(id)
    Restricciones: usuario_id es NOT NULL
    Índices: implícito en PK
Cardinalidad: 1:N con usuarios

5. educacion
Columnas:
    id: INTEGER, PK, AUTOINCREMENT, NOT NULL
    usuario_id: INTEGER, FK a usuarios(id), NOT NULL
    institucion: TEXT
    titulo: TEXT
    fecha_inicio: TEXT
    fecha_fin: TEXT
    descripcion: TEXT
    PK: id
    FK: usuario_id → usuarios(id)
    Restricciones: usuario_id es NOT NULL
    Índices: implícito en PK
Cardinalidad: 1:N con usuarios

6. formacion
Columnas:
    id: INTEGER, PK, AUTOINCREMENT, NOT NULL
    usuario_id: INTEGER, FK a usuarios(id), NOT NULL
    nombre_curso: TEXT
    institucion: TEXT
    fecha_inicio: TEXT
    fecha_fin: TEXT
    descripcion: TEXT
    PK: id
    FK: usuario_id → usuarios(id)
    Restricciones: usuario_id es NOT NULL
    Índices: implícito en PK
Cardinalidad: 1:N con usuarios

7. habilidades
Columnas:
    id: INTEGER, PK, AUTOINCREMENT, NOT NULL
    usuario_id: INTEGER, FK a usuarios(id), NOT NULL
    nombre: TEXT
    nivel: TEXT
    categoria: TEXT
    PK: id
    FK: usuario_id → usuarios(id)
    Restricciones: usuario_id es NOT NULL
    Índices: implícito en PK
Cardinalidad: 1:N con usuarios

8. experiencia
Columnas:
    id: INTEGER, PK, AUTOINCREMENT, NOT NULL
    usuario_id: INTEGER, FK a usuarios(id), NOT NULL
    empresa: TEXT
    cargo: TEXT
    duracion: TEXT
    PK: id
    FK: usuario_id → usuarios(id)
    Restricciones: usuario_id es NOT NULL
    Índices: implícito en PK
Cardinalidad: 1:N con usuarios

9. recomendaciones
Columnas:
    id: INTEGER, PK, AUTOINCREMENT, NOT NULL
    usuario_id: INTEGER, FK a usuarios(id), NOT NULL
    nombre: TEXT
    cargo: TEXT
    comentario: TEXT
    contacto: TEXT
    PK: id
    FK: usuario_id → usuarios(id)
    Restricciones: usuario_id es NOT NULL
    Índices: implícito en PK
Cardinalidad: 1:N con usuarios

10. proyectos
Columnas:
    id: INTEGER, PK, AUTOINCREMENT, NOT NULL
    usuario_id: INTEGER, FK a usuarios(id), NOT NULL
    nombre: TEXT
    descripcion: TEXT
    imagen: TEXT
    url: TEXT
    fecha: TEXT
    PK: id
    FK: usuario_id → usuarios(id)
    Restricciones: usuario_id es NOT NULL
    Índices: implícito en PK
Cardinalidad: 1:N con