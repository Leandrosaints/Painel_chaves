import time
from kivy.config import Config

Config.set('input', 'wm_pen', 'null')
Config.set('input', 'wm_touch', 'null')

from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

KV = '''
<LoginScreen>:
    name: 'login_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        pos_hint: {"center_x": 0.5, "center_y": 0.7}
        size_hint_x: None if root.width > 500 else 1
        width: min(root.width, dp(300))

        Image:
            source: "src/logo.png"  # Coloque o caminho correto para a imagem da logo
            size_hint_y: None
            height: dp(100)
            allow_stretch: True
            keep_ratio: True

        MDLabel:
            text: "Login"
            font_style: "H5"
            halign: "center"
            size_hint_y: None
            height: self.texture_size[1]

        MDTextField:
            id: email
            hint_text: "Email"
            icon_right: "email"
            mode: "rectangle"
            size_hint_y: None
            height: dp(50)

        MDTextField:
            id: senha
            hint_text: "Senha"
            icon_right: "lock"
            password: True
            mode: "rectangle"
            size_hint_y: None
            height: dp(50)

        MDRaisedButton:
            text: "Entrar"
            pos_hint: {"center_x": 0.5}
            size_hint_x: None
            width: dp(100)
            on_release: app.on_login_button_click() 

        MDTextButton:
            text: "Cadastrar"
            pos_hint: {"center_x": 0.5}
            on_release: app.root.current = 'info_user'

        MDTextButton:
            text: "Esqueceu sua senha?"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            size_hint_y: None
            height: self.texture_size[1]
            on_release: app.root.current = 'reset_senha'
'''





class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)
"""
<LoadingScreen>:
    name: 'loading_screen'
    MDBoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(20)
        MDLabel:
            text: "Carregando..."
            font_style: "H4"
            halign: "center"
        MDSpinner:
            size_hint: None, None
            size: dp(46), dp(46)
            active: True


class LoginApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"
        return Builder.load_string(KV)

    def login(self):
        email = self.root.get_screen('login_screen').ids.email.text
        senha = self.root.get_screen('login_screen').ids.senha.text

        if email == "user" and senha == "123":
            # Alterna para a tela de carregamento
            self.root.current = 'loading_screen'
            # Agenda a execução do app principal após 2 segundos
            Clock.schedule_once(self.start_main_app, 2)

    def start_main_app(self, *args):
        # Fecha a aplicação de login antes de iniciar o app principal
        self.stop()
        # Inicia a aplicação principal (gestor) em uma nova instância
        gestor.MyApp().run()

if __name__ == "__main__":
    LoginApp().run()"""
