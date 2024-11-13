from datetime import datetime

from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import ObjectProperty, ListProperty, NumericProperty, Clock
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.animation import Animation
from kivy.uix.image import Image
from kivy.metrics import dp
from kivymd.app import MDApp

kv = """
<InfoScreen>:
    name: 'info_screen'
    devolver_button: devolver_button

    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.95, 0.95

        # Logo e Número da Chave
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(80)
            spacing: dp(15)

            Image:
                source: "logo.png"
                size_hint_x: None
                width: dp(60)
                allow_stretch: True
                keep_ratio: True
            MDLabel:
                text: "Esta pegando a sala: "
                font_style: "H5"
                theme_text_color: "Primary"
                halign: "center"
                valign: "middle"
            MDLabel:
                id: info_title
                text: "Número da Chave: 123"
                font_style: "H5"
                theme_text_color: "Primary"
                halign: "left"
                valign: "middle"

        # Card com informações do professor e demais elementos
        MDCard:
            orientation: 'vertical'
            padding: dp(25)
            spacing: dp(25)
            size_hint_y: 0.6
            elevation: 2
            md_bg_color: app.theme_cls.bg_light

            # Seção de Informações do Professor
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(15)

                MDLabel:
                    id: name_id
                    text: "Nome do Responsável: João da Silva"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"

                MDLabel:
                    id:funcao
                    text: "Função: Professor de Matemática"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"

                MDLabel:
                    id: email_id
                    text: "Email: joao.silva@escola.com"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"

                MDLabel:
                    id: phone_id
                    text: "Telefone: (11) 98765-4321"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"

            # Imagem Digital, Data e Hora, Botões
            MDBoxLayout:
                orientation: 'horizontal'
                spacing: dp(25)

                # Imagem Digital
                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 0.4
                    spacing: dp(10)
                    Image:
                        source: "digital_red.png"
                        size_hint_y: None
                        height: dp(120)
                        allow_stretch: True
                        keep_ratio: True
                    MDLabel:
                        id: texto_data
                        text: "Data: 28/10/2024"
                        font_style: "Caption"
                        halign: "center"
                        theme_text_color: "Secondary"
                    MDLabel:
                        id: texto_hora
                        text: "Hora: 14:30"
                        font_style: "Caption"
                        halign: "center"
                        theme_text_color: "Secondary"

                # Botões
                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 0.4
                    spacing: dp(15)
                    MDLabel:
                        id: status_label  # Label para exibir o status
                        text: "Status: Pronto para ação"
                        font_style: "Subtitle1"
                        theme_text_color: "Primary"
                        halign: "center"
                    MDRaisedButton:
                        text: "Cancelar"
                        md_bg_color: app.theme_cls.error_color
                        pos_hint: {"center_x": 0.5}
                        on_release: app.root.current = 'main'

                    MDRaisedButton:
                        id: pegar_button  # Adicionado ID para o botão "Pegar"
                        text: "Pegar"
                        md_bg_color: app.theme_cls.primary_color
                        pos_hint: {"center_x": 0.5}
                        on_release: app.on_click_register_historico(True)

                    MDRaisedButton:
                        id: devolver_button
                        text: "Devolver"
                        md_bg_color: app.theme_cls.primary_color
                        pos_hint: {"center_x": 0.5}
                        opacity: 0  # Inicialmente invisível
                        disabled: True  # Desativado até ser necessário
                        on_release: app.on_click_register_historico(False)
"""

Builder.load_string(kv)


