# registro.py
import re
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

from database import registrar_usuario


class Registro_Screen(MDScreen):
    def __init__(self, **kwargs):
        super(Registro_Screen, self).__init__(**kwargs)

        # Los widgets se cargan desde el archivo .kv
        self.indicadores = {}

   
    def es_email_valido(self, email):
        patron = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(patron, email) is not None

    def validar_email(self, *args):
        email_input = self.ids.email_input
        if not self.es_email_valido(email_input.text.strip()):
            email_input.error = True
            email_input.helper_text = "Formato de correo inválido"
        else:
            email_input.error = False
            email_input.helper_text = ""

    def validar_passwords(self, *args):
        password_input = self.ids.password_input
        confirm_input = self.ids.confirm_input
        
        if password_input.text and confirm_input.text:
            if password_input.text != confirm_input.text:
                confirm_input.error = True
                confirm_input.helper_text = "Las contraseñas no coinciden"
            else:
                confirm_input.error = False
                confirm_input.helper_text = ""


    
    def registrar_usuario_handler(self, *args):
        registrar_btn = self.ids.registrar_btn
        registrar_btn.disabled = True
        try:
            self._registrar_usuario()
        finally:
            registrar_btn.disabled = False

    def _registrar_usuario(self):
        email_input = self.ids.email_input
        password_input = self.ids.password_input
        confirm_input = self.ids.confirm_input
        
        email = (email_input.text or "").strip()
        password = (password_input.text or "").strip()
        confirm = (confirm_input.text or "").strip()

        if not email or not password or not confirm:
            self.mostrar_popup("Todos los campos son obligatorios", correcto=False)
            return

        if not self.es_email_valido(email):
            self.mostrar_popup("Formato de correo no válido", correcto=False)
            return

        if password != confirm:
            self.mostrar_popup("Las contraseñas no coinciden", correcto=False)
            return

        # Intentamos registrar en la base de datos
        try:
            usuario_id = registrar_usuario(email, password)
        except Exception as e:
            usuario_id = None
            print("Error al llamar a registrar_usuario:", e)

        if usuario_id:
            self.mostrar_popup("Usuario registrado con éxito", correcto=True)
            # limpiar campos
            email_input.text = ""
            password_input.text = ""
            confirm_input.text = ""
            # regresar al login para que inicie sesión
            self.manager.current = 'login'
        else:
            self.mostrar_popup("El correo ya está registrado o hubo un error", correcto=False)

    def mostrar_popup(self, mensaje, correcto):
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

    def volver_login(self, *args):
        self.manager.current = 'login'
