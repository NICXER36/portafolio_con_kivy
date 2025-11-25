from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.textfield import MDTextField
from kivy.metrics import dp

from session import session
from database import (
    obtener_experiencia, agregar_experiencia, editar_experiencia, eliminar_experiencia,
    obtener_recomendaciones, agregar_recomendacion, editar_recomendacion, eliminar_recomendacion
)

class FilaEditable(MDBoxLayout):
    def __init__(self, campos, id_item=None, eliminar_callback=None, seleccionar_callback=None, tipo_item=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.spacing = dp(8)
        self.padding = [dp(10), dp(8)]
        self.md_bg_color = [0.95, 0.95, 0.95, 1]
        self.radius = [dp(8)]
        
        self.campos = campos
        self.id_item = id_item
        self.eliminar_callback = eliminar_callback
        self.seleccionar_callback = seleccionar_callback
        self.tipo_item = tipo_item
        
        self._crear_widgets()

    def _crear_widgets(self):
        # Primera fila: Campos principales
        fila1 = MDBoxLayout(orientation='horizontal', size_hint_y=None, height=dp(48), spacing=dp(8))
        self.input_0 = MDTextField(
            mode='rectangle',
            font_size=dp(13),
            size_hint_x=0.5
        )
        self.input_1 = MDTextField(
            mode='rectangle',
            font_size=dp(13),
            size_hint_x=0.5
        )
        fila1.add_widget(self.input_0)
        fila1.add_widget(self.input_1)
        
        # Segunda fila: Campo adicional + botón eliminar
        fila2 = MDBoxLayout(
            orientation='horizontal', 
            size_hint_y=None, 
            height=dp(80) if self.tipo_item == "recomendacion" else dp(48),
            spacing=dp(8)
        )
        self.input_2 = MDTextField(
            mode='rectangle',
            font_size=dp(13),
            multiline=(self.tipo_item == "recomendacion"),
            size_hint_x=0.9
        )
        btn_eliminar = MDFlatButton(
            text='X',
            size_hint_x=None,
            width=dp(40),
            md_bg_color=[1, 0, 0, 1],
            text_color=[1, 1, 1, 1],
            font_size=dp(14),
            on_press=self.eliminar
        )
        fila2.add_widget(self.input_2)
        fila2.add_widget(btn_eliminar)
        
        # Tercera fila: Campo de contacto (solo para recomendaciones)
        self.input_3 = MDTextField(
            mode='rectangle',
            font_size=dp(13),
            size_hint_x=1,
            size_hint_y=None,
            height=dp(48) if self.tipo_item == "recomendacion" else 0,
            opacity=1 if self.tipo_item == "recomendacion" else 0,
            disabled=False if self.tipo_item == "recomendacion" else True
        )
        
        self.add_widget(fila1)
        self.add_widget(fila2)
        if self.tipo_item == "recomendacion":
            self.add_widget(self.input_3)
        
        # Configurar campos con datos
        self._set_fields()
    
    def _set_fields(self):
        for i, (texto, hint) in enumerate(self.campos):
            if i == 0:
                self.input_0.text = texto
                self.input_0.hint_text = hint
                self.input_0.bind(text=self._verificar_campos_vacios)
            elif i == 1:
                self.input_1.text = texto
                self.input_1.hint_text = hint
                self.input_1.bind(text=self._verificar_campos_vacios)
            elif i == 2:
                self.input_2.text = texto
                self.input_2.hint_text = hint
                self.input_2.bind(text=self._verificar_campos_vacios)
            elif i == 3 and self.tipo_item == "recomendacion":
                self.input_3.text = texto
                self.input_3.hint_text = hint
                self.input_3.bind(text=self._verificar_campos_vacios)
    
    def eliminar(self, *args):
        """Elimina la fila con confirmación"""
        from kivymd.uix.dialog import MDDialog
        from kivymd.uix.button import MDRaisedButton
        
        def confirmar_eliminar(instance):
            if self.eliminar_callback:
                self.eliminar_callback(self)
            if self.id_item:
                if self.tipo_item == "experiencia":
                    eliminar_experiencia(self.id_item)
                elif self.tipo_item == "recomendacion":
                    eliminar_recomendacion(self.id_item)
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
    
    def _verificar_campos_vacios(self, *args):
        """Verifica si todos los campos visibles están vacíos y elimina automáticamente"""
        datos = self.get_data()
        if all(not dato.strip() for dato in datos):
            if self.id_item:
                if self.tipo_item == "experiencia":
                    eliminar_experiencia(self.id_item)
                elif self.tipo_item == "recomendacion":
                    eliminar_recomendacion(self.id_item)
            if self.eliminar_callback:
                self.eliminar_callback(self)

    def get_data(self):
        data = []
        if hasattr(self, 'input_0'):
            data.append(self.input_0.text.strip())
        if hasattr(self, 'input_1'):
            data.append(self.input_1.text.strip())
        if hasattr(self, 'input_2'):
            data.append(self.input_2.text.strip())
        if hasattr(self, 'input_3') and self.tipo_item == "recomendacion" and self.input_3.opacity > 0:
            data.append(self.input_3.text.strip())
        return data

class ListaEditable(MDBoxLayout):
    def __init__(self, titulo="", campos=None, tipo="", **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(8)
        self.size_hint_y = None
        self.titulo = titulo
        if tipo == "experiencia":
            self.campos = [("", "Empresa"), ("", "Cargo"), ("", "Duración")]
        elif tipo == "recomendacion":
            self.campos = [("", "Nombre"), ("", "Cargo"), ("", "Comentario"), ("", "Contacto")]
        else:
            self.campos = campos or []
        self.tipo = tipo
        self.seleccionado = None
        self.dialog_agregar = None
        self.bind(minimum_height=self.setter('height'))

    def cargar_desde_bd(self, usuario_id):
        items_layout = self.ids.items_layout
        items_layout.clear_widgets()
        
        if self.tipo == "experiencia":
            datos = obtener_experiencia(usuario_id)
            for item in datos:
                fila = FilaEditable(
                    campos=[(item[1], "Empresa"), (item[2], "Cargo"), (item[3], "Duración")],
                    id_item=item[0],
                    eliminar_callback=items_layout.remove_widget,
                    seleccionar_callback=self.seleccionar,
                    tipo_item="experiencia"
                )
                items_layout.add_widget(fila)
        elif self.tipo == "recomendacion":
            datos = obtener_recomendaciones(usuario_id)
            for item in datos:
                fila = FilaEditable(
                    campos=[(item[1], "Nombre"), (item[2], "Cargo"), (item[3], "Comentario"), (item[4] or "", "Contacto")],
                    id_item=item[0],
                    eliminar_callback=items_layout.remove_widget,
                    seleccionar_callback=self.seleccionar,
                    tipo_item="recomendacion"
                )
                items_layout.add_widget(fila)

    def agregar(self, *args):
        """Muestra modal para agregar experiencia o recomendación"""
        # Crear contenedor con tamaño fijo y mejor organización
        contenido = MDBoxLayout(
            orientation='vertical', 
            spacing=dp(15), 
            padding=[dp(25), dp(30), dp(25), dp(20)],
            size_hint_y=None,
            height=dp(450) if self.tipo == "experiencia" else dp(550)
        )
        
        if self.tipo == "experiencia":
            # Primera fila: Empresa y Cargo
            fila1 = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(48))
            campo_empresa = MDTextField(hint_text="Empresa", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
            campo_cargo = MDTextField(hint_text="Cargo", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
            fila1.add_widget(campo_empresa)
            fila1.add_widget(campo_cargo)
            
            # Segunda fila: Duración
            campo_duracion = MDTextField(hint_text="Duración", mode='rectangle', font_size=dp(14), size_hint_y=None, height=dp(48))
            
            contenido.add_widget(fila1)
            contenido.add_widget(campo_duracion)
            
            self.dialog_agregar = MDDialog(
                title="Agregar Experiencia Laboral",
                type="custom",
                content_cls=contenido,
                buttons=[
                    MDRaisedButton(
                        text="Cancelar",
                        on_press=lambda x, d=self.dialog_agregar: d.dismiss()
                    ),
                    MDRaisedButton(
                        text="Confirmar",
                        on_press=lambda x: self._confirmar_experiencia(campo_empresa, campo_cargo, campo_duracion)
                    )
                ],
                size_hint=(0.95, None),
                height=dp(600)
            )
        else:
            # Primera fila: Nombre y Cargo
            fila1 = MDBoxLayout(orientation='horizontal', spacing=dp(10), size_hint_y=None, height=dp(48))
            campo_nombre = MDTextField(hint_text="Nombre", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
            campo_cargo = MDTextField(hint_text="Cargo", mode='rectangle', font_size=dp(14), size_hint_x=0.5)
            fila1.add_widget(campo_nombre)
            fila1.add_widget(campo_cargo)
            
            # Segunda fila: Comentario (multilínea)
            campo_comentario = MDTextField(
                hint_text="Comentario", 
                mode='rectangle', 
                multiline=True, 
                font_size=dp(14), 
                size_hint_y=None, 
                height=dp(120)
            )
            
            # Tercera fila: Contacto
            campo_contacto = MDTextField(hint_text="Contacto", mode='rectangle', font_size=dp(14), size_hint_y=None, height=dp(48))
            
            contenido.add_widget(fila1)
            contenido.add_widget(campo_comentario)
            contenido.add_widget(campo_contacto)
            
            self.dialog_agregar = MDDialog(
                title="Agregar Recomendación",
                type="custom",
                content_cls=contenido,
                buttons=[
                    MDRaisedButton(
                        text="Cancelar",
                        on_press=lambda x, d=self.dialog_agregar: d.dismiss()
                    ),
                    MDRaisedButton(
                        text="Confirmar",
                        on_press=lambda x: self._confirmar_recomendacion(campo_nombre, campo_cargo, campo_comentario, campo_contacto)
                    )
                ],
                size_hint=(0.95, None),
                height=dp(700)
            )
        
        self.dialog_agregar.open()
    
    def _confirmar_experiencia(self, campo_empresa, campo_cargo, campo_duracion):
        """Confirma y agrega la experiencia"""
        if self.dialog_agregar:
            self.dialog_agregar.dismiss()
            self.dialog_agregar = None
        
        empresa = campo_empresa.text.strip()
        cargo = campo_cargo.text.strip()
        duracion = campo_duracion.text.strip()
        
        if empresa and cargo and duracion:
            usuario_id = session.user_id
            nuevo_id = agregar_experiencia(usuario_id, empresa, cargo, duracion)
            if nuevo_id:
                items_layout = self.ids.items_layout
                fila = FilaEditable(
                    campos=[(empresa, "Empresa"), (cargo, "Cargo"), (duracion, "Duración")],
                    id_item=nuevo_id,
                    eliminar_callback=items_layout.remove_widget,
                    seleccionar_callback=self.seleccionar,
                    tipo_item="experiencia"
                )
                items_layout.add_widget(fila)
    
    def _confirmar_recomendacion(self, campo_nombre, campo_cargo, campo_comentario, campo_contacto):
        """Confirma y agrega la recomendación"""
        if self.dialog_agregar:
            self.dialog_agregar.dismiss()
            self.dialog_agregar = None
        
        nombre = campo_nombre.text.strip()
        cargo = campo_cargo.text.strip()
        comentario = campo_comentario.text.strip()
        contacto = campo_contacto.text.strip()
        
        if nombre and cargo and comentario and contacto:
            usuario_id = session.user_id
            nuevo_id = agregar_recomendacion(usuario_id, nombre, cargo, comentario, contacto)
            if nuevo_id:
                items_layout = self.ids.items_layout
                fila = FilaEditable(
                    campos=[(nombre, "Nombre"), (cargo, "Cargo"), (comentario, "Comentario"), (contacto, "Contacto")],
                    id_item=nuevo_id,
                    eliminar_callback=items_layout.remove_widget,
                    seleccionar_callback=self.seleccionar,
                    tipo_item="recomendacion"
                )
                items_layout.add_widget(fila)
    

    def seleccionar(self, fila, *args):
        self.seleccionado = fila

    def guardar(self, *args):
        usuario_id = session.user_id
        
        if self.seleccionado:
            datos = self.seleccionado.get_data()
            if self.seleccionado.id_item:
                if self.tipo == "experiencia":
                    editar_experiencia(self.seleccionado.id_item,
                                       empresa=datos[0], cargo=datos[1], duracion=datos[2])
                elif self.tipo == "recomendacion":
                    editar_recomendacion(self.seleccionado.id_item,
                                         nombre=datos[0], cargo=datos[1], comentario=datos[2], contacto=datos[3] if len(datos) > 3 else "")
            elif any(datos):
                if self.tipo == "experiencia":
                    nuevo_id = agregar_experiencia(usuario_id, *datos)
                elif self.tipo == "recomendacion":
                    datos_completos = datos + [""] * (4 - len(datos))
                    nuevo_id = agregar_recomendacion(usuario_id, datos_completos[0], datos_completos[1], datos_completos[2], datos_completos[3] if len(datos_completos) > 3 else None)
                self.seleccionado.id_item = nuevo_id
            self.seleccionado = None

class ExperienciaScreen(MDScreen):
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
            'experiencia': [],
            'recomendacion': []
        }
        
        lista_experiencia = self.ids.lista_experiencia
        items_layout = lista_experiencia.ids.items_layout
        for fila in items_layout.children:
            datos = fila.get_data()
            self.datos_originales['experiencia'].append({
                'id': fila.id_item,
                'datos': datos
            })
        
        lista_recomendacion = self.ids.lista_recomendacion
        items_layout = lista_recomendacion.ids.items_layout
        for fila in items_layout.children:
            datos = fila.get_data()
            self.datos_originales['recomendacion'].append({
                'id': fila.id_item,
                'datos': datos
            })
    
    def hay_cambios(self):
        """Verifica si hay cambios pendientes"""
        lista_experiencia = self.ids.lista_experiencia
        items_layout = lista_experiencia.ids.items_layout
        experiencia_actual = []
        for fila in items_layout.children:
            datos = fila.get_data()
            experiencia_actual.append({
                'id': fila.id_item,
                'datos': datos
            })
        
        if experiencia_actual != self.datos_originales.get('experiencia', []):
            return True
        
        lista_recomendacion = self.ids.lista_recomendacion
        items_layout = lista_recomendacion.ids.items_layout
        recomendacion_actual = []
        for fila in items_layout.children:
            datos = fila.get_data()
            recomendacion_actual.append({
                'id': fila.id_item,
                'datos': datos
            })
        
        if recomendacion_actual != self.datos_originales.get('recomendacion', []):
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
        lista_experiencia = self.ids.lista_experiencia
        lista_recomendacion = self.ids.lista_recomendacion
        
        lista_experiencia.cargar_desde_bd(usuario_id)
        lista_recomendacion.cargar_desde_bd(usuario_id)
        
        self.guardar_estado_original()
