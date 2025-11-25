# perfil_screen.py
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.card import MDCard
from kivy.metrics import dp
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
import os

from session import session
from database import (
    obtener_perfil,
    obtener_contactos,
    obtener_redes,
    actualizar_perfil,
    agregar_contacto,
    editar_contacto,
    agregar_red,
    editar_red,
)
import sqlite3

class FilaDinamica(MDBoxLayout):
    def __init__(self, campo1="", campo2="", id_item=None, disabled=False, eliminar_callback=None, tipo_item=None, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(42)
        self.spacing = dp(8)
        self.padding = [0, dp(2)]
        
        self.campo1 = campo1
        self.campo2 = campo2
        self.id_item = id_item
        self.disabled = disabled
        self.eliminar_callback = eliminar_callback
        self.tipo_item = tipo_item  # 'contacto' o 'red'
        
        # Crear campos manualmente para evitar conflictos con Builder
        self.campo1_input = MDTextField(
            text=campo1,
            disabled=disabled,
            mode='rectangle',
            size_hint_x=0.45,
            font_size=dp(13)
        )
        self.campo2_input = MDTextField(
            text=campo2,
            disabled=disabled,
            mode='rectangle',
            size_hint_x=0.55,
            font_size=dp(13)
        )
        
        # Agregar listeners para detectar campos vacíos
        self.campo1_input.bind(text=self._verificar_campos_vacios)
        self.campo2_input.bind(text=self._verificar_campos_vacios)
        
        # Agregar listener para actualizar botón guardar en la pantalla padre
        self.campo1_input.bind(text=self._notificar_cambio)
        self.campo2_input.bind(text=self._notificar_cambio)
        
        self.add_widget(self.campo1_input)
        self.add_widget(self.campo2_input)
    
    def _notificar_cambio(self, *args):
        """Notifica cambios a la pantalla padre para actualizar botón guardar"""
        if hasattr(self, 'parent') and hasattr(self.parent, 'parent'):
            screen = None
            current = self.parent
            while current:
                if hasattr(current, '_actualizar_boton_guardar'):
                    screen = current
                    break
                current = current.parent
            if screen:
                screen._actualizar_boton_guardar()
    
    def _verificar_campos_vacios(self, *args):
        """Verifica si todos los campos están vacíos y elimina automáticamente"""
        campo1_text = self.campo1_input.text.strip()
        campo2_text = self.campo2_input.text.strip()
        
        if not campo1_text and not campo2_text:
            # Si tiene id_item, eliminar de la base de datos
            if self.id_item:
                try:
                    conn = sqlite3.connect("portafolio.db")
                    cursor = conn.cursor()
                    if self.tipo_item == 'contacto':
                        cursor.execute("DELETE FROM contactos WHERE id=?", (self.id_item,))
                    elif self.tipo_item == 'red':
                        cursor.execute("DELETE FROM redes_sociales WHERE id=?", (self.id_item,))
                    conn.commit()
                    conn.close()
                except Exception:
                    pass
            
            # Eliminar de la UI (tanto si tiene id_item como si no)
            if self.eliminar_callback:
                self.eliminar_callback(self)

class PerfilScreen(MDScreen):
    def __init__(self, usuario_id=None, **kwargs):
        super().__init__(**kwargs)
        self.usuario_id = usuario_id or session.user_id
        self.datos_originales = {}
        self.cambios_pendientes = False
        self.dialog = None
        self.dialog_agregar = None

    def on_pre_enter(self, *args):
        self.usuario_id = session.user_id
        self.cargar_datos()
        self.guardar_estado_original()
        self._actualizar_boton_guardar()
    
    def _actualizar_boton_guardar(self):
        """Actualiza el estado del botón guardar"""
        btn_guardar = self.ids.btn_guardar
        hay_cambios = self.hay_cambios()
        hay_vacios = self._hay_campos_vacios()
        btn_guardar.disabled = not hay_cambios or hay_vacios


    def cargar_datos(self):
        perfil = obtener_perfil(self.usuario_id)
        contactos = obtener_contactos(self.usuario_id)
        redes = obtener_redes(self.usuario_id)

        # Perfil
        txt_nombre = self.ids.txt_nombre
        txt_apellido = self.ids.txt_apellido
        txt_descripcion = self.ids.txt_descripcion
        img_perfil = self.ids.img_perfil
        
        # Vincular cambios para actualizar botón guardar
        txt_nombre.bind(text=lambda instance, value: self._actualizar_boton_guardar())
        txt_apellido.bind(text=lambda instance, value: self._actualizar_boton_guardar())
        txt_descripcion.bind(text=lambda instance, value: self._actualizar_boton_guardar())
        
        if perfil:
            if isinstance(perfil, dict):
                txt_nombre.text = perfil.get("nombre") or ""
                txt_apellido.text = perfil.get("apellido") or ""
                txt_descripcion.text = perfil.get("descripcion") or ""
                foto_path = perfil.get("foto") or ""
                if foto_path and os.path.exists(foto_path):
                    img_perfil.source = foto_path
                else:
                    img_perfil.source = 'kivy_mov/share/proyectomv/img/usuario.png'
            else:
                try:
                    txt_nombre.text = perfil[2] or ""
                    txt_apellido.text = ""
                    txt_descripcion.text = perfil[6] or ""
                    img_perfil.source = 'kivy_mov/share/proyectomv/img/usuario.png'
                except Exception:
                    txt_nombre.text = ""
                    txt_apellido.text = ""
                    txt_descripcion.text = ""
                    img_perfil.source = 'kivy_mov/share/proyectomv/img/usuario.png'
        else:
            txt_nombre.text = ""
            txt_apellido.text = ""
            txt_descripcion.text = ""
            img_perfil.source = 'kivy_mov/share/proyectomv/img/usuario.png'

        # Contactos
        panel_contactos = self.ids.panel_contactos_container
        panel_contactos.clear_widgets()
        for item in contactos or []:
            if len(item) == 3:
                if isinstance(item[0], int):
                    idc, tipo, valor = item
                else:
                    tipo, valor, idc = item
            else:
                idc, tipo, valor = (item[0], item[1], item[2]) if len(item) >= 3 else (None, "", "")
            fila = FilaDinamica(
                campo1=tipo, 
                campo2=valor, 
                id_item=idc, 
                disabled=False,
                eliminar_callback=panel_contactos.remove_widget,
                tipo_item='contacto'
            )
            panel_contactos.add_widget(fila)

        # Redes
        panel_redes = self.ids.panel_redes_container
        panel_redes.clear_widgets()
        for item in redes or []:
            if len(item) == 3:
                if isinstance(item[0], int):
                    idr, plataforma, link = item
                else:
                    plataforma, link, idr = item
            else:
                idr, plataforma, link = (item[0], item[1], item[2]) if len(item) >= 3 else (None, "", "")
            fila = FilaDinamica(
                campo1=plataforma, 
                campo2=link, 
                id_item=idr, 
                disabled=False,
                eliminar_callback=panel_redes.remove_widget,
                tipo_item='red'
            )
            panel_redes.add_widget(fila)
    
    def guardar_estado_original(self):
        """Guarda el estado original de los datos para detectar cambios"""
        img_perfil = self.ids.img_perfil
        foto_path = img_perfil.source if hasattr(img_perfil, 'source') else None
        self.datos_originales = {
            'nombre': self.ids.txt_nombre.text,
            'apellido': self.ids.txt_apellido.text,
            'descripcion': self.ids.txt_descripcion.text,
            'foto': foto_path,
            'contactos': [],
            'redes': []
        }
        
        panel_contactos = self.ids.panel_contactos_container
        for fila in panel_contactos.children:
            if isinstance(fila, FilaDinamica):
                self.datos_originales['contactos'].append({
                    'id': fila.id_item,
                    'campo1': fila.campo1_input.text,
                    'campo2': fila.campo2_input.text
                })
        
        panel_redes = self.ids.panel_redes_container
        for fila in panel_redes.children:
            if isinstance(fila, FilaDinamica):
                self.datos_originales['redes'].append({
                    'id': fila.id_item,
                    'campo1': fila.campo1_input.text,
                    'campo2': fila.campo2_input.text
                })
        
        self.cambios_pendientes = False
    
    def hay_cambios(self):
        """Verifica si hay cambios pendientes"""
        img_perfil = self.ids.img_perfil
        foto_actual = img_perfil.source if hasattr(img_perfil, 'source') else None
        foto_original = self.datos_originales.get('foto')
        
        if (self.ids.txt_nombre.text != self.datos_originales.get('nombre', '') or
            self.ids.txt_apellido.text != self.datos_originales.get('apellido', '') or
            self.ids.txt_descripcion.text != self.datos_originales.get('descripcion', '') or
            foto_actual != foto_original):
            return True
        
        panel_contactos = self.ids.panel_contactos_container
        contactos_actuales = []
        for fila in panel_contactos.children:
            if isinstance(fila, FilaDinamica):
                contactos_actuales.append({
                    'id': fila.id_item,
                    'campo1': fila.campo1_input.text,
                    'campo2': fila.campo2_input.text
                })
        
        if contactos_actuales != self.datos_originales.get('contactos', []):
            return True
        
        panel_redes = self.ids.panel_redes_container
        redes_actuales = []
        for fila in panel_redes.children:
            if isinstance(fila, FilaDinamica):
                redes_actuales.append({
                    'id': fila.id_item,
                    'campo1': fila.campo1_input.text,
                    'campo2': fila.campo2_input.text
                })
        
            if redes_actuales != self.datos_originales.get('redes', []):
                return True
            
            return False
    
    def seleccionar_imagen(self, *args):
        """Abre un diálogo para seleccionar imagen"""
        from kivy.uix.filechooser import FileChooserListView
        from kivymd.uix.button import MDFlatButton
        
        contenido = MDBoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10),
            size_hint_y=None,
            height=dp(400)
        )
        
        filechooser = FileChooserListView(
            path=os.path.expanduser('~'),
            filters=['*.png', '*.jpg', '*.jpeg']
        )
        contenido.add_widget(filechooser)
        
        def seleccionar(instance):
            if filechooser.selection:
                self.foto_path = filechooser.selection[0]
                img_perfil = self.ids.img_perfil
                if os.path.exists(self.foto_path):
                    img_perfil.source = self.foto_path
            if self.dialog_agregar:
                self.dialog_agregar.dismiss()
                self.dialog_agregar = None
        
        def cancelar(instance):
            if self.dialog_agregar:
                self.dialog_agregar.dismiss()
                self.dialog_agregar = None
        
        self.dialog_agregar = MDDialog(
            title="Seleccionar Imagen",
            type="custom",
            content_cls=contenido,
            buttons=[
                MDFlatButton(
                    text="Cancelar",
                    on_press=cancelar
                ),
                MDRaisedButton(
                    text="Seleccionar",
                    on_press=seleccionar
                )
            ],
            size_hint=(0.9, None),
            height=dp(500)
        )
        self.dialog_agregar.open()

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

    def guardar_cambios(self, *args):
        """Guarda los cambios con confirmación"""
        self.mostrar_dialogo_confirmacion(
            "¿Deseas guardar los cambios?",
            self._guardar_cambios_real
        )
    
    def _guardar_cambios_real(self):
        """Guarda los cambios en la base de datos"""
        txt_nombre = self.ids.txt_nombre
        txt_apellido = self.ids.txt_apellido
        txt_descripcion = self.ids.txt_descripcion
        img_perfil = self.ids.img_perfil
        
        foto_path = img_perfil.source if hasattr(img_perfil, 'source') and img_perfil.source != 'kivy_mov/share/proyectomv/img/usuario.png' else None
        
        actualizar_perfil(self.usuario_id,
                          nombre=txt_nombre.text,
                          apellido=txt_apellido.text,
                          descripcion=txt_descripcion.text,
                          foto=foto_path)

        panel_contactos = self.ids.panel_contactos_container
        panel_redes = self.ids.panel_redes_container

        for fila in list(panel_contactos.children):
            if isinstance(fila, FilaDinamica) and getattr(fila, "id_item", None):
                editar_contacto(fila.id_item, fila.campo1_input.text, fila.campo2_input.text)
        
        for fila in list(panel_redes.children):
            if isinstance(fila, FilaDinamica) and getattr(fila, "id_item", None):
                editar_red(fila.id_item, fila.campo1_input.text, fila.campo2_input.text)

        self.guardar_estado_original()
        self._actualizar_boton_guardar()
        
        # Mostrar mensaje de éxito
        self.mostrar_dialogo_confirmacion(
            "Cambios guardados exitosamente",
            self._cerrar_dialogo
        )

    def nuevo_contacto(self, *args):
        """Muestra modal para agregar nuevo contacto"""
        contenido = MDBoxLayout(orientation='vertical', spacing=dp(12), padding=dp(15), adaptive_height=True)
        
        campo_tipo = MDTextField(
            hint_text="Tipo (ej: Teléfono, Email)",
            mode='rectangle',
            font_size=dp(14)
        )
        campo_valor = MDTextField(
            hint_text="Información",
            mode='rectangle',
            font_size=dp(14)
        )
        
        contenido.add_widget(campo_tipo)
        contenido.add_widget(campo_valor)
        
        self.dialog_agregar = MDDialog(
            title="Agregar Contacto",
            type="custom",
            content_cls=contenido,
            buttons=[
                MDRaisedButton(
                    text="Cancelar",
                    on_press=lambda x, d=self.dialog_agregar: d.dismiss()
                ),
                MDRaisedButton(
                    text="Confirmar",
                    on_press=lambda x: self._confirmar_contacto(campo_tipo, campo_valor)
                )
            ]
        )
        self.dialog_agregar.open()
    
    def _confirmar_contacto(self, campo_tipo, campo_valor):
        """Confirma y agrega el contacto"""
        tipo = campo_tipo.text.strip()
        valor = campo_valor.text.strip()
        
        if self.dialog_agregar:
            self.dialog_agregar.dismiss()
        
        panel_contactos = self.ids.panel_contactos_container
        idc = agregar_contacto(self.usuario_id, tipo, valor)
        if idc:
            fila = FilaDinamica(
                campo1=tipo, 
                campo2=valor, 
                id_item=idc, 
                disabled=False,
                eliminar_callback=panel_contactos.remove_widget,
                tipo_item='contacto'
            )
        else:
            fila = FilaDinamica(
                campo1=tipo, 
                campo2=valor, 
                id_item=None, 
                disabled=False,
                eliminar_callback=panel_contactos.remove_widget,
                tipo_item='contacto'
            )
        panel_contactos.add_widget(fila)

    def nueva_red(self, *args):
        """Muestra modal para agregar nueva red social"""
        contenido = MDBoxLayout(orientation='vertical', spacing=dp(12), padding=dp(15), adaptive_height=True)
        
        campo_plataforma = MDTextField(
            hint_text="Plataforma (ej: LinkedIn, GitHub)",
            mode='rectangle',
            font_size=dp(14)
        )
        campo_link = MDTextField(
            hint_text="Enlace",
            mode='rectangle',
            font_size=dp(14)
        )
        
        contenido.add_widget(campo_plataforma)
        contenido.add_widget(campo_link)
        
        self.dialog_agregar = MDDialog(
            title="Agregar Red Social",
            type="custom",
            content_cls=contenido,
            buttons=[
                MDRaisedButton(
                    text="Cancelar",
                    on_press=lambda x, d=self.dialog_agregar: d.dismiss()
                ),
                MDRaisedButton(
                    text="Confirmar",
                    on_press=lambda x: self._confirmar_red(campo_plataforma, campo_link)
                )
            ]
        )
        self.dialog_agregar.open()
    
    def _confirmar_red(self, campo_plataforma, campo_link):
        """Confirma y agrega la red social"""
        plataforma = campo_plataforma.text.strip()
        link = campo_link.text.strip()
        
        if self.dialog_agregar:
            self.dialog_agregar.dismiss()
        
        panel_redes = self.ids.panel_redes_container
        idr = agregar_red(self.usuario_id, plataforma, link)
        if idr:
            fila = FilaDinamica(
                campo1=plataforma, 
                campo2=link, 
                id_item=idr, 
                disabled=False,
                eliminar_callback=panel_redes.remove_widget,
                tipo_item='red'
            )
        else:
            fila = FilaDinamica(
                campo1=plataforma, 
                campo2=link, 
                id_item=None, 
                disabled=False,
                eliminar_callback=panel_redes.remove_widget,
                tipo_item='red'
            )
        panel_redes.add_widget(fila)
    
    def _hay_campos_vacios(self):
        """Verifica si hay campos vacíos"""
        if not self.ids.txt_nombre.text.strip() or not self.ids.txt_apellido.text.strip():
            return True
        return False
    
    def ir_a_otra(self, *args):
        """Verifica cambios antes de salir"""
        if self._hay_campos_vacios():
            self.mostrar_dialogo_confirmacion(
                "Tienes campos vacíos. Si sales, se restaurarán los valores anteriores. ¿Deseas salir?",
                lambda: self._restaurar_y_salir(),
                lambda: None
            )
        elif self.hay_cambios():
            self.mostrar_dialogo_confirmacion(
                "Tienes cambios sin guardar. ¿Deseas salir sin guardar?",
                lambda: self._salir_sin_guardar(),
                lambda: None
            )
        else:
            self._salir_sin_guardar()
    
    def _restaurar_y_salir(self):
        """Restaura valores originales y sale"""
        # Restaurar valores originales
        self.ids.txt_nombre.text = self.datos_originales.get('nombre', '')
        self.ids.txt_apellido.text = self.datos_originales.get('apellido', '')
        self.ids.txt_descripcion.text = self.datos_originales.get('descripcion', '')
        
        # Restaurar imagen
        img_perfil = self.ids.img_perfil
        foto_original = self.datos_originales.get('foto')
        if foto_original and os.path.exists(foto_original):
            img_perfil.source = foto_original
        else:
            img_perfil.source = 'kivy_mov/share/proyectomv/img/usuario.png'
        
        # Restaurar contactos y redes
        panel_contactos = self.ids.panel_contactos_container
        panel_contactos.clear_widgets()
        for contacto in self.datos_originales.get('contactos', []):
            fila = FilaDinamica(
                campo1=contacto.get('campo1', ''),
                campo2=contacto.get('campo2', ''),
                id_item=contacto.get('id'),
                disabled=False,
                eliminar_callback=panel_contactos.remove_widget,
                tipo_item='contacto'
            )
            panel_contactos.add_widget(fila)
        
        panel_redes = self.ids.panel_redes_container
        panel_redes.clear_widgets()
        for red in self.datos_originales.get('redes', []):
            fila = FilaDinamica(
                campo1=red.get('campo1', ''),
                campo2=red.get('campo2', ''),
                id_item=red.get('id'),
                disabled=False,
                eliminar_callback=panel_redes.remove_widget,
                tipo_item='red'
            )
            panel_redes.add_widget(fila)
        
        if self.dialog:
            self.dialog.dismiss()
        self.manager.current = 'dashboard'
    
    def _salir_sin_guardar(self):
        """Sale de la pantalla sin guardar"""
        if self.dialog:
            self.dialog.dismiss()
        self.manager.current = 'dashboard'
