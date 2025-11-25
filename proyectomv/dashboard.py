from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.card import MDCard
from kivy.metrics import dp
import random

# Colores para las tarjetas
COLORES_TARJETAS = [
    [0.2, 0.5, 0.85, 1],  # Azul
    [0.25, 0.65, 0.75, 1],  # Azul turquesa
    [0.3, 0.6, 0.8, 1],  # Azul claro
    [0.35, 0.55, 0.9, 1]  # Azul índigo
]

class RecuadroImagen(MDCard):
    def __init__(self, texto="", imagen="", destino="", **kwargs):
        super().__init__(**kwargs)
        self.texto = texto
        self.imagen = imagen
        self.destino = destino
        self.background_color = random.choice(COLORES_TARJETAS)
        self.md_bg_color = self.background_color
        self.elevation = 3
        self.orientation = 'vertical'
        self.padding = dp(12)
        self.spacing = dp(8)

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            try:
                from kivy.app import App
                app = App.get_running_app()
                if app and hasattr(app, 'root') and app.root:
                    app.root.current = self.destino
                return True
            except Exception as e:
                print(f"Error al navegar: {e}")
        return super().on_touch_down(touch)


class MenuScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
