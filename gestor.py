import asyncio
from threading import Thread

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation

from api_client import APIClientSalas

kv = """
<MainScreen>:
    container: container

    MDBoxLayout:
        orientation: 'vertical'

        MDTopAppBar:
            elevation: 1
            md_bg_color: [0.5, 1, 0.5, 1]   # Exemplo de cor azul (RGBA)
            # Estrutura principal de layout horizontal para o botão, logo e título
            MDBoxLayout:
                orientation: 'horizontal'
                spacing: dp(10)  # Espaçamento entre os elementos
                padding: [dp(2), 0]  # Ajuste de padding no eixo X para centralizar

                # Botão de menu à esquerda
                MDIconButton:
                    icon: "menu"
                    on_release: nav_drawer.set_state("toggle")
                    size_hint_x: None
                    width: dp(40)

                # Logo da aplicação
                FitImage:
                    source: "logo.png"
                 
                    size_hint_x: None  # Define o valor como None para que a largura seja definida em pixels
                    size_hint_y: None  # Define o valor como None para que a altura seja definida em pixels
                    width: dp(60)  # Define uma largura fixa para a imagem
                    height: dp(60)  # Define uma altura fixa para a imagem
                    pos_hint: {"top": 1.8}  # Posiciona a imagem no topo do layout pai
                    allow_stretch: True  # Permite que a imagem se ajuste ao tamanho definido
                    keep_ratio: True  # Mantém a proporção original da imagem
                   
                # Nome da aplicação
                MDLabel:
                    text: "Painel de chaves"
                    halign: "center"
                    theme_text_color: "Primary"
                    font_style: "H6"
                    size_hint_x: 0.5
                    size_hint_y: 1
                    #width: self.texture_size[0] + dp(10)  # Ajusta largura para o tamanho do texto

        # Conteúdo do layout principal
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
                            
            # Menu de navegação
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
                        OneLineIconListItem:
                            text: "Perfil"
                            on_release:
                                nav_drawer.set_state("close")
                                app.show_user_info_screen()  # Chame a função com os dados do usuário
                            IconLeftWidget:
                                icon: "account"  # Ícone do perfil (pode usar qualquer ícone do Material Design)
                    
                        OneLineIconListItem:
                            text: "Logout"
                            on_release:
                                nav_drawer.set_state("close")
                                app.on_logout()
                            IconLeftWidget:
                                icon: "logout"  # Ícone de logout (pode usar qualquer ícone do Material Design)

"""

Builder.load_string(kv)



from Loading import LoadingOverlay

class MainScreen(MDScreen):
    container = ObjectProperty(None)
    api_client = APIClientSalas("http://127.0.0.1:8000")  # URL da API

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_once(self.initialize_container, 0.1)

    def on_kv_post(self, base_widget):
        self.initialize_container()

    def fetch_salas(self):
        """Busca os dados das salas da API."""
        return self.api_client.get_salas()

    def initialize_container(self, *args):
        """Inicializa o layout e configurações do container."""
        self.container = self.ids.container
        Thread(target=self.create_image_buttons).start()
        Window.bind(on_resize=self.update_grid_columns)
        self.update_grid_columns()

    def update_grid_columns(self, *args):
        """Atualiza o número de colunas no grid com base no tamanho da janela."""
        button_width = dp(80)
        spacing = dp(10)
        padding = dp(10)

        if self.container:
            total_space_per_button = button_width + spacing
            num_columns = max(1, int((Window.width - 2 * padding) / total_space_per_button))
            self.container.cols = num_columns
            self.container.spacing = [spacing, spacing]
            self.container.padding = [padding, padding]

    def create_image_buttons(self):
        """Cria botões com imagens representando salas."""
        try:
            salas = self.fetch_salas()
            Clock.unschedule(self.retry_fetch)
            Clock.schedule_once(lambda dt: self.populate_container(salas))

        except Exception as e:
            #print(f"Erro ao conectar com ao servidor: {e}")
            Clock.schedule_once(lambda dt: self.show_error_message(
                "Serviço indisponível no momento. Tentando novamente..."
            ))
            Clock.schedule_interval(self.retry_fetch, 10)

    def populate_container(self, salas):
        """Popula o container com os botões das salas."""
        try:
            self.container.clear_widgets()

            for sala in salas:
                button_layout = self.create_button_layout(sala)
                self.container.add_widget(button_layout)
        except:
           #self.show_error_message("Erro: 'salas' não é uma lista válida.")
           return  # Retorna sem tentar iterar
    def create_button_layout(self, sala):
        """Cria o layout de um botão de sala."""
        image_path_free = "src/chave_open.png"
        image_path_occupied = "src/chave_red.png"

        button_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(50),  # Altura ajustada para comportar a imagem maior
            padding=[dp(15), dp(30), dp(3), dp(10)],
            spacing=dp(10)  # Espaçamento entre o botão e as labels
        )

        # Define a imagem do botão com base no estado da sala
        button_image = Image(
            source=image_path_occupied if sala['is_ocupada'] else image_path_free,
            size_hint=(None, None),  # Adiciona controle de tamanho manual
            size=(dp(50), dp(50)),  # Tamanho ajustado
            allow_stretch=True,  # Permite que a imagem seja esticada para caber no tamanho
            keep_ratio=True ,

        )

        # Botão com a imagem
        button = MDFlatButton(
            id=str(sala['numero']),
            on_release=self.create_on_release(sala['numero'], sala['nome'], sala["is_ocupada"]),
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'center_x': 0.6, 'center_y': 0.5},

        )
        button.add_widget(button_image)

        # Layout para o número e nome da sala
        label_layout = self.create_label_layout(sala)

        # Adiciona ao layout do botão
        button_layout.add_widget(button)
        button_layout.add_widget(label_layout)

        return button_layout

    def create_label_layout(self, sala):
        """Cria o layout de texto para número e nome da sala."""
        label_layout = BoxLayout(
            orientation='vertical',
            size_hint=(1, None),
            height=dp(40),
            spacing=dp(3),

        )

        number_label = Label(
            text=f"[b]{sala['numero']}[/b]",
            markup=True,
            size_hint=(1, None),
            height=dp(18),
            halign='center',
            color=(0, 0, 0, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
        )
        number_label.bind(size=number_label.setter('text_size'))

        name_label = Label(
            text=sala['nome'],
            size_hint=(1, None),
            height=dp(18),
            halign='center',
            color=(0, 0, 0, 1)
        )
        name_label.bind(size=name_label.setter('text_size'))

        label_layout.add_widget(number_label)
        label_layout.add_widget(name_label)

        return label_layout

    def show_error_message(self, message):
        """Mostra uma mensagem de erro no container."""
        self.container.clear_widgets()
        error_label = Label(
            text=message,
            size_hint=(1, None),
            height=dp(100),
            color=(1, 0, 0, 1),
            halign='center'
        )
        error_label.bind(size=error_label.setter('text_size'))
        self.container.add_widget(error_label)

    def retry_fetch(self, *args):
        """Tenta buscar os dados novamente."""
        self.create_image_buttons()

    def create_on_release(self, button_id, name, status):
        """Cria a ação para o botão ao ser clicado."""

       # def show_loading_screen(self, button_id, name, status):
        # Add it to the current screen/widget
            # Optionally, do something else like starting a loading animation

        return lambda btn: self.show_info_screen(button_id, name, status)

    def show_info_screen(self, index, name, status):

        """Exibe a tela de informações de uma sala."""
        app = MDApp.get_running_app()
        app.show_info_screen(index, name, status)
