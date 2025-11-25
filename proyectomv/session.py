# session.py
class UserSession:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UserSession, cls).__new__(cls)
            cls._instance._reset()
        return cls._instance

    def _reset(self):
        self.user_id = None
        self.email = None
        self.nombre = None
        self.apellido = None
        self.foto = None
        self.descripcion = None

    def login(self, user_dict):
        self.user_id = user_dict.get("id")
        self.email = user_dict.get("email")
        self.nombre = user_dict.get("nombre")
        self.apellido = user_dict.get("apellido")
        self.foto = user_dict.get("foto")
        self.descripcion = user_dict.get("descripcion")

    def logout(self):
        self._reset()

    def is_authenticated(self):
        return self.user_id is not None

# instancia compartida para importar desde las pantallas
session = UserSession()
