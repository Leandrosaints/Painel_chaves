from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.uix.button import MDRaisedButton

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
                source: "src/logo.png"
                size_hint_x: None
                width: dp(60)
                allow_stretch: True
                keep_ratio: True

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
            elevation: 6
            md_bg_color: app.theme_cls.bg_light

            # Seção de Informações do Professor
            MDBoxLayout:
                orientation: 'vertical'
                spacing: dp(15)

                MDLabel:
                    text: "Nome do Responsável: João da Silva"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"

                MDLabel:
                    text: "Função: Professor de Matemática"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"

                MDLabel:
                    text: "Email: joao.silva@escola.com"
                    font_style: "Subtitle1"
                    theme_text_color: "Primary"

                MDLabel:
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
                        source: "src/digital_red.png"
                        size_hint_y: None
                        height: dp(120)
                        allow_stretch: True
                        keep_ratio: True
                    MDLabel:
                        text: "Data: 28/10/2024"
                        font_style: "Caption"
                        halign: "center"
                        theme_text_color: "Secondary"
                    MDLabel:
                        text: "Hora: 14:30"
                        font_style: "Caption"
                        halign: "center"
                        theme_text_color: "Secondary"

                # Botões
                MDBoxLayout:
                    orientation: 'vertical'
                    size_hint_x: 0.4
                    spacing: dp(15)

                    MDRaisedButton:
                        text: "Cancelar"
                        md_bg_color: app.theme_cls.error_color
                        pos_hint: {"center_x": 0.5}
                        on_release: app.cancel_action()

                    MDRaisedButton:
                        text: "Pegar"
                        md_bg_color: app.theme_cls.primary_color
                        pos_hint: {"center_x": 0.5}
                        on_release: root.show_devolver_button()

                    # Botão "Devolver" oculto inicialmente
                    MDRaisedButton:
                        id: devolver_button
                        text: "Devolver"
                        md_bg_color: app.theme_cls.primary_color
                        pos_hint: {"center_x": 0.5}
                        opacity: 0  # Inicialmente invisível
                        disabled: True  # Desativado até ser necessário
                        on_release: app.devolver_action()
"""

Builder.load_string(kv)

class InfoScreen(MDScreen):
    devolver_button = ObjectProperty(None)

    def show_devolver_button(self):
        # Torna o botão "Devolver" visível e habilitado
        self.devolver_button.opacity = 1
        self.devolver_button.disabled = False
