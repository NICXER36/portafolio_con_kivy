from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.uix.behaviors import ButtonBehavior
from kivy.metrics import dp

from session import session
from database import (
    obtener_habilidades,
    agregar_habilidad,
    editar_habilidad,
    eliminar_habilidad
)

class ItemHabilidad(ButtonBehavior, MDLabel):
    def __init__(self, texto="", id_item=None, **kwargs):
        super().__init__(**kwargs)
        self.text = texto
        self.id_item = id_item
        self.theme_text_color = 'Primary'
        self.font_style = 'Body2'

class ListaConEliminar(MDBoxLayout):
    def __init__(self, titulo="", hint_text="", categoria="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(8)
        self.size_hint_y = None
        self.titulo = titulo
        self.hint_text = hint_text
        self.categoria = categoria
        self.seleccionado = None
        self.seleccionado_id = None
        self.dialog_agregar = None
        self.bind(minimum_height=self.setter('height'))

    def cargar_desde_bd(self, usuario_id):
        items_layout = self.ids.items_layout
        items_layout.clear_widgets()
        habilidades = obtener_habilidades(usuario_id)
        for hab in habilidades:
            if hab[3] == self.categoria:
                self._crear_fila(hab[1], hab[0])

    def _crear_fila(self, texto, id_item):
        items_layout = self.ids.items_layout
        fila = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30), spacing=dp(5))
        
        lbl = ItemHabilidad(text=texto, id_item=id_item)
        lbl.bind(on_press=lambda x: self.seleccionar(lbl, id_item))
        
        btn_del = MDFlatButton(
            text='✕',
            size_hint_x=None,
            width=dp(35),
            md_bg_color=[0.9, 0.3, 0.3, 1],
            text_color=[1, 1, 1, 1],
            font_size=dp(14)
        )
        btn_del.bind(on_press=lambda b: self.eliminar_fila(fila, lbl, id_item))
        
        fila.add_widget(lbl)
        fila.add_widget(btn_del)
        items_layout.add_widget(fila)

    def agregar(self, *args):
        """Muestra modal para agregar habilidad"""
        # Crear contenedor con tamaño fijo y mejor organización
        contenido = MDBoxLayout(
            orientation='vertical', 
            spacing=dp(15), 
            padding=[dp(25), dp(30), dp(25), dp(20)],
            size_hint_y=None,
            height=dp(200)
        )
        
        campo_nombre = MDTextField(
            hint_text=self.hint_text,
            mode='rectangle',
            font_size=dp(14),
            size_hint_y=None,
            height=dp(48)
        )
        
        contenido.add_widget(campo_nombre)
        
        self.dialog_agregar = MDDialog(
            title=f"Agregar {self.titulo}",
            type="custom",
            content_cls=contenido,
            buttons=[
                MDRaisedButton(
                    text="Cancelar",
                    on_press=lambda x, d=self.dialog_agregar: d.dismiss()
                ),
                MDRaisedButton(
                    text="Confirmar",
                    on_press=lambda x: self._confirmar_habilidad(campo_nombre)
                )
            ],
            size_hint=(0.95, None),
            height=dp(350)
        )
        self.dialog_agregar.open()
    
    def _confirmar_habilidad(self, campo_nombre):
        """Confirma y agrega la habilidad"""
        if self.dialog_agregar:
            self.dialog_agregar.dismiss()
            self.dialog_agregar = None
        
        texto = campo_nombre.text.strip()
        
        if texto:
            usuario_id = session.user_id
            nuevo_id = agregar_habilidad(usuario_id, texto, nivel="medio", categoria=self.categoria)
            if nuevo_id:
                self._crear_fila(texto, nuevo_id)

    def seleccionar(self, label, id_item, *args):
        input_field = self.ids.input_field
        self.seleccionado = label
        self.seleccionado_id = id_item
        input_field.text = label.text

    def eliminar_fila(self, fila, label, id_item, *args):
        """Elimina una fila con confirmación"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton
        
        def confirmar_eliminar(instance):
            items_layout = self.ids.items_layout
            input_field = self.ids.input_field
            
            if self.seleccionado == label:
                self.seleccionado = None
                self.seleccionado_id = None
                input_field.text = ''
            
            items_layout.remove_widget(fila)
            if id_item:
                eliminar_habilidad(id_item)
            
            if dialog:
                dialog.dismiss()
        
        def cancelar(instance):
            if dialog:
                dialog.dismiss()
        
        dialog = MDDialog(
            text="¿Estás seguro de que deseas eliminar este elemento?",
            buttons=[
                MDRaisedButton(
                    text="Cancelar",
                    on_press=cancelar
                ),
                MDRaisedButton(
                    text="Eliminar",
                    on_press=confirmar_eliminar
                )
            ]
        )
        dialog.open()

class HabilidadesScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.datos_originales = {}
        self.dialog = None
    
    def ir_dashboard(self, *args):
        """Verifica cambios antes de salir"""
        if self.hay_cambios():
            self.mostrar_dialogo_confirmacion(
                "Tienes cambios sin guardar. ¿Deseas salir sin guardar?",
                lambda: self._salir_sin_guardar(),
                lambda: None
            )
        else:
            self._salir_sin_guardar()
    
    def _salir_sin_guardar(self):
        """Sale de la pantalla sin guardar"""
        if self.dialog:
            self.dialog.dismiss()
        self.manager.current = 'dashboard'
    
    def mostrar_dialogo_confirmacion(self, mensaje, callback_si, callback_no=None):
        """Muestra un diálogo de confirmación"""
        if self.dialog:
            self.dialog.dismiss()
        
        self.dialog = MDDialog(
            text=mensaje,
            buttons=[
                MDRaisedButton(
                    text="Sí",
                    on_press=lambda x: self._ejecutar_callback(callback_si)
                ),
                MDRaisedButton(
                    text="No",
                    on_press=lambda x: self._ejecutar_callback(callback_no) if callback_no else self._cerrar_dialogo()
                )
            ]
        )
        self.dialog.open()
    
    def _ejecutar_callback(self, callback):
        """Ejecuta un callback y cierra el diálogo"""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
        if callback:
            callback()
    
    def _cerrar_dialogo(self):
        """Cierra el diálogo"""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None
    
    def guardar_estado_original(self):
        """Guarda el estado original de los datos"""
        self.datos_originales = {
            'lista1': [],
            'lista2': [],
            'lista3': []
        }
        
        for lista_id in ['lista1', 'lista2', 'lista3']:
            lista = self.ids[lista_id]
            items_layout = lista.ids.items_layout
            habilidades = []
            for fila in items_layout.children:
                for widget in fila.children:
                    if isinstance(widget, ItemHabilidad):
                        habilidades.append({
                            'id': widget.id_item,
                            'texto': widget.text
                        })
            self.datos_originales[lista_id] = habilidades
    
    def hay_cambios(self):
        """Verifica si hay cambios pendientes"""
        for lista_id in ['lista1', 'lista2', 'lista3']:
            lista = self.ids[lista_id]
            items_layout = lista.ids.items_layout
            habilidades_actuales = []
            for fila in items_layout.children:
                for widget in fila.children:
                    if isinstance(widget, ItemHabilidad):
                        habilidades_actuales.append({
                            'id': widget.id_item,
                            'texto': widget.text
                        })
            
            if habilidades_actuales != self.datos_originales.get(lista_id, []):
                return True
        
        for lista_id in ['lista1', 'lista2', 'lista3']:
            lista = self.ids[lista_id]
            input_field = lista.ids.input_field
            if input_field.text.strip():
                return True
        
        return False
    
    def guardar_todo(self, *args):
        """Guarda todos los cambios con confirmación"""
        self.mostrar_dialogo_confirmacion(
            "¿Deseas guardar los cambios?",
            self._guardar_todo_real
        )
    
    def _guardar_todo_real(self):
        """Guarda todos los cambios en la base de datos"""
        self.guardar_estado_original()
        self.mostrar_dialogo_confirmacion(
            "Cambios guardados exitosamente",
            self._cerrar_dialogo
        )

    def on_pre_enter(self, *args):
        usuario_id = session.user_id
        lista1 = self.ids.lista1
        lista2 = self.ids.lista2
        lista3 = self.ids.lista3
        
        lista1.cargar_desde_bd(usuario_id)
        lista2.cargar_desde_bd(usuario_id)
        lista3.cargar_desde_bd(usuario_id)
        
        self.guardar_estado_original()
