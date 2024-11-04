from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

kv = """

<UserInfoScreen>:
    ScrollView:
        MDBoxLayout:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(20)
            adaptive_height: True
            
            MDIconButton:
                icon: "arrow-left"
                pos_hint: {"center_y": 0.5}
                on_release: app.root.current = "main"

            MDLabel:
                text: "Cadastro" if not root.show_history else "Informações do Usuário"
                font_style: "H5"
                halign: "center"
                theme_text_color: "Primary"
                size_hint_y: None
                height: self.texture_size[1] + dp(10)

            # Seção: Informações Pessoais
            MDCard:
                orientation: "vertical"
                size_hint: 0.9, None
                height: self.minimum_height
                padding: dp(20)
                spacing: dp(15)
                pos_hint: {"center_x": 0.5}
                ripple_behavior: True
                adaptive_height: True

                MDLabel:
                    text: "Informações Pessoais"
                    font_style: "H6"
                    theme_text_color: "Secondary"
                    halign: "left"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDTextField:
                    id: first_name
                    hint_text: "Primeiro nome"
                    helper_text: "Primeiro nome"
                    helper_text_mode: "on_focus"
                    size_hint_x: 1
                MDTextField:
                    id: second_name
                    hint_text: "Sobrenome"
                    helper_text: "Sobrenome"
                    helper_text_mode: "on_focus"
                    size_hint_x: 1
                MDTextField:
                    id: email
                    hint_text: "Email"
                    helper_text: "Digite o email"
                    helper_text_mode: "on_focus"
                    size_hint_x: 1
                MDTextField:
                    id: phone
                    hint_text: "Telefone"
                    helper_text: "Digite o telefone"
                    helper_text_mode: "on_focus"
                    size_hint_x: 1
                MDTextField:
                    id: senha
                    hint_text: "Senha"
                    helper_text: "Digite uma senhar"
                    helper_text_mode: "on_focus"
                    size_hint_x: 1
                MDTextField:
                    id: confirme_senha
                    hint_text: "Confirme a Senha"
                    helper_text: "Confirme a Senha"
                    helper_text_mode: "on_focus"
                    size_hint_x: 1
                

            # Seção: Endereço
            MDCard:
                orientation: "vertical"
                size_hint: 0.9, None
                height: self.minimum_height
                padding: dp(20)
                spacing: dp(15)
                pos_hint: {"center_x": 0.5}
                ripple_behavior: True
                adaptive_height: True

                MDLabel:
                    text: "Endereço"
                    font_style: "H6"
                    theme_text_color: "Secondary"
                    halign: "left"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDTextField:
                    id: address
                    hint_text: "Endereço"
                    helper_text: "Digite o endereço"
                    helper_text_mode: "on_focus"
                    size_hint_x: 1

                MDTextField:
                    id: neighborhood
                    hint_text: "Bairro"
                    helper_text: "Digite o bairro"
                    helper_text_mode: "on_focus"
                    size_hint_x: 1

                MDTextField:
                    id: house_number
                    hint_text: "Número"
                    helper_text: "Número da casa/apartamento"
                    helper_text_mode: "on_focus"
                    size_hint_x: 1

                MDTextField:
                    id: city
                    hint_text: "Cidade"
                    helper_text: "Digite a cidade"
                    helper_text_mode: "on_focus"
                    size_hint_x: 1

                MDTextField:
                    id: state
                    hint_text: "Estado"
                    helper_text: "Digite o estado"
                    helper_text_mode: "on_focus"
                    size_hint_x: 1

            # Seção: Histórico de Salas Usadas
            MDCard:
                orientation: "vertical"
                size_hint: 0.9, None
                height: self.minimum_height
                padding: dp(20)
                spacing: dp(15)
                pos_hint: {"center_x": 0.5}
                ripple_behavior: True
                adaptive_height: True
                opacity: 1 if root.show_history else 0
                canvas.before:
                    Color:
                        rgba: 1, 1, 1, 1 if root.show_history else 0  # Controla a visibilidade
                    Rectangle:
                        pos: self.pos
                        size: self.size

                MDLabel:
                    text: "Histórico de Salas"
                    font_style: "H6"
                    theme_text_color: "Secondary"
                    halign: "left"
                    size_hint_y: None
                    height: self.texture_size[1]

                MDBoxLayout:
                    orientation: "vertical"
                    spacing: dp(10)
                    adaptive_height: True

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(5)
                        adaptive_height: True
                        md_bg_color: 0.95, 0.95, 0.95, 1

                        MDLabel:
                            text: "Sala: 101"
                            font_style: "Body1"
                            theme_text_color: "Primary"
                            halign: "left"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            text: "Data e Hora de Entrada: 01/10/2024 10:00"
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                            halign: "left"
                            size_hint_y: None
                            height: self.texture_size[1]

                        MDLabel:
                            text: "Hora Finalizada: 01/10/2024 12:00"
                            font_style: "Caption"
                            theme_text_color: "Secondary"
                            halign: "left"
                            size_hint_y: None
                            height: self.texture_size[1]

            MDRaisedButton:
                text: "Salvar Informações" if root.show_history else "Cadastrar"
                pos_hint: {"center_x": 0.5}
                size_hint: None, None
                size: dp(200), dp(48)
                on_release: app.save_user_info()
"""


Builder.load_string(kv)


class UserInfoScreen(MDScreen):
    show_history = BooleanProperty(False)  # Define se o histórico de salas será mostrado