from kivy.app import App
from kivy.uix.relativelayout import RelativeLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

class FormacionEducacion(RelativeLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        decoracion = Image(source='formacion_lateral.png', allow_stretch=True, keep_ratio=False, size_hint=(0.4, 1))
        self.add_widget(decoracion)

        contenido = BoxLayout(orientation='vertical', padding=20, spacing=10, size_hint=(0.6, 1), pos_hint={'x': 0.4})
        self.add_widget(contenido)

        contenido.add_widget(Label(text='Formación y Educación', font_size='18sp', color=(0, 0, 0, 1), size_hint_y=None, height=30))
        self.input = TextInput(hint_text='Agregar formación o educación', size_hint_y=None, height=40)
        contenido.add_widget(self.input)

        self.lista = []
        self.seleccionado = None
        self.items = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.items.bind(minimum_height=self.items.setter('height'))
        scroll = ScrollView()
        scroll.add_widget(self.items)
        contenido.add_widget(scroll)

        botones = BoxLayout(size_hint_y=None, height=40, spacing=10)
        self.btn_agregar = Button(text='Agregar')
        self.btn_editar = Button(text='Editar')
        self.btn_guardar = Button(text='Guardar', disabled=True)
        self.btn_eliminar = Button(text='Eliminar')
        botones.add_widget(self.btn_agregar)
        botones.add_widget(self.btn_editar)
        botones.add_widget(self.btn_guardar)
        botones.add_widget(self.btn_eliminar)
        contenido.add_widget(botones)

        self.btn_agregar.bind(on_press=self.agregar)
        self.btn_editar.bind(on_press=self.editar)
        self.btn_guardar.bind(on_press=self.guardar)
        self.btn_eliminar.bind(on_press=self.eliminar)
        self.input.bind(text=self.validar_guardado)

    def agregar(self, instance):
        texto = self.input.text.strip()
        if texto:
            lbl = Label(text=texto, size_hint_y=None, height=30)
            lbl.bind(on_touch_down=self.seleccionar)
            self.items.add_widget(lbl)
            self.lista.append(lbl)
            self.input.text = ''

    def seleccionar(self, label, touch):
        if label.collide_point(*touch.pos):
            self.seleccionado = label
            self.input.text = label.text

    def editar(self, instance):
        if self.seleccionado:
            self.input.text = self.seleccionado.text
            self.btn_guardar.disabled = False

    def guardar(self, instance):
        texto = self.input.text.strip()
        if texto and self.seleccionado:
            self.seleccionado.text = texto
            self.input.text = ''
            self.seleccionado = None
            self.btn_guardar.disabled = True

    def eliminar(self, instance):
        if self.seleccionado:
            self.items.remove_widget(self.seleccionado)
            self.lista.remove(self.seleccionado)
            self.input.text = ''
            self.seleccionado = None
            self.btn_guardar.disabled = True

    def validar_guardado(self, instance, value):
        self.btn_guardar.disabled = not bool(value.strip())

class FormacionApp(App):
    def build(self):
        return FormacionEducacion()

if __name__ == '__main__':
    FormacionApp().run()
