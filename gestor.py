import asyncio
import time
from threading import Thread

from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.button import MDFlatButton, MDRoundFlatIconButton

from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.animation import Animation

from Loading import LoadingOverlay
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



class MainScreen(MDScreen):
    container = ObjectProperty(None)
    api_client = APIClientSalas("http://127.0.0.1:8000")  # URL da API

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.salas_cache = None  # Cache para dados das salas
        self.cache_time = None  # Hora do último carregamento do cache
        self.cache_duration = 60  # Cache válido por 60 segundos
        self.is_retrying = False  # Controle para evitar tentativas simultâneas

    def on_kv_post(self, base_widget):
        print("on_kv_post chamado")  # Debug
        if not hasattr(self, "salas_cache"):
            self.salas_cache = None
            self.cache_time = None
            self.cache_duration = 60
            self.is_retrying = False
        self.initialize_container()

    def fetch_salas(self):
        """Busca os dados das salas da API, com cache."""

        try:
            self.salas_cache = self.api_client.get_salas()

            return self.salas_cache
        except Exception as e:
            print(f"Erro ao buscar salas: {e}")
            return []

    def initialize_container(self, *args):
        """Inicializa o layout e configurações do container."""
        self.container = self.ids.container
        self.update_grid_columns()
        self.reload_salas()

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

    def reload_salas(self):
        """Inicia o processo de recarregar as salas com overlay de carregamento."""
        self.loading_overlay = LoadingOverlay()
        self.loading_overlay.open()
        Thread(target=self._reload_salas).start()

    def _reload_salas(self):
        """Carrega as salas em um thread separado e atualiza a interface."""
        try:
            salas = self.fetch_salas()
            # Atualiza os botões na interface principal
            Clock.schedule_once(lambda dt: self.populate_container(salas))
        except Exception as e:
            print(f"Erro ao carregar salas: {e}")
            # Exibe o botão de recarregar em caso de erro
            Clock.schedule_once(lambda dt: self.show_reload_button())
        finally:
            # Dismiss o overlay após a operação
            Clock.schedule_once(lambda dt: self.loading_overlay.dismiss())

    def populate_container(self, salas):
        """Popula o container com os botões das salas."""
        if not salas:
            self.show_reload_button()  # Exibe botão de recarregar se salas estiver vazio ou None
            return

        self.container.clear_widgets()
        for sala in salas:
            button_layout = self.create_button_layout(sala)
            self.container.add_widget(button_layout)

    def show_reload_button(self):
        """Exibe um botão para recarregar as salas."""
        self.container.clear_widgets()
        reload_button = MDRoundFlatIconButton(
            text="Indisponível, Recarregar Novamente!",
            size_hint=(1, None),
            height=dp(50),
            pos_hint={"center_x": 0.8, "center_y": 0.5},
            icon="refresh"
        )
        reload_button.bind(on_release=lambda btn: self.reload_salas())
        self.container.add_widget(reload_button)

    def create_image_buttons(self):
        """Inicia a criação dos botões com imagens das salas."""
        if not self.is_retrying:
            self.is_retrying = True
            Thread(target=self._create_image_buttons).start()

    def _create_image_buttons(self):
        """Thread para criar os botões das salas."""
        try:
            salas = self.fetch_salas()
            Clock.schedule_once(lambda dt: self.populate_container(salas))
            self.is_retrying = False
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_reload_button())
            self.is_retrying = False

    def create_button_layout(self, sala):
        """Cria o layout de um botão de sala."""
        image_path_free = "src/chave_open.png"
        image_path_occupied = "src/chave_red.png"

        button_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            height=dp(50),
            padding=[dp(15), dp(30), dp(3), dp(10)],
            spacing=dp(10)
        )

        button_image = Image(
            source=image_path_occupied if sala['is_ocupada'] else image_path_free,
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            allow_stretch=True,
            keep_ratio=True
        )

        button = MDFlatButton(
            id=str(sala['numero']),
            on_release=self.create_on_release(sala['numero'], sala['nome'], sala["is_ocupada"]),
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'center_x': 0.6, 'center_y': 0.5},
        )
        button.add_widget(button_image)

        label_layout = self.create_label_layout(sala)

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

    def create_on_release(self, button_id, name, status):
        """Cria a ação para o botão ao ser clicado."""
        return lambda btn: self.show_info_screen(button_id, name, status)

    def show_info_screen(self, index, name, status):
        """Exibe a tela de informações de uma sala."""
        app = MDApp.get_running_app()
        app.show_info_screen(index, name, status)

