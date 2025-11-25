from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout

from gestor import crear_tabla, agregar_tarea, listar_tareas, completar_tarea

class ToDoApp(App):
    def build(self):
        crear_tabla()

        # Layout principal
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Caja de entrada + botón
        input_layout = BoxLayout(size_hint_y=None, height=40)
        self.task_input = TextInput(hint_text="Escribe una tarea", multiline=False)
        add_button = Button(text="Agregar")
        add_button.bind(on_release=self.add_task)

        input_layout.add_widget(self.task_input)
        input_layout.add_widget(add_button)
        self.layout.add_widget(input_layout)

        # Lista de tareas con scroll
        self.task_container = GridLayout(cols=1, spacing=5, size_hint_y=None)
        self.task_container.bind(minimum_height=self.task_container.setter('height'))

        scroll = ScrollView()
        scroll.add_widget(self.task_container)
        self.layout.add_widget(scroll)

        self.refresh_tasks()
        return self.layout

    def add_task(self, instance):
        text = self.task_input.text.strip()
        if text:
            agregar_tarea(text)
            self.task_input.text = ""
            self.refresh_tasks()

    def complete_task(self, id_tarea):
        completar_tarea(id_tarea)
        self.refresh_tasks()

    def refresh_tasks(self):
        self.task_container.clear_widgets()
        tareas = listar_tareas()
        for tarea in tareas:
            # Botón que muestra la tarea y la completa al tocar
            estado = tarea['estado']
            texto = f"{tarea['titulo']} - {estado}"
            btn = Button(text=texto, size_hint_y=None, height=40)

            if estado == "pendiente":
                btn.background_color = (1, 0.7, 0.7, 1)  # rojo claro
                btn.bind(on_release=lambda _, tid=tarea['id']: self.complete_task(tid))
            else:
                btn.background_color = (0.7, 1, 0.7, 1)  # verde claro
                btn.disabled = True

            self.task_container.add_widget(btn)

if __name__ == "__main__":
    ToDoApp().run()
