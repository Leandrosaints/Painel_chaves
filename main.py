import re
from datetime import datetime
import time
from threading import Thread

from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.image import Image
from kivymd.uix.button import MDFlatButton, MDRoundFlatIconButton
from kivymd.uix.dialog import MDDialog
from passlib.context import CryptContext
from kivy.lang import Builder
from kivy.metrics import dp
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.popup import Popup
from kivy.uix.label import Label

from Loading import LoadingOverlay
from login import LoginScreen
from gestor import MainScreen  # Importar telas
from infoScreen import InfoScreen
from screen_history import HistoryScreen
from info_user import UserInfoScreen
from redefinir_senha import ResetPasswordScreen
from api_client import APIClient, APIClientSalas

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

    user_token = None  # Variável para armazenar o token do usuário
    user_id = None
    id_sala = None
    show_history_user = False#controla widgets da info_iuser
    last_activity_time =time.time()  # Armazena o horário da última atividade do usuário
    inactivity_event = None
    dialog = None


    def build(self):
        try:
            self.api = APIClient("http://127.0.0.1:8000")
            self.api_clientsalas = APIClientSalas("http://127.0.0.1:8000")
            Builder.load_string(kv)
            self.manager = MDScreenManager()

            # Adiciona as telas ao gerenciador
            self._add_screens()
            self.on_start()
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
            ResetPasswordScreen(name='reset_senha'),
            HistoryScreen(name='screen_history')

        ]
        for screen in screens:
            self.manager.add_widget(screen)

    def show_user_info_screen(self):
        """ Exibe informações detalhadas do usuário na tela """

        if self.user_token:
            # Inicia o overlay de carregamento
            self.loading_overlay = LoadingOverlay()
            self.loading_overlay.open()

            user_info_screen = self.root.get_screen('info_user')

            # Função para buscar e exibir informações do usuário
            def fetch_user_info(dt):
                dados = self.api.fetch_user(self.user_id, self.user_token)
                historicos = self.api.fetch_historico(self.user_id, self.user_token)

                user_info_screen.toggle_show_history(self.show_history_user)
                #self._display_user_history(user_info_screen, historicos)
                self._fill_user_info_fields(user_info_screen, dados)

                # Fecha o overlay de carregamento após as informações serem carregadas
                self.loading_overlay.dismiss()

                # Exibe a tela de informações do usuário
                self.root.current = 'info_user'

            # Inicia a operação de busca de informações do usuário
            Clock.schedule_once(fetch_user_info, 0)
        else:
            self.show_history_user = False

    def _display_user_history(self):#ver tela de historico de sala dos user
        self.screen_history = self.root.get_screen('screen_history')
        if self.user_token:
            # Inicia o overlay de carregamento
            self.loading_overlay = LoadingOverlay()
            self.loading_overlay.open()

            #user_info_screen = self.root.get_screen('info_user')

            # Função para buscar e exibir informações do usuário

        #dados = self.api.fetch_user(self.user_id, self.user_token)
        historicos = self.api.fetch_historico(self.user_id, self.user_token)
        """ Exibe o histórico do usuário na tela """
        if historicos:
            for historico in historicos:
                historico_item = self._create_historico_item(historico)
                self.screen_history.ids.history_layout.add_widget(historico_item)
                self.root.current = 'screen_history'
                self.loading_overlay.dismiss()

        else:

            self.show_error_popup('atenção',"Nenhum histórico encontrado para o usuário.")

            self.root.current = 'screen_history'
            self.button_reload_history()
            self.loading_overlay.dismiss()
    def button_reload_history(self):
        """Exibe uma imagem de erro e um botão para recarregar."""
        self.screen_history.ids.history_layout.clear_widgets()

        # Adiciona a imagem de erro
        self.error_image = Image(
            source='src/history_anim.png',
            size_hint=(1, None),
            height=dp(100),
            opacity=0  # Inicialmente invisível
        )
        self.screen_history.ids.history_layout.add_widget(self.error_image)

        # Iniciar animação após um curto atraso
        Clock.schedule_once(self.start_animation, 0.5)

        # Rótulo de mensagem
        name_label = Label(
            text='Hummm, parece que não há histórico.',
            size_hint=(1, None),
            height=dp(18),
            halign='center',
            color=(0, 0, 0, 1)
        )
        name_label.bind(size=name_label.setter('text_size'))
        self.screen_history.ids.history_layout.add_widget(name_label)

        # Adiciona o botão de recarregar
        reload_button = MDRoundFlatIconButton(
            text="Recarregar",
            size_hint=(1, None),
            height=dp(50),
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            icon="refresh"
        )
        reload_button.bind(on_release=lambda btn: self._display_user_history())
        self.screen_history.ids.history_layout.add_widget(reload_button)

    def start_animation(self, dt):
        # Animação de subir e descer levemente
        entry_anim = Animation(opacity=1, duration=1.2, t='out_cubic') + \
                     Animation(y=self.error_image.y + dp(10), duration=0.6, t='in_out_sine') + \
                     Animation(y=self.error_image.y, duration=0.6, t='in_out_sine')

        entry_anim.repeat = True  # Faz a animação repetir indefinidamente
        entry_anim.start(self.error_image)

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
            self.show_error_popup('Atenção',"Usuário não encontrado ou sem dados!")


    def show_info_screen(self, index, name, status):
        info_screen = self.root.get_screen('info_screen')
        self.id_sala = index

        # Inicia o overlay de carregamento
        self.loading_overlay = LoadingOverlay()
        self.loading_overlay.open()

        # Atualiza o título da tela de informações
        info_screen.ids.info_title.text = f"{name}"

        # Função para atualizar a tela de informações
        def update_info_screen(dt):

            try:
                # Tenta buscar o histórico do usuário
                historico = self.api_clientsalas.get_historico_user(index, self.user_token)
                print(historico)

                # Determina o ID do usuário do histórico ou usa o usuário atual
                user_id_historico = historico.get("user_id", self.user_id) if historico else self.user_id

                # Atualiza o status dos botões com base no status e histórico
                info_screen.toggle_key_status(status, user_id_historico, self.user_id)

                if status:

                    # Se a chave está ocupada, exibe o histórico
                    if historico:
                        self._fill_info_screen_fields(info_screen, historico)
                    else:
                        self.show_error_popup('Atenção', 'Não foi possível carregar as informações do histórico.')
                else:

                    # Se a chave está disponível ou o histórico for inexistente, usa dados do usuário atual
                    dados = self.api.fetch_user(self.user_id, self.user_token)
                    if dados:
                        self._fill_info_screen_fields(info_screen, dados)
                    else:
                        self.show_error_popup('Atenção', 'Não foi possível carregar as informações do usuário.')

            except Exception as e:
                self.show_error_popup('Erro', f'Erro ao buscar informações: {str(e)}')

            # Fecha o overlay de carregamento após as operações
            self.loading_overlay.dismiss()

            # Exibe a tela de informações
            self.root.current = 'info_screen'

        # Inicia a atualização da tela de informações após um pequeno atraso
        Clock.schedule_once(update_info_screen, 0)

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

    def login(self):
        """Realiza o login e exibe a tela de loading"""
        try:
            # Exibir overlay de carregamento
            self.loading_overlay = LoadingOverlay()
            self.loading_overlay.open()

            # Processar login em segundo plano
            def process_login():
                try:
                    # Obter dados de login
                    email = self.manager.get_screen("login").ids.email.text
                    senha = self.manager.get_screen("login").ids.senha.text

                    # Chamar a API
                    token_info = self.api.authenticator(email, senha)

                    if token_info:
                        # Atualizar informações do usuário
                        self.user_token = token_info["token"]
                        self.user_id = token_info["user_id"]
                        self.show_history_user = True

                        # Redirecionar para a tela principal
                        Clock.schedule_once(lambda dt: setattr(self.manager, "current", "main"), 0)
                    else:
                        # Exibir erro de credenciais inválidas
                        Clock.schedule_once(lambda dt: self.show_error_popup("Erro", "Credenciais inválidas"), 0)
                except Exception as ex:
                    # Capturar mensagem de erro
                    error_message = str(ex)
                    Clock.schedule_once(lambda dt: self.show_error_popup("Erro ao tentar login", error_message), 0)
                finally:
                    # Fechar overlay de carregamento
                    Clock.schedule_once(lambda dt: self.loading_overlay.dismiss(), 0)

            # Executar o processo em um thread separado
            Thread(target=process_login).start()

        except Exception as ex:
            # Exibir erro inesperado
            self.show_error_popup("Erro inesperado", str(ex))

    def logout(self):

        result = self.api.logout(self.user_token)
        if result:
            self.user_token = None
            self.user_id = None
            self.show_history_user = False
            user_info_screen = self.root.get_screen('info_user')
            user_info_screen.toggle_show_history(self.show_history_user)

            self.root.current = 'login'

    def register_historico(self, status):
        """ Registra o histórico de acesso do usuário """

        self.api_clientsalas.update_sala_status(sala_id=self.id_sala, is_ocupada=status)

        if status:
            dados_historico = {
                "numero_chave": self.id_sala,
                "usuario_id": self.user_id,
                "data_hora_retirada": datetime.now().isoformat(),

            }

            resposta = self.api.enviar_historico(dados_historico, self.user_token)


            if resposta:
                self.show_error_popup('Sucesso', "Histórico de acesso registrado com sucesso!")
            else:
                self.show_error_popup('Erro', "Erro ao registrar o histórico de acesso.")
            self.refresh_buttons()
        else:
            self.api_clientsalas.update_historico_devolucao(self.id_sala, self.user_id, self.user_token)
            self.refresh_buttons()

    def refresh_buttons(self, delay=1):
        """Atualiza os botões após uma alteração no status com um atraso."""
        Clock.schedule_once(self._delayed_refresh, delay)
        self.root.current = 'main'

    def _delayed_refresh(self, *args):
        tela_screen_main = self.root.get_screen('main')
        tela_screen_main.reload_salas()


    def reset_senha(self):
        """ Redefine a senha do usuário """
        password_reset = self.root.get_screen('reset_senha')
        passwords = {
            "email": password_reset.ids.email.text,
            "new_password": password_reset.ids.new_password.text,
            "confirm_password": password_reset.ids.confirm_password.text,
        }

        if passwords["new_password"] == passwords["confirm_password"]:
            try:
                response = self.api.update_password(passwords["email"], passwords["new_password"])
                if response:
                    self.show_error_popup('Sucesso',f"Response: {response}")
                else:
                    self.show_error_popup('Erro',"Erro ao redefinir a senha.")
            except Exception as e:
                self.show_error_popup('atenção',f"Erro ao tentar enviar dados para o servidor: {str(e)}")
        else:
            self.show_error_popup('Atenção',"As senhas não correspondem.")

    def save_user_info(self):
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
            response = self.api.register_user_now(user_data)

            # Verifica a resposta da API
            if response:
                self.show_error_popup('Sucesso', "Dados inseridos com sucesso!")
                self.root.current = 'login'
            else:
                self.show_error_popup('Erro', "Erro ao cadastrar usuário. Tente novamente.")

        except Exception as e:

            self.show_error_popup('Erro', f"Erro ao conectar-se com o servidor: {e}")
    def update_user_info(self):
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

        result = self.api.update_usuario(user_id=self.user_id, user_data=user_data, token=self.user_token)
        if result:
            self.show_error_popup('Sucesso', 'Dados atualizados')

            self.root.current = 'main'
            return result
        else:
            self.show_error_popup('Erro', 'Erro ao salvar dados contacte os responsaveis!')
    def show_error_popup(self, title, message):
        """Exibe um MDDialog com título e mensagem"""
        if not self.dialog:
            self.dialog = MDDialog(
                title=title,
                text=message,
                buttons=[
                    MDFlatButton(
                        text="OK",
                        on_release=self.close_dialog
                    )
                ],
            )
        else:
            # Atualiza o texto e título do diálogo existente
            self.dialog.title = title
            self.dialog.text = message

        self.dialog.open()

    def close_dialog(self, *args):
        """Fecha o diálogo"""
        if self.dialog:
            self.dialog.dismiss()
            self.dialog = None



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

    #def on_click_info_salas(self, index, name, status):

        #""" Exibe informações detalhadas ao clicar em uma sala """
        #self.show_info_screen(index, name, status)
    def on_update_user(self):
        self.update_user_info()

    def on_login_button_click(self):
        self.login()


    def try_go_back_to_main(self):
        # Função para verificar o login e mudar a tela
        if self.user_token:
            self.root.current = "main"
        else:
            self.root.current = 'login'

    def go_to_info_user_clean(self):
        # Obtém a referência da tela info_user
        info_user_screen = self.root.get_screen('info_user')

        # Limpa os campos individuais
        info_user_screen.ids.first_name.text = ""
        info_user_screen.ids.second_name.text = ""
        info_user_screen.ids.funcao_id.text = ""
        info_user_screen.ids.email.text = ""
        info_user_screen.ids.senha.text = ""
        info_user_screen.ids.phone.text = ""
        info_user_screen.ids.address.text = ""
        info_user_screen.ids.neighborhood.text = ""
        info_user_screen.ids.house_number.text = ""
        info_user_screen.ids.city.text = ""
        info_user_screen.ids.state.text = ""

        #info_user_screen.ids.history_layout.clear_widgets()
        # Alterar para a tela info_user
        self.root.current = 'info_user'
        #info_user_screen.ids.show_history = False

    def on_click_register_historico(self, status):#trabalhando aqui implementaçao do passar o status
        self.register_historico(status)

    def on_save_register_now(self):
        try:
            Clock.schedule_once(lambda dt: self.save_user_info())
        except Exception as e:
            self.show_error_popup('Erro', "Tente novamente mais tarde: 422")

    #def _run_save_user_info(self):


    def on_logout(self):

        self.logout()

        if self.root.current == 'login':
            self.manager.get_screen("login").ids.email.text = ''
            self.manager.get_screen("login").ids.senha.text = ''
    def on_start(self):

        # Inicie o monitoramento de inatividade quando o aplicativo for iniciado
        self.reset_inactivity_timer()
        Window.bind(on_touch_down=self.on_user_activity)

    def on_stop(self):
        # Pare o monitoramento de inatividade ao encerrar o app
        if self.inactivity_event:
            self.inactivity_event.cancel()

    def on_pause(self):
        # Pause o monitoramento quando o app estiver em pausa
        if self.inactivity_event:
            self.inactivity_event.cancel()
        return True

    def on_resume(self):
        # Retome o monitoramento ao retornar do modo de pausa
        self.reset_inactivity_timer()

    def reset_inactivity_timer(self, *args):
        """Reinicia o temporizador de inatividade."""
        self.last_activity_time = time.time()

        # Cancela o evento anterior, se houver
        if self.inactivity_event:
            self.inactivity_event.cancel()

        # Agenda o monitoramento de inatividade para acontecer a cada segundo
        self.inactivity_event = Clock.schedule_interval(self.check_inactivity, 600)

    def on_user_activity(self, *args):
        """Reseta o temporizador de inatividade ao detectar qualquer atividade do usuário."""
        self.reset_inactivity_timer()

    def check_inactivity(self, dt):
        """Verifica o tempo de inatividade e desloga o usuário se o limite for atingido."""
        current_time = time.time()
        if current_time - self.last_activity_time > 10:
            self.on_logout()

if __name__ == "__main__":

    app = MainApp()
    app.run()
