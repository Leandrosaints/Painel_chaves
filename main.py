import re
from datetime import datetime

import requests
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from login import LoginScreen
from gestor import MainScreen  # Importar telas
from infoScreen import InfoScreen
from info_user import UserInfoScreen
from redefinir_senha import ResetPasswordScreen
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
    user_id = None
    def build(self):
        try:
            Builder.load_string(kv)
            self.manager = MDScreenManager()

            # Adiciona as telas ao gerenciador
            self.manager.add_widget(LoginScreen(name="login"))
            self.manager.add_widget(MainScreen(name="main"))
            self.manager.add_widget(InfoScreen(name="info_screen"))
            self.manager.add_widget(UserInfoScreen(name='info_user'))
            self.manager.add_widget(ResetPasswordScreen(name='reset_senha'))

            return self.manager
        except Exception as e:
            self.show_error_popup("Erro ao construir a interface", str(e))


    def on_click_info_salas(self, index, name):
        asyncio.run(self.show_info_screen(index, name))


    async def show_user_info_screen(self):
        try:
            user_info_screen = self.root.get_screen('info_user')
            user_info_screen.toggle_show_history()  # Exibe a seção de histórico de salas

            user_id = self.user_id
            dados = await self.api.fetch_user(user_id)
            historicos = await self.api.fetch_historico(user_id)

            if historicos:
                for historico in historicos:
                    historico_item = MDBoxLayout(
                        orientation="vertical",
                        spacing=dp(5),
                        adaptive_height=True,
                        md_bg_color=(0.95, 0.95, 0.95, 1),
                        padding=dp(10)
                    )

                    sala_nome = MDLabel(
                        text=f"Sala: {historico.get('sala_nome', 'Não informado')}",
                        font_style="Body1",
                        theme_text_color="Primary",
                        halign="left",
                        size_hint_y=None,
                        height=dp(24)
                    )
                    entrada = MDLabel(
                        text=f"Data e Hora de Entrada: {historico.get('entrada', 'Não informado')}",
                        font_style="Caption",
                        theme_text_color="Secondary",
                        halign="left",
                        size_hint_y=None,
                        height=dp(20)
                    )
                    saida = MDLabel(
                        text=f"Hora Finalizada: {historico.get('saida', 'Não informado')}",
                        font_style="Caption",
                        theme_text_color="Secondary",
                        halign="left",
                        size_hint_y=None,
                        height=dp(20)
                    )

                    historico_item.add_widget(sala_nome)
                    historico_item.add_widget(entrada)
                    historico_item.add_widget(saida)

                    user_info_screen.ids.history_layout.add_widget(historico_item)
            else:
                print("Nenhum histórico encontrado para o usuário.")
            if dados:
                campos = {
                    "nome": user_info_screen.ids.first_name,
                    "sobrenome": user_info_screen.ids.second_name,
                    "funcao":user_info_screen.ids.funcao_id,
                    "email": user_info_screen.ids.email,
                    "telefone": user_info_screen.ids.phone,

                }

                for chave, campo in campos.items():
                    campo.text = dados.get(chave, "Não informado")

                endereco = dados.get("endereco", "Não informado")
                logradouro, numero, bairro, cidade, estado = self.desconcatenar_endereco(endereco)
                user_info_screen.ids.address.text = logradouro if logradouro else "Nao informado"
                user_info_screen.ids.neighborhood.text = bairro if bairro else "Não informado"
                user_info_screen.ids.house_number.text = numero if numero else "Não informado"
                user_info_screen.ids.city.text = cidade if cidade else "Não informado"
                user_info_screen.ids.state.text = estado if estado else "Não informado"

                self.root.current = 'info_user'
            else:
                print("Usuário não encontrado ou sem dados!")

        except Exception as e:
            print("Ocorreu um erro:", str(e))

    #async def show_historico_acesso(self):


    def try_go_back_to_main(self):
        # Função para verificar o login e mudar a tela
        if self.user_token:
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
    async def show_info_screen(self, index, name):

        info_screen = self.root.get_screen('info_screen')
        info_screen.ids.info_title.text = f"{name}"
        info_screen.update_title(name)  # Atualiza o título
        info_screen.toggle_key_status(index + 1)

        user_id = self.user_id
        dados = await self.api.fetch_user(user_id)

        if dados:
            campos = {
                "nome": info_screen.ids.name_id,
                "funcao":info_screen.ids.funcao,
                "email": info_screen.ids.email_id,
                "telefone": info_screen.ids.phone_id,

            }

            for chave, campo in campos.items():
                campo.text = dados.get(chave, "Não informado")



        #info_screen.ids.info_details.text = f"O Número : {index + 1}"
        self.root.current = 'info_screen'
    async def login(self):
        try:
            email = self.manager.get_screen("login").ids.email.text
            senha = self.manager.get_screen("login").ids.senha.text

            token_info = await self.api.authenticator(email, senha)

            if token_info:
                # Armazena o token e o ID do usuário separadamente
                self.user_token = token_info["token"]
                self.user_id = token_info["user_id"]  # Armazena o ID do usuário
                #self.user_id = token_info["user_id"]  # Armazena o ID do usuário

                self.manager.current = "main"  # Muda para a tela principal

            else:

                self.show_error_popup("Erro", "Credenciais inválidas!")  # Exibe um popup de erro
        except Exception as e:
            self.show_error_popup("Erro ao tentar login", str(e))
    async def register_historico(self, sala_id: int):
        # Criação do dicionário com os dados a serem enviados
        dados_historico = {
            "sala_id": sala_id,
            "usuario_id": self.user_id,
            "data_hora_retirada": datetime.now().isoformat(),  # ISO format para garantir o formato correto
            "data_hora_devolucao": datetime.now().isoformat()  # ISO format
        }

        # Enviar o histórico usando a função enviar_historico
        resposta = await self.api.enviar_historico(dados_historico)

        # Verificar a resposta
        if resposta:
            print("Histórico de acesso registrado com sucesso!")
            print(f"Dados retornados: {resposta}")
        else:
            print("Erro ao registrar o histórico de acesso.")
            # Imprimir o conteúdo do erro para ajudar a entender o problema
            print(f"Erro detalhado: {resposta}")
    async def reset_senha_async(self):
        # Obtem a tela de redefinição de senha
        password_reset = self.root.get_screen('reset_senha')

        # Armazena as senhas e email em um dicionário
        passwords = {
            "email": password_reset.ids.email.text,  # Agora estamos coletando o email
            "new_password": password_reset.ids.new_password.text,
            "confirm_password": password_reset.ids.confirm_password.text,
        }

        # Verificar se as senhas correspondem
        if passwords["new_password"] == passwords["confirm_password"]:
            print("Senha redefinida com sucesso!")
            # Chama a função assíncrona para atualizar a senha
            try:
                # Aqui, estamos passando o email corretamente para a função de atualização
                response = await self.api.update_password(passwords["email"], passwords["new_password"])
                if response:
                    print(f"Resposta da API: {response}")
                else:
                    print("Erro ao redefinir a senha.")
            except Exception as e:
                print(f"Erro ao tentar enviar dados para o servidor: {str(e)}")
        else:
            print("As senhas não correspondem.")

    async def update_user_info(self):
        user_info = self.root.get_screen('info_user')

        # Formata o endereço
        endereco_concatenado = self.formatar_endereco(
            logradouro=user_info.ids.address.text,
            bairro=user_info.ids.neighborhood.text,
            numero=user_info.ids.house_number.text,
            cidade=user_info.ids.city.text,
            estado=user_info.ids.state.text
        )

        # Coleta os valores dos campos
        user_data = {
            "nome": user_info.ids.first_name.text,
            "sobrenome": user_info.ids.second_name.text,
            "funcao": user_info.ids.funcao_id.text,
            "email": user_info.ids.email.text,
            "senha": user_info.ids.senha.text,
            "telefone": user_info.ids.phone.text,
            "endereco": endereco_concatenado,
        }

        # Validação das senhas
        if user_data["senha"] != user_info.ids.confirme_senha.text:
            self.show_error_popup("Erro", "As senhas não coincidem.")
            return

        try:
            # Chamada assíncrona para atualizar o usuário
            await self.api.update_usuario(user_id=self.user_id, user_data=user_data)
        except Exception as e:
            self.show_error_popup('Erro', "Tente novamente mais tarde: 422")

    async def save_user_info(self):
        user_info = self.root.get_screen('info_user')

        # Coleta os valores dos campos
        user_data = {
            "nome": user_info.ids.first_name.text.strip(),
            "sobrenome": user_info.ids.second_name.text.strip(),
            "funcao": user_info.ids.funcao.text.strip(),
            "email": user_info.ids.email.text.strip(),
            "senha": user_info.ids.senha.text.strip(),
            "telefone": user_info.ids.phone.text.strip(),
            "endereco": self.formatar_endereco(
                logradouro=user_info.ids.address.text.strip(),
                bairro=user_info.ids.neighborhood.text.strip(),
                numero=user_info.ids.house_number.text.strip(),
                cidade=user_info.ids.city.text.strip(),
                estado=user_info.ids.state.text.strip()
            )
        }




        if user_data["senha"] != user_info.ids.confirme_senha.text.strip():
            self.show_error_popup('Erro', "As senhas não coincidem.")
            return

        try:
            # Chama a API para registrar o usuário
            response = await self.api.register_user_now(user_data)

            # Verifica a resposta da API
            if response.get("detail") == "Sucesso":
                self.show_error_popup('Sucesso', "Dados inseridos com sucesso!")
            else:
                self.show_error_popup('Erro', "Erro ao cadastrar usuário. Tente novamente.")

        except Exception as e:
            print("Erro ao conectar-se com o servidor:", e)
            self.show_error_popup('Erro', f"Erro ao conectar-se com o servidor: {e}")

    def show_error_popup(self, title, message):
        # Cria e exibe um popup de erro
        popup_content = Label(text=message)
        popup = Popup(title=title, content=popup_content, size_hint=(0.8, 0.4))
        popup.open()




    #concatena o endereço para ficar em apenas um campo no banco de dados
    def formatar_endereco(self, logradouro, bairro, numero, cidade, estado):
        # Concatena os campos com uma vírgula e espaço entre eles, ignorando os campos vazios
        endereco = ", ".join(filter(None, [logradouro, f"Nº {numero}", bairro, cidade, estado]))
        return endereco


    def desconcatenar_endereco(self, endereco: str):
        partes = [parte.strip() for parte in endereco.split(",")]
        logradouro = None
        numero = None
        bairro = None
        cidade = None
        estado = None

        if len(partes) > 0:
            logradouro = partes[0]
        if len(partes) > 1:
            if "Nº" in partes[1]:
                numero = re.search(r'Nº (\d+)', partes[1])
                numero = numero.group(1) if numero else None
                bairro = partes[2] if len(partes) > 2 else None
            else:
                numero = partes[1]
                bairro = partes[2] if len(partes) > 2 else None

        if len(partes) > 3:
            cidade = partes[-2]
            estado = partes[-1]

        return logradouro, numero, bairro, cidade, estado



    def on_click_get_historico(self, sala_id):
        try:
            # Executa a função assíncrona diretamente no loop de eventos
            asyncio.run(self.register_historico(sala_id))
        except Exception as e:
            print("erro ao tentar enviar dados para o historico de chaves:", str(e))


    def on_reset_senha(self):#chama a funcao que envia os dados na requisao de reset
        try:
            # Executa a função assíncrona diretamente no loop de eventos
            asyncio.run(self.reset_senha_async())
        except Exception as e:
            print("erro ao tentar redefinir senha:", str(e))





    def on_login_button_click(self):
        asyncio.run(self.login())  # Chama a função de login

    def on_user_dados(self):#
        try:
            # Executa a função assíncrona diretamente no loop de eventos
            asyncio.run(self.show_user_info_screen())
        except Exception as e:
            self.show_error_popup('Erro', "Tente novamente mais tarde: 422")

    def on_save_register_now(self):
        try:
            asyncio.run(self.save_user_info())
        except Exception as e:
            self.show_error_popup('Erro', "Tente novamente mais tarde: 422")

    def on_update_user(self):
        try:
            asyncio.run(self.update_user_info())
        except Exception as e:
            self.show_error_popup('Erro', "Tente novamente mais tarde: 422")
if __name__ == "__main__":
    MainApp().run()
