from kivy.lang import Builder
from kivy.properties import BooleanProperty
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
kv_reset_password = """
<ResetPasswordScreen>:
    name: 'reset_password_screen'

    MDBoxLayout:
        orientation: "vertical"
        padding: dp(20)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint: 0.9, 0.9

        # Adiciona um botão de seta no topo da tela para voltar
        MDBoxLayout:
            size_hint_y: None
            height: "50dp"
            orientation: "horizontal"
            padding: dp(10)
            MDIconButton:
                icon: "arrow-left"  # Ícone de seta para voltar
                on_release: app.root.current = "login"

        # Card de redefinição de senha
        MDCard:
            orientation: "vertical"
            padding: dp(20)
            spacing: dp(20)
            size_hint_y: None
            height: self.minimum_height
            pos_hint: {"center_x": 0.5}
            elevation: 4

            MDLabel:
                text: "Redefinir Senha"
                font_style: "H5"
                halign: "center"
                theme_text_color: "Primary"

            # Campo para email
            MDTextField:
                id: email
                hint_text: "Email"
                helper_text: "Digite seu email"
                helper_text_mode: "on_focus"
                size_hint_x: 1

            # Campo para nova senha
            MDTextField:
                id: new_password
                hint_text: "Nova senha"
                password: True
                helper_text: "Digite a nova senha"
                helper_text_mode: "on_focus"
                size_hint_x: 1

            # Campo para confirmar a nova senha
            MDTextField:
                id: confirm_password
                hint_text: "Confirme a nova senha"
                password: True
                helper_text: "Digite a nova senha novamente"
                helper_text_mode: "on_focus"
                size_hint_x: 1

            MDRaisedButton:
                text: "Salvar"
                pos_hint: {"center_x": 0.5}
                on_release: app.reset_senha()
"""

Builder.load_string(kv_reset_password)
class ResetPasswordScreen(MDScreen):
    pass
#def save_password(self):