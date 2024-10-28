from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.button import MDIconButton
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation
from kivy.uix.gridlayout import GridLayout

kv = """
<MainScreen>:
    container: container

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Minha Aplicação"
            left_action_items: [["menu", lambda x: nav_drawer.set_state("toggle")]]
            elevation: 1

        MDNavigationLayout:
            ScreenManager:
                MDScreen:
                    name: 'screen1'
                    ScrollView:
                        GridLayout:
                            id: container
                            cols: 1
                            row_default_height: dp(100)
                            row_force_default: True
                            spacing: dp(10)
                            padding: dp(20)
                            size_hint_y: None
                            height: self.minimum_height
                            pos_hint: {"center_x": 0.5}

            MDNavigationDrawer:
                id: nav_drawer
                BoxLayout:
                    orientation: 'vertical'
                    padding: dp(10)
                    spacing: dp(10)

                    MDLabel:
                        text: "Menu"
                        font_style: "H5"
                        halign: 'center'

                    MDList:
                        OneLineListItem:
                            text: "Opção 1"
                            on_release: nav_drawer.set_state("close")
                        OneLineListItem:
                            text: "Opção 2"
                            on_release: nav_drawer.set_state("close")
                        OneLineListItem:
                            text: "Opção 3"
                            on_release: nav_drawer.set_state("close")
"""

Builder.load_string(kv)

class RotatableButton(MDIconButton):
    rotating = False
    angle = 0

    def toggle_rotation(self, *args):
        if self.rotating:
            self.stop_rotation()
        else:
            self.start_rotation()

    def start_rotation(self):
        self.rotating = True
        self.rotation_animation = Animation(angle=360, duration=1)
        self.rotation_animation += Animation(angle=0, duration=0)
        self.rotation_animation.repeat = True
        self.rotation_animation.start(self)

    def stop_rotation(self):
        self.rotating = False
        if hasattr(self, 'rotation_animation'):
            self.rotation_animation.cancel(self)
        self.angle = 0

class MainScreen(MDScreen):
    container = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.initialize_container)

    def initialize_container(self, *args):
        self.container = self.ids.container
        self.create_image_buttons()
        Window.bind(on_resize=self.update_grid_columns)
        self.update_grid_columns()

    def update_grid_columns(self, *args):
        button_width = dp(100)
        spacing = dp(10)
        padding = dp(20)
        if self.container:
            total_space_per_button = button_width + spacing
            num_columns = max(1, int((Window.width - 2 * padding) / total_space_per_button))
            self.container.cols = num_columns
            self.container.spacing = [spacing, spacing]
            self.container.padding = [padding, padding]

    def create_image_buttons(self):
        image_path = "src/chave_open.png"
        nomes = [
            "sala 01", "sala 02", "sala 03", "sala 04", "lab frc", "Senai lab",
            "sala 06", "sala 07", "sala 08", "sala 09", "Lab 01", "Lab 02",
            "Lab 03", "Lab 04", "Lab 05", "Lab 18", "sala 10", "sala 11",
            "sala 12", "sala 13", "sala 26", "Lab 30", "sala 14", "sala 15",
            "sala 16", "Lab 19", "sala 01", "sala 02", "sala 03", "sala 04",
            "lab frc", "Senai lab", "sala 06", "sala 07", "sala 08", "sala 09",
            "Lab 01", "Lab 02", "Lab 03", "Lab 04", "Lab 05", "Lab 18", "sala 10",
            "sala 11", "sala 12", "sala 13", "sala 26", "Lab 30", "sala 14",
            "sala 15", "sala 16", "Lab 19"
        ]
        num_buttons = 50
        #nomes = ["sala 01", "sala 02", "sala 03", "sala 04", "lab frc", "Senai lab"]
        for i in range(num_buttons):
            button_id = f"button_{i}"
            button_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), spacing=dp(5),
                                      padding=[dp(50), dp(10), dp(10), dp(10)])

            number_label = Label(
                text=str(i + 1),
                size_hint=(1, None),
                height=dp(15),
                halign='center',
                color=(0, 0, 0, 1)
            )
            number_label.bind(size=number_label.setter('text_size'))
            button_layout.add_widget(number_label)

            button = RotatableButton(id=button_id, size_hint=(None, None), size=(dp(80), dp(80)))
            button.bind(on_release=lambda btn, index=i, name=nomes[i]: self.show_info_screen(index, name))
            button_image = Image(source=image_path, size=(dp(80), dp(80)))
            button.add_widget(button_image)
            button_layout.add_widget(button)

            name_label = Label(
                text=nomes[i],
                size_hint=(1, None),
                height=dp(15),
                halign='center',
                color=(0, 0, 0, 1)
            )
            name_label.bind(size=name_label.setter('text_size'))
            button_layout.add_widget(name_label)
            self.container.add_widget(button_layout)

    def show_info_screen(self, index, name):
        app = MDApp.get_running_app()
        app.show_info_screen(index, name)

