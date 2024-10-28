from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from login import LoginScreen
from gestor import MainScreen  # Importar telas
from infoScreen import InfoScreen
import trio

kv = '''
MDScreenManager:
    LoginScreen:
    MainScreen:
    InfoScreen:
'''


class MainApp(MDApp):
    def build(self):
        Builder.load_string(kv)
        self.manager = MDScreenManager()

        # Adiciona as telas ao gerenciador
        self.manager.add_widget(LoginScreen(name="login"))
        self.manager.add_widget(MainScreen(name="main"))
        self.manager.add_widget(InfoScreen(name="info_screen"))


        return self.manager

    def show_info_screen(self, index, name):
        info_screen = self.root.get_screen('info_screen')
        info_screen.ids.info_title.text = f"Informações da {name}"
        info_screen.ids.info_details.text = f"Número: {index + 1}"
        self.root.current = 'info_screen'

    def go_back_to_main_screen(self):
        self.root.current = 'main'
    def login(self):
        email = self.manager.get_screen("login").ids.email.text
        senha = self.manager.get_screen("login").ids.senha.text

        if email == "user" and senha == "123":
            print("Login bem-sucedido!")
            self.manager.current = "main"
        else:
            print("Credenciais inválidas!")


if __name__ == "__main__":
    MainApp().run()
