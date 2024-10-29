from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from login import LoginScreen
from gestor import MainScreen  # Importar telas
from infoScreen import InfoScreen


kv = '''
MDScreenManager:
    LoginScreen:
    MainScreen:
    InfoScreen:
'''

class MainApp(MDApp):
    def build(self):
        try:
            Builder.load_string(kv)
            self.manager = MDScreenManager()

            # Adiciona as telas ao gerenciador
            self.manager.add_widget(LoginScreen(name="login"))
            self.manager.add_widget(MainScreen(name="main"))
            self.manager.add_widget(InfoScreen(name="info_screen"))

            return self.manager
        except Exception as e:
            self.show_error_popup("Erro ao construir a interface", str(e))

    def show_info_screen(self, index, name):
        try:
            info_screen = self.root.get_screen('info_screen')
            info_screen.ids.info_title.text = f"Pegar a chave da {name}"
            #info_screen.ids.info_details.text = f"O Número : {index + 1}"
            self.root.current = 'info_screen'
        except Exception as e:
            self.show_error_popup("Erro ao exibir informações", str(e))

    def go_back_to_main_screen(self):
        try:
            self.root.current = 'main'
        except Exception as e:
            self.show_error_popup("Erro ao voltar para a tela principal", str(e))

    def login(self):
        try:
            email = self.manager.get_screen("login").ids.email.text
            senha = self.manager.get_screen("login").ids.senha.text

            if email == "user" and senha == "123":
                print("Login bem-sucedido!")
                self.manager.current = "main"
            else:
                print("Credenciais inválidas!")
        except Exception as e:
            self.show_error_popup("Erro ao tentar login", str(e))

    def show_error_popup(self, title, message):
        # Cria e exibe um popup de erro
        popup_content = Label(text=message)
        popup = Popup(title=title, content=popup_content, size_hint=(0.8, 0.4))
        popup.open()

if __name__ == "__main__":
    MainApp().run()
