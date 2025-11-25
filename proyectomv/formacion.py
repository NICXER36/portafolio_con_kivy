from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.metrics import dp

from session import session
from database import (
    obtener_formacion, agregar_formacion, editar_formacion, eliminar_formacion,
    obtener_educacion, agregar_educacion, editar_educacion, eliminar_educacion
)

class FilaHorizontal(MDBoxLayout):
    def __init__(self, campos, id_item=None, eliminar_callback=None, editar_callback=None, tipo_item=None, **kwargs):
        super().__init__(**kwargs)
        self.campos = campos
        self.id_item = id_item
        self.eliminar_callback = eliminar_callback
        self.editar_callback = editar_callback
        self.tipo_item = tipo_item  # 'formacion' o 'educacion'
        self._configure_fields()

    def _configure_fields(self):
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self._set_fields(), 0.1)

    def _set_fields(self):
        if not hasattr(self, 'ids') or not self.ids:
            return
        for i, (texto, hint) in enumerate(self.campos):
            input_id = f'input_{i}'
            if input_id in self.ids:
                inp = self.ids[input_id]
                inp.text = texto
                inp.hint_text = hint
                # Agregar listener para detectar campos vacíos
                inp.bind(text=self._verificar_campos_vacios)
    
    def _verificar_campos_vacios(self, *args):
        """Verifica si todos los campos están vacíos y elimina automáticamente"""
        datos = self.get_data()
        if all(not dato.strip() for dato in datos):
            # Si tiene id_item, eliminar de la base de datos
            if self.id_item and self.editar_callback:
                self.editar_callback(self.id_item)
            
            # Eliminar de la UI (tanto si tiene id_item como si no)
            if self.eliminar_callback:
                self.eliminar_callback(self)

    def get_data(self):
        inputs = [self.ids.get(f'input_{i}') for i in range(5) if f'input_{i}' in self.ids]
        return [inp.text.strip() if inp else "" for inp in inputs]

    def eliminar(self, *args):
        if self.eliminar_callback:
            self.eliminar_callback(self)
        if self.id_item and self.editar_callback:
            self.editar_callback(self.id_item)

