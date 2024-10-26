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
from kivy.uix.scrollview import ScrollView
from kivy.animation import Animation

# Definindo o tamanho da janela
Window.size = (400, 600)
Window.minimum_width = 200
Window.maximum_width = 800

# Define a interface em KV
KV = '''
MDNavigationLayout:

    MDScreenManager:
        MainScreen:

    MDNavigationDrawer:
        id: nav_drawer
        radius: 0, dp(16), dp(16), 0
        anchor: 'left'

        MDNavigationDrawerMenu:

            MDNavigationDrawerHeader:
                title: "Meu Menu"

            MDNavigationDrawerItem:
                icon: "inbox"
                text: "Inbox"
                on_release: app.change_screen('screen1')

            MDNavigationDrawerItem:
                icon: "send"
                text: "Sent"
                on_release: app.change_screen('screen2')

            MDNavigationDrawerItem:
                icon: "star"
                text: "Favorites"
                on_release: app.change_screen('screen3')


<MainScreen>:
    container: container

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            title: "Minha Aplicação"
            left_action_items: [["menu", lambda x: app.root.ids.nav_drawer.set_state("toggle")]]
            elevation: 1

        MDScreenManager:
            id: screen_manager

            MDScreen:
                name: 'screen1'

                ScrollView:  # Adicionado para permitir rolagem
                    GridLayout:
                        id: container
                        cols: 1  # Valor inicial; será atualizado dinamicamente
                        row_default_height: dp(100)
                        row_force_default: True
                        spacing: dp(10)
                        padding: [dp(16), dp(16), dp(16), dp(16)]
                        size_hint_y: None
                        height: self.minimum_height
                        pos_hint: {"center_x": 0.5}

                        canvas.before:
                            Color:
                                rgba:236,236,236
                            RoundedRectangle:
                                pos: self.pos
                                size: self.size
                                radius: [20,]  # Raio para bordas arredondadas

            MDScreen:
                name: 'screen2'
                MDLabel:
                    text: 'Conteúdo da Tela 2'
                    halign: 'center'

            MDScreen:
                name: 'screen3'
                MDLabel:
                    text: 'Conteúdo da Tela 3'
                    halign: 'center'
'''

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

    def on_kv_post(self, base_widget):
        self.create_image_buttons()
        Window.bind(on_resize=self.update_grid_columns)
        self.update_grid_columns()

    def update_grid_columns(self, *args):
        button_width = 80 + 10
        self.container.cols = max(1, int(Window.width / button_width))

    def create_image_buttons(self):
        image_path = "src/chave_open.png"
        self.container.clear_widgets()
        nomes = [ "sala 01",
            "sala 02",
            "sala 03",
            "sala 04",
            "lab frc",
            "Senai lab",
            "sala 06",
            "sala 07",
            "sala 08",
            "sala 09",
             "Lab 01",
             "Lab 02",
             "Lab 03",
             "Lab 04",
             "Lab 05"
             "Lab 18",
             "sala 10",
             "sala 11",
             "sala 12",
             "sala 13",
             "sala 26",
             "Lab 30",
              "sala 14",
              "sala 15",
              "sala 16",
              "Lab 19",
                  "sala 01",
                  "sala 02",
                  "sala 03",
                  "sala 04",
                  "lab frc",
                  "Senai lab",
                  "sala 06",
                  "sala 07",
                  "sala 08",
                  "sala 09",
                  "Lab 01",
                  "Lab 02",
                  "Lab 03",
                  "Lab 04",
                  "Lab 05",
                  "Lab 18",
                  "sala 10",
                  "sala 11",
                  "sala 12",
                  "sala 13",
                  "sala 26",
                  "Lab 30",
                  "sala 14",
                  "sala 15",
                  "sala 16",
                  "Lab 19",
             ]
        num_buttons = 50  # Altere conforme necessário
        #names = [nomes[] + str(i+1) for i in range(num_buttons)]  # Lista de nomes

        for i in range(num_buttons):
            button_id = f"button_{i}"

            # Cria um layout para o botão e as labels
            button_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(100), spacing=dp(5))

            # Cria uma label para o número acima do botão
            number_label = Label(
                text=str(i + 1),  # Número do botão
                size_hint_y=None,
                height=dp(15),
                halign='center',
                color=(0, 0, 0, 1)  # Cor da fonte
            )
            button_layout.add_widget(number_label)

            # Cria o botão rotacionável
            button = RotatableButton(
                id=button_id,
                size_hint=(None, None),
                size=(80, 80)
            )
            button.bind(on_release=button.toggle_rotation)
            button.add_widget(Image(source=image_path, size=(80, 80)))

            # Adiciona o botão ao layout
            button_layout.add_widget(button)

            # Cria uma label para o nome abaixo do botão
            name_label = Label(
                text=nomes[i],  # Nome correspondente ao botão
                size_hint_y=None,
                height=dp(15),
                halign='center',
                color=(0, 0, 0, 1)  # Cor da fonte
            )
            button_layout.add_widget(name_label)

            # Adiciona o layout do botão ao container
            self.container.add_widget(button_layout)

class MyApp(MDApp):

    def build(self):

        return Builder.load_string(KV)

    def change_screen(self, screen_name):
        main_screen = self.root.ids.get('screen_manager') or self.root.children[0]
        if main_screen:
            main_screen.current = screen_name
        self.root.ids.nav_drawer.set_state("close")

#MyApp().run()
