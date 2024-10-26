from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.textfield import MDTextField
from kivymd.uix.label import MDLabel
from kivy.core.window import Window
import main
# Ajuste a janela para desktop ou mobile.
Window.size = (350, 600)  # Tamanho padrão para dispositivos móveis

KV = '''
MDScreen:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)
        pos_hint: {"center_x": 0.5, "center_y": 0.5}
        size_hint_x: None if root.width > 500 else 1
        width: min(root.width, dp(300))

        # Adiciona a logo no topo
        Image:
            source: "src/logo.png"  # Coloque o caminho correto para a imagem da logo
            size_hint_y: None
            height: dp(100)
            allow_stretch: True
            keep_ratio: True

        MDLabel:
            text: "Login"
            font_style: "H3"
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
            on_release: app.login()

        MDRaisedButton:
            text: "Criar Conta"
            pos_hint: {"center_x": 0.5}
            size_hint_x: None
            width: dp(100)
            on_release: app.create_account()

        MDLabel:
            text: "Esqueceu sua senha?"
            halign: "center"
            theme_text_color: "Custom"
            text_color: app.theme_cls.primary_color
            size_hint_y: None
            height: self.texture_size[1]
'''

class LoginApp(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Blue"  # Defina a cor primária
        return Builder.load_string(KV)

    def login(self):
        email = self.root.ids.email.text
        senha = self.root.ids.senha.text
        if email == "user@gmail.com" and senha == "12345":
            print("Login bem-sucedido!")
            self.stop()  # Fecha a aplicação de login
            main.MyApp().run()# .MainApp().run()  # Inicia a aplicação principal
            # Aqui você pode adicionar lógica para autenticação.
            print(f"Tentativa de login com email: {email} e senha: {senha}")

    def create_account(self):
        # Lógica para criar conta ou navegar para a tela de criação de conta.
        print("Navegando para a tela de criação de conta")

LoginApp().run()
