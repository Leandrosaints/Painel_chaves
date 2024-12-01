import time
from kivy.config import Config
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen

# Desativar gestos de toque (se necessário)
Config.set('input', 'wm_pen', 'null')
Config.set('input', 'wm_touch', 'null')

KV = '''
<LoginScreen>:
    name: 'login_screen'
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(15)  # Melhor espaçamento entre os elementos
        pos_hint: {"center_x": 0.5, "center_y": 0.7}
        size_hint_x: None if root.width > 500 else 1
        width: min(root.width, dp(350))

        # Logo na parte superior
        Image:
            source: "src/logo.png"  # Substitua pelo caminho correto para sua logo
            size_hint_y: None
            height: dp(120)
            allow_stretch: True
            keep_ratio: True


        # Campo de email
        MDTextField:
            id: email
            hint_text: "Digite seu email"
            icon_right: "email"
            mode: "rectangle"
            size_hint_y: None
            height: dp(50)
            font_size: "18sp"
            radius: [10, 10, 10, 10]

        # Campo de senha
        MDTextField:
            id: senha
            hint_text: "Digite sua senha"
            icon_right: "lock"
            password: True
            mode: "rectangle"
            size_hint_y: None
            height: dp(50)
            font_size: "18sp"
            radius: [10, 10, 10, 10]

        # Opção de mostrar senha
        MDBoxLayout:
            orientation: "horizontal"
            spacing: dp(10)
            size_hint_y: None
            height: dp(30)
            MDCheckbox:
                id: show_password
                size_hint: None, None
                size: dp(24), dp(24)
                on_active: 
                    
                    app.root.get_screen('login').toggle_password_visibility(self, senha)
            MDLabel:
                text: "Mostrar senha"
                valign: "center"
                halign: "left"

        # Botão de login com design moderno
        MDRaisedButton:
            text: "Entrar"
            pos_hint: {"center_x": 0.5}
            size_hint_x: None
            width: dp(120)
            md_bg_color: app.theme_cls.primary_color
            text_color: 1, 1, 1, 1  # Texto branco
            elevation: 1
            on_release: app.on_login_button_click()

        # Botão para cadastro
        MDTextButton:
            text: "Cadastrar-se"
            pos_hint: {"center_x": 0.5}
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            on_release: app.go_to_info_user_clean()

        # Botão para resetar senha
        MDTextButton:
            text: "Esqueceu sua senha?"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            size_hint_y: None
            pos_hint: {"center_x": 0.5}
            height: self.texture_size[1]
            on_release: app.root.current = 'reset_senha'
'''

class LoginScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Builder.load_string(KV)

    def toggle_password_visibility(self, checkbox, password_field):
        password_field.password = not checkbox.active

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