class FormacionScreen(MDScreen):
    def __init__(self, titulo="Formación y Educación", **kwargs):
        super().__init__(**kwargs)
        self.datos_originales = {}
        self.dialog = None
        self.dialog_agregar = None
    
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
            'formacion': [],
            'educacion': []
        }
        
        formacion_container = self.ids.formacion_container
        for fila in formacion_container.children:
            datos = fila.get_data()
            self.datos_originales['formacion'].append({
                'id': fila.id_item,
                'datos': datos
            })
        
        educacion_container = self.ids.educacion_container
        for fila in educacion_container.children:
            datos = fila.get_data()
            self.datos_originales['educacion'].append({
                'id': fila.id_item,
                'datos': datos
            })
    
    def hay_cambios(self):
        """Verifica si hay cambios pendientes"""
        formacion_container = self.ids.formacion_container
        formacion_actual = []
        for fila in formacion_container.children:
            datos = fila.get_data()
            formacion_actual.append({
                'id': fila.id_item,
                'datos': datos
            })
        
        if formacion_actual != self.datos_originales.get('formacion', []):
            return True
        
        educacion_container = self.ids.educacion_container
        educacion_actual = []
        for fila in educacion_container.children:
            datos = fila.get_data()
            educacion_actual.append({
                'id': fila.id_item,
                'datos': datos
            })
        
        if educacion_actual != self.datos_originales.get('educacion', []):
            return True
        
        return False

    def on_pre_enter(self, *args):
        usuario_id = session.user_id
        formacion_container = self.ids.formacion_container
        educacion_container = self.ids.educacion_container
        
        formacion_container.clear_widgets()
        for item in obtener_formacion(usuario_id):
            fila = FilaHorizontal(
                campos=[
                    (item[1], "Curso"),
                    (item[2], "Institución"),
                    (item[3], "Inicio"),
                    (item[4], "Fin"),
                    (item[5], "Descripción")
                ],
                id_item=item[0],
                eliminar_callback=formacion_container.remove_widget,
                editar_callback=eliminar_formacion,
                tipo_item='formacion'
            )
            formacion_container.add_widget(fila)

        educacion_container.clear_widgets()
        for item in obtener_educacion(usuario_id):
            fila = FilaHorizontal(
                campos=[
                    (item[1], "Institución"),
                    (item[2], "Título"),
                    (item[3], "Inicio"),
                    (item[4], "Fin"),
                    (item[5], "Descripción")
                ],
                id_item=item[0],
                eliminar_callback=educacion_container.remove_widget,
                editar_callback=eliminar_educacion,
                tipo_item='educacion'
            )
            educacion_container.add_widget(fila)
        
        self.guardar_estado_original()

    def agregar_formacion(self, *args):
        """Muestra modal para agregar formación"""
        # Crear contenedor con tamaño fijo y mejor organización
        contenido = MDBoxLayout(
            orientation='vertical', 
            spacing=dp(15), 
            padding=[dp(25), dp(30), dp(25), dp(20)],
            size_hint_y=None,
            height=dp(450)
        )
        
        # Primera fila: Curso e Institución
        fila1 = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(48))
        campo_curso = MDTextField(hint_text="Curso", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
        campo_institucion = MDTextField(hint_text="Institución", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
        fila1.add_widget(campo_curso)
        fila1.add_widget(campo_institucion)
        
        # Segunda fila: Fechas
        fila2 = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(48))
        campo_inicio = MDTextField(hint_text="Fecha Inicio", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
        campo_fin = MDTextField(hint_text="Fecha Fin", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
        fila2.add_widget(campo_inicio)
        fila2.add_widget(campo_fin)
        
        # Tercera fila: Descripción (ancho completo)
        campo_descripcion = MDTextField(
            hint_text="Descripción", 
            mode='rectangle', 
            multiline=True, 
            font_size=dp(14), 
            size_hint_y=None, 
            height=dp(120)
        )
        
        contenido.add_widget(fila1)
        contenido.add_widget(fila2)
        contenido.add_widget(campo_descripcion)
        
        self.dialog_agregar = MDDialog(
            title="Agregar Formación",
            type="custom",
            content_cls=contenido,
            buttons=[
                MDRaisedButton(
                    text="Cancelar",
                    on_press=lambda x, d=self.dialog_agregar: d.dismiss()
                ),
                MDRaisedButton(
                    text="Confirmar",
                    on_press=lambda x: self._confirmar_formacion(campo_curso, campo_institucion, campo_inicio, campo_fin, campo_descripcion)
                )
            ],
            size_hint=(0.95, None),
            height=dp(600)
        )
        self.dialog_agregar.open()
    
    def _confirmar_formacion(self, campo_curso, campo_institucion, campo_inicio, campo_fin, campo_descripcion):
        """Confirma y agrega la formación"""
        if self.dialog_agregar:
            self.dialog_agregar.dismiss()
        
        formacion_container = self.ids.formacion_container
        fila = FilaHorizontal(
            campos=[
                (campo_curso.text.strip(), "Curso"),
                (campo_institucion.text.strip(), "Institución"),
                (campo_inicio.text.strip(), "Inicio"),
                (campo_fin.text.strip(), "Fin"),
                (campo_descripcion.text.strip(), "Descripción")
            ],
            eliminar_callback=formacion_container.remove_widget,
            editar_callback=eliminar_formacion,
            tipo_item='formacion'
        )
        formacion_container.add_widget(fila)

    def agregar_educacion(self, *args):
        """Muestra modal para agregar educación"""
        # Crear contenedor con tamaño fijo y mejor organización
        contenido = MDBoxLayout(
            orientation='vertical', 
            spacing=dp(15), 
            padding=[dp(25), dp(30), dp(25), dp(20)],
            size_hint_y=None,
            height=dp(450)
        )
        
        # Primera fila: Institución y Título
        fila1 = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(48))
        campo_institucion = MDTextField(hint_text="Institución", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
        campo_titulo = MDTextField(hint_text="Título", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
        fila1.add_widget(campo_institucion)
        fila1.add_widget(campo_titulo)
        
        # Segunda fila: Fechas
        fila2 = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(48))
        campo_inicio = MDTextField(hint_text="Fecha Inicio", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
        campo_fin = MDTextField(hint_text="Fecha Fin", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
        fila2.add_widget(campo_inicio)
        fila2.add_widget(campo_fin)
        
        # Tercera fila: Descripción (ancho completo)
        campo_descripcion = MDTextField(
            hint_text="Descripción", 
            mode='rectangle', 
            multiline=True, 
            font_size=dp(14), 
            size_hint_y=None, 
            height=dp(120)
        )
        
        contenido.add_widget(fila1)
        contenido.add_widget(fila2)
        contenido.add_widget(campo_descripcion)
        
        self.dialog_agregar = MDDialog(
            title="Agregar Educación",
            type="custom",
            content_cls=contenido,
            buttons=[
                MDRaisedButton(
                    text="Cancelar",
                    on_press=lambda x, d=self.dialog_agregar: d.dismiss()
                ),
                MDRaisedButton(
                    text="Confirmar",
                    on_press=lambda x: self._confirmar_educacion(campo_institucion, campo_titulo, campo_inicio, campo_fin, campo_descripcion)
                )
            ],
            size_hint=(0.95, None),
            height=dp(600)
        )
        self.dialog_agregar.open()
    
    def _confirmar_educacion(self, campo_institucion, campo_titulo, campo_inicio, campo_fin, campo_descripcion):
        """Confirma y agrega la educación"""
        if self.dialog_agregar:
            self.dialog_agregar.dismiss()
        
        educacion_container = self.ids.educacion_container
        fila = FilaHorizontal(
            campos=[
                (campo_institucion.text.strip(), "Institución"),
                (campo_titulo.text.strip(), "Título"),
                (campo_inicio.text.strip(), "Inicio"),
                (campo_fin.text.strip(), "Fin"),
                (campo_descripcion.text.strip(), "Descripción")
            ],
            eliminar_callback=educacion_container.remove_widget,
            editar_callback=eliminar_educacion,
            tipo_item='educacion'
        )
        educacion_container.add_widget(fila)

    def guardar_todo(self, *args):
        """Guarda los cambios con confirmación"""
        self.mostrar_dialogo_confirmacion(
            "¿Deseas guardar los cambios?",
            self._guardar_todo_real
        )
    
    def _guardar_todo_real(self):
        """Guarda los cambios en la base de datos"""
        usuario_id = session.user_id
        formacion_container = self.ids.formacion_container
        educacion_container = self.ids.educacion_container

        for fila in formacion_container.children:
            datos = fila.get_data()
            if fila.id_item:
                editar_formacion(fila.id_item,
                                 nombre_curso=datos[0],
                                 institucion=datos[1],
                                 fecha_inicio=datos[2],
                                 fecha_fin=datos[3],
                                 descripcion=datos[4])
            elif any(datos):
                nuevo_id = agregar_formacion(usuario_id, *datos)
                fila.id_item = nuevo_id

        for fila in educacion_container.children:
            datos = fila.get_data()
            if fila.id_item:
                editar_educacion(fila.id_item,
                                 institucion=datos[0],
                                 titulo=datos[1],
                                 fecha_inicio=datos[2],
                                 fecha_fin=datos[3],
                                 descripcion=datos[4])
            elif any(datos):
                nuevo_id = agregar_educacion(usuario_id, *datos)
                fila.id_item = nuevo_id
        
        self.guardar_estado_original()
        
        # Mostrar mensaje de éxito
        self.mostrar_dialogo_confirmacion(
            "Cambios guardados exitosamente",
            self._cerrar_dialogo
        )
