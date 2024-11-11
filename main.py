import re
from datetime import datetime
import asyncio

from kivy.clock import Clock
from passlib.context import CryptContext
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
from core.api_client import APIClient, APIClientSalas

kv = '''
MDScreenManager:
    LoginScreen:
    MainScreen:
    InfoScreen:
    UserInfoScreen
'''

# instanciando a class CryptContext
CRIPTO = CryptContext(schemes=['bcrypt'], deprecated='auto')

def verificar_senha(senha: str, hash_senha: str) -> bool:
    return CRIPTO.verify(senha, hash_senha)


class MainApp(MDApp):
    api = APIClient("http://127.0.0.1:8000")
    api_clientsalas =  APIClientSalas("http://localhost:8000")
    user_token = None  # Variável para armazenar o token do usuário
    user_id = None
    id_sala = None

    def build(self):
        try:
            Builder.load_string(kv)
            self.manager = MDScreenManager()

            # Adiciona as telas ao gerenciador
            self._add_screens()

            return self.manager
        except Exception as e:
            self.show_error_popup("Erro ao construir a interface", str(e))

    def _add_screens(self):
        """ Adiciona todas as telas ao gerenciador de telas """
        screens = [
            LoginScreen(name="login"),
            MainScreen(name="main"),
            InfoScreen(name="info_screen"),
            UserInfoScreen(name='info_user'),
            ResetPasswordScreen(name='reset_senha')
        ]
        for screen in screens:
            self.manager.add_widget(screen)



    async def show_user_info_screen(self):
        """ Exibe informações detalhadas do usuário na tela """
        try:
            user_info_screen = self.root.get_screen('info_user')
            user_info_screen.toggle_show_history()  # Exibe a seção de histórico de salas

            dados = await self.api.fetch_user(self.user_id)
            historicos = await self.api.fetch_historico(self.user_id)

            self._display_user_history(user_info_screen, historicos)
            self._fill_user_info_fields(user_info_screen, dados)

            self.root.current = 'info_user'
        except Exception as e:
            print("Ocorreu um erro:", str(e))

    def _display_user_history(self, user_info_screen, historicos):
        """ Exibe o histórico do usuário na tela """
        if historicos:
            for historico in historicos:
                historico_item = self._create_historico_item(historico)
                user_info_screen.ids.history_layout.add_widget(historico_item)
        else:
            print("Nenhum histórico encontrado para o usuário.")

    def _create_historico_item(self, historico):
        """ Cria um item do histórico de acesso para exibição """
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

        return historico_item

    def _fill_user_info_fields(self, user_info_screen, dados):
        """ Preenche os campos de informações do usuário """
        if dados:
            campos = {
                "nome": user_info_screen.ids.first_name,
                "sobrenome": user_info_screen.ids.second_name,
                "funcao": user_info_screen.ids.funcao_id,
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
        else:
            print("Usuário não encontrado ou sem dados!")

    async def show_info_screen(self, index, name, status):
        # Verifica se o status é True
        if status:
            # Se o status for True, exibe as informações do histórico do usuário
            historico = await self.api_clientsalas.get_historico_user(
                index)  # Supondo que o 'index' seja o 'historico_id'

            if historico:
                # Exibe as informações detalhadas do histórico na tela
                info_screen = self.root.get_screen('info_screen')
                info_screen.ids.info_title.text = f"Histórico de {name}"
                self.id_sala = index
                info_screen.toggle_key_status(True)

                # Passa o histórico como dados para preencher os campos
                self._fill_info_screen_fields(info_screen, historico)

            else:
                # Caso não consiga carregar as informações do histórico
                print("Não foi possível carregar as informações do histórico.")

        else:
            # Se o status for False, exibe as informações do usuário
            print(f"Status é False, exibindo dados de {name}.")

            info_screen = self.root.get_screen('info_screen')
            info_screen.ids.info_title.text = f"{name}"
            self.id_sala = index
            info_screen.toggle_key_status(True)

            # Aqui, vamos buscar os dados do usuário
            dados = await self.api.fetch_user(self.user_id)

            if dados:
                # Passa os dados do usuário para preencher os campos
                self._fill_info_screen_fields(info_screen, dados)

            else:
                # Caso não consiga carregar as informações do usuário
                print("Não foi possível carregar as informações do usuário.")

        # Muda para a tela de informações
        self.root.current = 'info_screen'

    def _fill_info_screen_fields(self, info_screen, dados):
        """ Preenche os campos da tela de informações """
        campos = {
            "nome": info_screen.ids.name_id,
            "funcao": info_screen.ids.funcao,
            "email": info_screen.ids.email_id,
            "telefone": info_screen.ids.phone_id,
        }

        for chave, campo in campos.items():
            campo.text = dados.get(chave, "Não informado")

    async def login(self):
        """ Realiza o login e armazena o token do usuário """
        try:
            email = self.manager.get_screen("login").ids.email.text
            senha = self.manager.get_screen("login").ids.senha.text

            token_info = await self.api.authenticator(email, senha)

            if token_info:
                # Armazena o token e o ID do usuário
                self.user_token = token_info["token"]
                self.user_id = token_info["user_id"]
                self.manager.current = "main"  # Muda para a tela principal
            else:
                self.show_error_popup("Erro", "Credenciais inválidas!")  # Exibe um popup de erro
        except Exception as e:
            self.show_error_popup("Erro ao tentar login", str(e))

    async def register_historico(self):
        """ Registra o histórico de acesso do usuário """
        dados_historico = {
            "sala_id": self.id_sala,
            "usuario_id": self.user_id,
            "data_hora_retirada": datetime.now().isoformat(),
            "data_hora_devolucao": datetime.now().isoformat()
        }

        resposta = await self.api.enviar_historico(dados_historico)
        await self.api_clientsalas.update_sala_status(sala_id=self.id_sala, is_ocupada=True)

        self.refresh_buttons(2)
        if resposta:
            print("Histórico de acesso registrado com sucesso!")
        else:
            print("Erro ao registrar o histórico de acesso.")
            print(f"Erro detalhado: {resposta}")

    def refresh_buttons(self, delay=1):
        """Atualiza os botões após uma alteração no status com um atraso."""
        Clock.schedule_once(self._delayed_refresh, delay)
        self.root.current = 'main'

    def _delayed_refresh(self, *args):
        tela_screen_main = self.root.get_screen('main')
        asyncio.run(tela_screen_main.create_image_buttons())

    async def reset_senha_async(self):
        """ Redefine a senha do usuário """
        password_reset = self.root.get_screen('reset_senha')
        passwords = {
            "email": password_reset.ids.email.text,
            "new_password": password_reset.ids.new_password.text,
            "confirm_password": password_reset.ids.confirm_password.text,
        }

        if passwords["new_password"] == passwords["confirm_password"]:
            try:
                response = await self.api.update_password(passwords["email"], passwords["new_password"])
                if response:
                    print(f"Resposta da API: {response}")
                else:
                    print("Erro ao redefinir a senha.")
            except Exception as e:
                print(f"Erro ao tentar enviar dados para o servidor: {str(e)}")
        else:
            print("As senhas não correspondem.")

    async def save_user_info(self):
        user_info = self.root.get_screen('info_user')

        # Coleta os valores dos campos
        user_data = {
            "nome": user_info.ids.first_name.text,
            "sobrenome": user_info.ids.second_name.text,
            "funcao": user_info.ids.funcao_id.text,
            "email": user_info.ids.email.text,
            "senha": user_info.ids.senha.text,
            "telefone": user_info.ids.phone.text,
            "endereco": self.formatar_endereco(
                logradouro=user_info.ids.address.text,
                bairro=user_info.ids.neighborhood.text,
                numero=user_info.ids.house_number.text,
                cidade=user_info.ids.city.text,
                estado=user_info.ids.state.text
            )
        }

        if user_data["senha"] != user_info.ids.confirme_senha.text.strip():
            self.show_error_popup('Erro', "As senhas não coincidem.")
            return

        try:
            # Chama a API para registrar o usuário
            response = await self.api.register_user_now(user_data)

            # Verifica a resposta da API
            if response:
                self.show_error_popup('Sucesso', "Dados inseridos com sucesso!")
            else:
                self.show_error_popup('Erro', "Erro ao cadastrar usuário. Tente novamente.")

        except Exception as e:
            #print("Erro ao conectar-se com o servidor:", e)
            self.show_error_popup('Erro', f"Erro ao conectar-se com o servidor: {e}")
    async def update_user_info(self):
        """ Atualiza as informações do usuário """
        user_info = self.root.get_screen('info_user')
        endereco_concatenado = self.formatar_endereco(
            logradouro=user_info.ids.address.text,
            bairro=user_info.ids.neighborhood.text,
            numero=user_info.ids.house_number.text,
            cidade=user_info.ids.city.text,
            estado=user_info.ids.state.text
        )

        user_data = {
            "nome": user_info.ids.first_name.text,
            "sobrenome": user_info.ids.second_name.text,
            "funcao": user_info.ids.funcao_id.text,
            "email": user_info.ids.email.text,
            "telefone": user_info.ids.phone.text,
            "endereco": endereco_concatenado,
        }

        result = await self.api.update_usuario(user_id=self.user_id, user_data=user_data)
        await asyncio.sleep(2)  #
        return result

    def show_error_popup(self, title, message):
        """ Exibe um popup de erro """
        popup_content = Label(text=message)
        popup = Popup(title=title, content=popup_content, size_hint=(0.8, 0.4))
        popup.open()




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

    def on_click_info_salas(self, index, name, status):

        """ Exibe informações detalhadas ao clicar em uma sala """
        asyncio.run(self.show_info_screen(index, name, status))
    def on_update_user(self):
        asyncio.run(self.update_user_info())

    def on_login_button_click(self):
        asyncio.run(self.login())

    def on_user_dados(self):
        asyncio.run(self.show_user_info_screen())
    def try_go_back_to_main(self):
        # Função para verificar o login e mudar a tela
        if self.user_token:
            self.root.current = "main"
        else:
            self.root.current = 'login'
            #print("Usuário não está logado. Não pode retornar para a tela principal.")
    def on_click_register_historico(self):
        asyncio.run(self.register_historico())

    def on_save_register_now(self):
        try:
            Clock.schedule_once(lambda dt: self._run_save_user_info())
        except Exception as e:
            self.show_error_popup('Erro', "Tente novamente mais tarde: 422")

    def _run_save_user_info(self):
        asyncio.run(self.save_user_info())

if __name__ == "__main__":

    app = MainApp()
    app.run()
