import requests
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from login import LoginScreen
from gestor import MainScreen  # Importar telas
from infoScreen import InfoScreen
from info_user import UserInfoScreen
from core.api_client import APIClient
kv = '''
MDScreenManager:
    LoginScreen:
    MainScreen:
    InfoScreen:
    UserInfoScreen
'''
import httpx
import asyncio


async def login(username: str, password: str):
    url = "http://127.0.0.1:8000/api/v1/usuarios/login"
    async with httpx.AsyncClient() as client:
        response = await client.post(url, data={"username": username, "password": password})

        if response.status_code == 200:
            return response.json()  # Retorna o token de acesso
        else:
            print(f"Erro: {response.json()}")
            return None

class MainApp(MDApp):
    api = APIClient("http://127.0.0.1:8000")
    user_token = None  # Variável para armazenar o token do usuário
    def build(self):
        try:
            Builder.load_string(kv)
            self.manager = MDScreenManager()

            # Adiciona as telas ao gerenciador
            self.manager.add_widget(LoginScreen(name="login"))
            self.manager.add_widget(MainScreen(name="main"))
            self.manager.add_widget(InfoScreen(name="info_screen"))
            self.manager.add_widget(UserInfoScreen(name='info_user'))

            return self.manager
        except Exception as e:
            self.show_error_popup("Erro ao construir a interface", str(e))

    def show_info_screen(self, index, name):

        info_screen = self.root.get_screen('info_screen')
        info_screen.ids.info_title.text = f"{name}"

        info_screen.update_title(name)  # Atualiza o título
        info_screen.toggle_key_status(index + 1)
        #info_screen.ids.info_details.text = f"O Número : {index + 1}"
        self.root.current = 'info_screen'

    def show_user_info_screen(self, user_data):
        try:
            # Obtém a tela de informações do usuário
            user_info_screen = self.root.get_screen('info_user')

            user_info_screen.toggle_show_history()
            #user_info_screen.root.toggle_show_history()
            # Preenche os campos de texto com os dados do usuário
            user_info_screen.ids.first_name.text = user_data.get("full_name", "Não informado")
            user_info_screen.ids.second_name.text = user_data.get("second_name", "Não informado")
            user_info_screen.ids.email.text = user_data.get("email", "Não informado")
            user_info_screen.ids.phone.text = user_data.get("phone", "Não informado")
            user_info_screen.ids.address.text = user_data.get("address", "Não informado")
            user_info_screen.ids.neighborhood.text = user_data.get("neighborhood", "Não informado")
            user_info_screen.ids.house_number.text = user_data.get("house_number", "Não informado")
            user_info_screen.ids.city.text = user_data.get("city", "Não informado")
            user_info_screen.ids.state.text = user_data.get("state", "Não informado")

            # Muda a tela atual para `user_info_screen`
            self.root.current = 'info_user'
        except Exception as e:
            # Mostra um popup em caso de erro
            self.show_error_popup("Erro ao exibir informações do usuário", str(e))



    def is_logged_in(self):
        # Verifica se o usuário está logado
        return self.user_token is not None

    def try_go_back_to_main(self):
        # Função para verificar o login e mudar a tela
        if self.is_logged_in():

            self.root.current = "main"

        else:
            self.root.current = 'login'
            #print("Usuário não está logado. Não pode retornar para a tela principal.")

    '''async def authenticator(self, username: str, password: str):
        url = "http://127.0.0.1:8000/api/v1/usuarios/login"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data={"username": username, "password": password})

            if response.status_code == 200:
                return response.json()  # Retorna o token de acesso
            else:
                print(f"Erro: {response.json()}")
                return None'''

    async def login(self):
        try:

            email = self.manager.get_screen("login").ids.email.text
            senha = self.manager.get_screen("login").ids.senha.text

            token_info = await self.api.authenticator(email, senha)  # Chama a função correta

            if token_info:

                self.user_token = token_info
                #print("Login bem-sucedido!")
                self.manager.current = "main"  # Muda para a tela principal

            else:

                self.show_error_popup("Erro", "Credenciais inválidas!")  # Exibe um popup de erro
        except Exception as e:
            self.show_error_popup("Erro ao tentar login", str(e))


    def show_error_popup(self, title, message):
        # Cria e exibe um popup de erro
        popup_content = Label(text=message)
        popup = Popup(title=title, content=popup_content, size_hint=(0.8, 0.4))
        popup.open()

    def on_login_button_click(self):
        asyncio.run(self.login())  # Chama a função de login


    def on_register_button_click(self):
        # Ação de cadastro
        self.root.current = 'info_user'


    #concatena o endereço para ficar em apenas um campo no banco de dados
    def formatar_endereco(self, logradouro, bairro, numero, cidade, estado):
        # Concatena os campos com uma vírgula e espaço entre eles, ignorando os campos vazios
        endereco = ", ".join(filter(None, [logradouro, f"Nº {numero}", bairro, cidade, estado]))
        return endereco


    #metodo responsavel por inserir os dados do cadastro do usuario
    def save_user_info(self):
        user_info = self.root.get_screen('info_user')
        endereco_concatenado = self.formatar_endereco(
            logradouro=user_info.ids.address.text,
            bairro=user_info.ids.neighborhood.text,
            numero=user_info.ids.house_number.text,
            cidade=user_info.ids.city.text,
            estado=user_info.ids.state.text
        )
        print(endereco_concatenado)
        # Coleta os valores dos campos
        user_data = {
            "nome": user_info.ids.first_name.text,
            "sobrenome":user_info.ids.second_name.text,
            "email": user_info.ids.email.text,
            "senha": user_info.ids.senha.text,
            "telefone": user_info.ids.phone.text,
            "endereco":endereco_concatenado,
        }

        # Validações podem ser adicionadas aqui, como confirmar a senha
        if user_data["senha"] != user_info.ids.confirme_senha.text:
            print("As senhas não coincidem.")
            return

        # Faz a requisição POST para o endpoint de registro
        try:
            response = requests.post("http://127.0.0.1:8000/api/v1/usuarios/register", json=user_data)
            if response.status_code == 201:
                print("Usuário cadastrado com sucesso!")
            else:
                print("Erro ao cadastrar usuário:", response.json().get("detail", "Erro desconhecido"))
        except Exception as e:
            print("Erro ao conectar-se com o servidor:", e)



if __name__ == "__main__":
    MainApp().run()