from core.api_client import APIClientSalas
class InfoScreen(MDScreen):
    status_label = ObjectProperty(None)  # Referência para o status label
    keys = ListProperty([])  # Lista de chaves
    current_key_id = None
    agora = datetime.now()
    api =  APIClientSalas("http://localhost:8000")

    # Dividir em data e hora


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.loading_dialog = None  # Adicione isso para inicializar a variável de diálogo
        # Pegar a data e hora atuais
        agora = datetime.now()

        # Dividir em data e hora
        self.data = agora.date()
        #self.hora = agora.time()

        # Atualizar os rótulos com a data e hora
        #self.ids.texto_data.text = str(self.data)
        #self.ids.texto_hora.text = str(self.hora)

        #self.update_date_time()

        # Atualizar a data e hora a cada segundo
        Clock.schedule_interval(self.update_date_time, 1)


    def update_date_time(self, *args):
        """Atualiza a data e hora na interface."""
        agora = datetime.now()

        # Atualizar os valores de data e hora
        self.ids.texto_data.text = agora.strftime("%d/%m/%Y")  # Formatar como '28/10/2024'
        self.ids.texto_hora.text = agora.strftime("%H:%M")  # Formatar como '14:30'
    def update_title(self, name):
        self.ids.info_title.text = f"{name}"

    async def get_last_user_for_room(self, room_id):
        """Obtém o último usuário vinculado à sala a partir do histórico de acesso."""
        historico = await self.api.get_historico_user(room_id)
        if historico:
            return historico.get("usuario_id")  # Retorna o ID do último usuário que acessou a sala
        return None

    def toggle_key_status(self, status: bool, room_id: int, current_user_id: int):
        """Alterna o estado dos botões com base no status da chave e no usuário."""


        if status is False:
            # Chave disponível, botão "Pegar" fica visível e habilitado, "Devolver" invisível e desabilitado
            self.ids.devolver_button.opacity = 0
            self.ids.devolver_button.disabled = True
            self.ids.pegar_button.opacity = 1
            self.ids.pegar_button.disabled = False
        else:

            # Chave ocupada; "Devolver" só visível se o usuário atual for o último a pegar a chave
            if room_id == current_user_id:

                self.ids.devolver_button.opacity = 1
                self.ids.devolver_button.disabled = False
            else:
                self.ids.devolver_button.opacity = 0
                self.ids.devolver_button.disabled = True

            self.ids.pegar_button.opacity = 0
            self.ids.pegar_button.disabled = True

    def show_loading_dialog(self):
        # Obtendo o texto do 'info_title' diretamente
        info_text = self.ids.info_title.text
        if not self.loading_dialog:
            # Usando o texto de 'info_title' no diálogo
            self.loading_dialog = MDDialog(
                title=info_text,  # Texto obtido de 'info_title'
                type="custom",
                auto_dismiss=False,
                content_cls=self.LoadingContent(dialog_ref=self)  # Passa referência do diálogo
            )
        self.loading_dialog.open()

    class LoadingContent(MDBoxLayout):
        def __init__(self, dialog_ref, **kwargs):
            super().__init__(**kwargs)
            self.orientation = 'vertical'
            self.spacing = dp(20)
            self.padding = dp(20)
            self.dialog_ref = dialog_ref

            # Ícone de verificação com animação
            self.verified_icon = Image(
                source="src/check.png",
                size_hint=(None, None),
                width=dp(50),
                height=dp(50),
                opacity=0  # Inicialmente invisível para a animação de entrada
            )
            self.add_widget(self.verified_icon)

            # Iniciar animação de subida e pulso
            self.start_entry_animation()

            # Botão OK
            self.ok_button = MDRaisedButton(
                text="OK",
                pos_hint={"center_x": 0.5},
                on_release=self.dismiss_dialog
            )
            self.add_widget(self.ok_button)

        def start_entry_animation(self):
            # Animação de subida até o topo
            entry_anim = Animation(y=self.height * 3.5, opacity=1, duration=1.2, t='out_cubic') + Animation(
                size=(dp(55), dp(55)), duration=0.3, t='in_out_sine') + Animation(
                size=(dp(50), dp(50)), duration=0.3, t='in_out_sine'
            )
            entry_anim.start(self.verified_icon)

        def dismiss_dialog(self, *args):
            self.dialog_ref.loading_dialog.dismiss()
''' def show_devolver_button(self):
        # Mostra o botão "Devolver" e oculta o botão "Pegar"
        self.devolver_button.opacity = 1
        self.devolver_button.disabled = False

        pegar_button = self.ids.pegar_button
        pegar_button.opacity = 0
        pegar_button.disabled = True

    def show_pegar_button(self):
        # Mostra o botão "Pegar" e oculta o botão "Devolver"
        self.devolver_button.opacity = 0
        self.devolver_button.disabled = True

        pegar_button = self.ids.pegar_button
        pegar_button.opacity = 1
        pegar_button.disabled = False

        # Exibe o diálogo ao clicar no botão "Devolver"
        self.show_loading_dialog()
'''