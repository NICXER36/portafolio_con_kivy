from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from kivy.core.window import Window
from login import LoginScreen
from dashboard import MenuScreen
from formacion import FormacionScreen
from habilidades import HabilidadesScreen
from experiencia import ExperienciaScreen
from perfil import PerfilScreen
from registro import Registro_Screen
from database import crear_bd

# Configuración para móvil
Window.size = (360, 640)  # Ancho x Alto para móvil vertical

crear_bd() 


class MyApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.primary_hue = "500"
    
    def build(self):
        # Cargar archivos .kv manualmente
        from kivy.lang import Builder
        import os
        
        kv_files = ['login.kv', 'registro.kv', 'dashboard.kv', 'perfil.kv', 'formacion.kv', 'habilidades.kv', 'experiencia.kv']
        for kv_file in kv_files:
            kv_path = os.path.join(os.path.dirname(__file__), kv_file)
            if os.path.exists(kv_path):
                Builder.load_file(kv_path)
        
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MenuScreen(name='dashboard'))
        sm.add_widget(FormacionScreen(name='formacion'))
        sm.add_widget(HabilidadesScreen(name='habilidades'))
        sm.add_widget(ExperienciaScreen(name='experiencia'))
        sm.add_widget(PerfilScreen(name='perfil'))
        sm.add_widget(Registro_Screen(name='registro'))
        return sm

if __name__ == '__main__':
    MyApp().run()
