from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.core.window import Window




class Appprueba(App):
    def build(self):
        
        nombre = Nombre()
        apelli = apellido()
        sobremi = sobre_mi()
        datcontactos = datos_contacto()
        redsocial = Redes_sociales()
        contenedorprincipal = BoxLayout(orientation='horizontal', spacing=10, padding=10)


        # barra lateral
        barralateral = BoxLayout(orientation='vertical', size_hint_x=None, width=200, spacing=10)
        barralateral.add_widget(Label(text="Usuario", size_hint_y=None, height=50))
        barralateral.add_widget(Image(source='kivy_venv/Scripts/PROYECTO/img/tl.png', size_hint_y=None, height=150))
        barralateral.add_widget(Label(text="Nombre", size_hint_y=None, height=30))
        barralateral.add_widget(nombre)
        barralateral.add_widget(Label(text="Apellido", size_hint_y=None, height=30))
        barralateral.add_widget(apelli)

        # contenido principal
        contenidoprincipal = BoxLayout(orientation='vertical', spacing=10)
        contenidoprincipal.add_widget(Label(text='Sobre mí'))
        contenidoprincipal.add_widget(sobremi)
        contenidoprincipal.add_widget(Label(text='Datos de contacto'))
        contenidoprincipal.add_widget(datcontactos)
        contenidoprincipal.add_widget(Label(text='Redes sociales'))
        contenidoprincipal.add_widget(redsocial)
        contenidoprincipal.add_widget(contenedor_botones(nombre, apelli, sobremi, redsocial, datcontactos))

        contenedorprincipal.add_widget(barralateral)
        contenedorprincipal.add_widget(contenidoprincipal)

        return contenedorprincipal

#sobre mi
class sobre_mi(BoxLayout):
    def __init__(self, **kwargs):
        super(sobre_mi, self).__init__(**kwargs)
        self.txisobre_mi = TextInput(multiline=True, size_hint_y=None, height=100)
        self.add_widget(self.txisobre_mi)

#grilla datos de contacto
class datos_contacto(GridLayout):
    def __init__(self, **kwargs):
        super(datos_contacto, self).__init__(**kwargs)
        self.cols = 4 #columnas
        self.rows = 4 #filas
        self.txiemail = TextInput()
        self.txitelefono = TextInput()
        self.add_widget(Label(text='Email:'))
        self.add_widget(self.txiemail)
        self.add_widget(Label(text='Telefono:'))
        self.add_widget(self.txitelefono)

#grilla redes sociales
class Redes_sociales(GridLayout):
    def __init__(self, **kwargs):
        super(Redes_sociales, self).__init__(**kwargs)
        self.cols = 4 #columnas
        self.rows = 4 #filas
        self.txilinkedin = TextInput()
        self.txigithub = TextInput()
        self.add_widget(Label(text='Linkedin:'))
        self.add_widget(self.txilinkedin)
        self.add_widget(Label(text='Github:'))
        self.add_widget(self.txigithub)

    
#contenedor nombre        
class Nombre(BoxLayout):
    def __init__(self, **kwargs):
        super(Nombre, self).__init__(**kwargs)
        self.txinombre = TextInput()
        self.add_widget(self.txinombre)
    
#contenedor apellido       
class apellido(BoxLayout):
    def __init__(self, **kwargs):
        super(apellido, self).__init__(**kwargs)
        self.txiapellido = TextInput()
        self.add_widget(self.txiapellido)
        
#contenedor imagen        
class imgperfil(BoxLayout):
    def __init__(self, **kwargs):
        super(imgperfil, self).__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint = (None, None)  # tamaño fijo
        self.width = 150
        self.height = 150
        self.img = Image(source='kivy_venv/Scripts/PROYECTO/img/tl.png')
        self.add_widget(self.img)
#boton editar
class boton_editar_perfil(Button):
        def __init__(self, nombre, apelli, sobremi, redsocial, datcontactos, **kwargs):
            super(boton_editar_perfil, self).__init__(**kwargs)
            self.text = "Editar"
            self.bind(on_press=self.activar_edicion)
            self.redsocial = redsocial
            self.datcontactos = datcontactos
            self.nombre = nombre
            self.apelli = apelli
            self.sobremi = sobremi
        def activar_edicion(self, instance):
            self.redsocial.txilinkedin.disabled = False
            self.redsocial.txigithub.disabled = False
            self.datcontactos.txiemail.disabled = False
            self.datcontactos.txitelefono.disabled = False
            self.nombre.txinombre.disabled = False
            self.apelli.txiapellido.disabled = False
            self.sobremi.txisobre_mi.disabled = False


#boton guardar
class boton_guardar(Button):
    def __init__(self, nombre, apelli, sobremi, redsocial, datcontactos, **kwargs):
        super(boton_guardar, self).__init__(**kwargs)
        self.text = "Guardar"
        self.bind(on_press=self.guardar_cambios)
        self.redsocial = redsocial
        self.datcontactos = datcontactos
        self.nombre = nombre
        self.apelli = apelli
        self.sobremi = sobremi

    def guardar_cambios(self, instance):
        self.redsocial.txilinkedin.disabled = True
        self.redsocial.txigithub.disabled = True
        self.datcontactos.txiemail.disabled = True
        self.datcontactos.txitelefono.disabled = True
        self.nombre.txinombre.disabled = True
        self.apelli.txiapellido.disabled = True
        self.sobremi.txisobre_mi.disabled = True

#grilla botones
class contenedor_botones(GridLayout):
    def __init__(self, nombre, apelli, sobremi, redsocial, datcontactos, **kwargs):
        super(contenedor_botones, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(boton_editar_perfil(nombre, apelli, sobremi, redsocial, datcontactos))
        self.add_widget(boton_guardar(nombre, apelli, sobremi, redsocial, datcontactos))

    

if __name__ == '__main__':
    Appprueba().run()