# login.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog

from database import verificar_usuario
from session import session

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        # Los widgets se cargan desde el archivo .kv
        pass

    def validar_campos(self, *args):
        email_input = self.ids.email_input
        password_input = self.ids.password_input
        ingresar_btn = self.ids.ingresar_btn
        
        email = (email_input.text or "").strip()
        password = (password_input.text or "").strip()
        ingresar_btn.disabled = not (email and password)

    def verificar_credenciales_handler(self, *args):
        ingresar_btn = self.ids.ingresar_btn
        ingresar_btn.disabled = True
        try:
            self.verificar_credenciales()
        finally:
            ingresar_btn.disabled = False

    def verificar_credenciales(self):
        email_input = self.ids.email_input
        password_input = self.ids.password_input
        
        email = (email_input.text or "").strip()
        password = (password_input.text or "").strip()

        usuario = verificar_usuario(email, password)
        if usuario:
            # inicializar sesión compartida y cargar perfil si corresponde
            session.login(usuario)
            # navegar al dashboard
            self.manager.current = 'dashboard'
        else:
            self.mostrar_popup("Usuario o contraseña incorrectos", correcto=False)

    def mostrar_popup(self, mensaje, correcto):
        # Usar MDDialog de KivyMD
        titulo = '✓ Éxito' if correcto else '✗ Error'
        self.dialog = MDDialog(
            text=mensaje,
            title=titulo,
            buttons=[
                MDRaisedButton(
                    text="Cerrar",
                    on_press=lambda x: self.dialog.dismiss()
                )
            ]
        )
        self.dialog.open()

    def ir_registro(self, *args):
        self.manager.current = 'registro'
