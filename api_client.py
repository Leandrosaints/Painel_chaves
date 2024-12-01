import asyncio
from datetime import datetime
from typing import Optional

#import httpx
import requests
import logging

# Configuração básica do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Usando logging em vez de print
#logging.debug("Este é um log de depuração.")  # Será mostrado apenas se o nível for DEBUG
#logging.info("Este é um log informativo.")    # Será mostrado sempre
#logging.warning("Este é um aviso.")
#logging.error("Este é um erro.")
#logging.critical("Este é um erro crítico.")

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    #Metodo que faz uma requisao no metodo get da api realizando o login retonando o token e id
    def authenticator(self, username: str, password: str):
        url = f"{self.base_url}/api/v1/usuarios/login"
        try:
            response = requests.post(url, data={"username": username, "password": password})

            if response.status_code == 200:
                data = response.json()
                return {
                    "token": data.get("acess_token"),
                    "user_id": data.get("user_id")
                }
            else:
                return None
        except requests.RequestException as e:
            #print(f"Erro na requisição: {e}")
            logging.error(f"Erro ao executar requisção. {e}")
            return None
    #METODO que faz requisicao no metodo post e retona os dado do usuarios filtrado pelo ID

    def logout(self, token: str):
        try:
            headers = {"Authorization": f"Bearer {token}"}
            response = requests.post(f"{self.base_url}/api/v1/usuarios/logout", headers=headers)
            response.raise_for_status()

            # Retorna a resposta como um dicionário JSON
            return response.json()

        except requests.RequestException as e:
            # Log de erro, se necessário
            logging.error(f"Erro ao acessar a API: {e}")

            return None

    def fetch_user(self, user_id: int, token):
        try:
            headers = {
                "Authorization": f"Bearer {token}"  # Adiciona o token no cabeçalho
            }
            response = requests.get(f"{self.base_url}/api/v1/usuarios/{user_id}", headers=headers)

            if response.status_code == 200:
                user_data = response.json()

                return user_data
            elif response.status_code == 403:
                logging.info("Você não tem permissão para acessar os dados deste usuário.")
            elif response.status_code == 404:
                logging.info("Usuário não encontrado!")
            else:
                logging.error("Erro ao buscar usuário:", response.text)
            return None
        except requests.RequestException as e:
            # Log de erro, se necessário
            logging.error(f"Erro ao acessar a API: {e}")
            return None
    def register_user_now(self, user_data: dict):
        url = f"{self.base_url}/api/v1/usuarios/register"

        try:
            # Requisição POST para registrar o usuário
            response = requests.post(url, json=user_data)

            # Verifica se o status da resposta é 201 (Criado)
            if response.status_code == 201:
                # Retorna os dados do usuário registrado em formato JSON
                data = response.json()
                return data
            else:
                # Se houver erro, captura a mensagem de erro do servidor
                error_message = response.json().get("detail", "Erro desconhecido")
                raise Exception(f"Erro ao registrar usuário: {error_message}")

        except requests.RequestException as e:
            # Captura qualquer erro de requisição, como problemas de rede
            raise Exception(f"Erro ao registrar usuário: {e}")

    '''def get_data(self, endpoint):
        try:
            async with httpx.AsyncClient() as client:
                response = client.get(f"{self.base_url}/{endpoint}")
                response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx
                return response.json()
        except httpx.RequestError as e:
            pass
            #print(f"Erro ao acessar a API: {e}")
            return None'''



    ########### requisicoes de historico de salas #########

    def enviar_historico(self, data_historico: dict, token) -> Optional[dict]:
        #url = f"{self.base_url}/api/v1/historicos/register"

        try:
            headers = {
                "Authorization": f"Bearer {token}"  # Adiciona o token no cabeçalho
            }
            # Enviar os dados recebidos em formato JSON
            response = requests.post(f"{self.base_url}/api/v1/historicos/register", json=data_historico, headers=headers)
            response.raise_for_status()

            # Verificar a resposta e retornar o resultado
            return response.json() if response.ok else None
        except requests.RequestException as e:
            # Log de erro, se necessário
            logging.error(f"Erro ao enviar histórico: {e}")
            return None

    def fetch_historico(self, user_historico_id: int, token):
        try:
            headers = {
                "Authorization": f"Bearer {token}"  # Adiciona o token no cabeçalho
            }
            response = requests.get(
                f"{self.base_url}/api/v1/usuarios/historicos/{user_historico_id}",
                headers=headers
            )
            response.raise_for_status()

            if response.status_code == 200:
                historico_data = response.json()  # Converte a resposta para JSON

                # Ajuste para trabalhar diretamente com a lista retornada
                if isinstance(historico_data, list):
                    historicos = []
                    for h in historico_data:
                        sala_nome = h.get('sala_nome', 'Nome da sala não encontrado')
                        data_hora_entrada = h.get('data_hora_retirada', 'Data de entrada não disponível')
                        data_hora_saida = h.get('data_hora_devolucao', 'Data de saída não disponível')

                        historicos.append({
                            "sala_nome": sala_nome,
                            "entrada": data_hora_entrada,
                            "saida": data_hora_saida
                        })
                    return historicos
                else:
                    logging.debug(f"Estrutura inesperada na resposta da API: {historico_data}")
                    return None

            elif response.status_code == 404:
                logging.debug(f"Histórico com ID {user_historico_id} não encontrado!")
            else:
                logging.error(f"Erro ao buscar histórico: {response.text}")
            return None

        except requests.RequestException as e:
            logging.error(f"Erro ao acessar a API: {e}")
            return None

    def update_usuario(self, user_id: int, user_data: dict, token) -> Optional[dict]:

        # Define a URL com o ID do usuário a ser atualizado


        try:
            headers = {
                "Authorization": f"Bearer {token}"  # Adiciona o token no cabeçalho
            }
            # Envia a requisição PATCH com os dados do usuário
            response = requests.patch(f"{self.base_url}/api/v1/usuarios/{user_id}", json=user_data, headers=headers)
            response.raise_for_status()  # Gera uma exceção se a resposta tiver um status de erro

            # Verifica o status da resposta
            if response.status_code == 202:
                # Retorna os dados atualizados
                return response.json()
            elif response.status_code == 404:
                logging.info("Usuário não encontrado.")
                return None
            else:
                logging.error(f"Erro ao atualizar usuário: {response.status_code}")
                return None
        except requests.RequestException as e:
            logging.error(f"Erro ao tentar atualizar usuário: {e}")
            return None

    def update_password(self, email: str, new_password: str) -> Optional[dict]:
        # Define a URL com o endpoint correto
        url = f"{self.base_url}/api/v1/usuarios/reset-password"

        # Dados a serem enviados no corpo da requisição
        user_data = {
            "email": email,
            "senha": new_password  # Certifique-se de que o campo é "senha" no lado do servidor
        }

        try:
            # Envia a requisição PATCH com os dados de redefinição de senha
            response = requests.patch(url, json=user_data)
            response.raise_for_status()  # Gera uma exceção se a resposta tiver um status de erro

            # Verifica o status da resposta
            if response.status_code == 200:
                return response.json()  # Retorna a resposta com a confirmação de sucesso
            elif response.status_code == 404:
                logging.info("Usuário não encontrado.")
                return None
            elif response.status_code == 400:
                logging.info("Dados inválidos. Verifique o email ou a senha.")
                return None
            elif response.status_code == 422:
                logging.error(f"Dados inválidos, verifique os requisitos da API.{response.json()}")
                #(f"Detalhes do erro: {response.json()}")  # Exibe detalhes do erro retornado pela API
                return None
            else:
                logging.error(f"Erro ao redefinir senha: {response.status_code}")
                return None
        except requests.RequestException as e:
            logging.error(f"Erro ao tentar redefinir a senha: {e}")
            return None

class APIClientSalas:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_salas(self) -> Optional[list]:
        try:

            # Realiza uma requisição GET para obter as salas
            response = requests.get(f"{self.base_url}/api/v1/salas/salas")
            response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx

            # Supondo que a resposta seja uma lista de salas
            salas = response.json()

            # Processar as salas para obter o número, o nome e o valor 'is_ocupada'
            resultado = []
            for sala in salas:
                resultado.append({
                    "numero": sala["numero_chave"],  # Substitua "numero" pelo campo correto no seu modelo
                    "nome": sala["nome"],  # Substitua "nome" pelo campo correto no seu modelo
                    "is_ocupada": sala["is_ocupada"]  # Substitua "is_ocupada" pelo campo correto no seu modelo
                })

            # Retorna a lista de dicionários com os detalhes das salas
            return resultado

        except requests.RequestException as e:
            logging.error(f"Erro ao acessar a API: {e}")
            return None

    def update_sala_status(self, sala_id: int, is_ocupada: bool) -> Optional[dict]:
        try:

            # Monta o corpo da requisição para atualizar o status
            payload = {"is_ocupada": is_ocupada}
            # Realiza a requisição PATCH de forma síncrona
            response = requests.patch(
                f"{self.base_url}/api/v1/salas/{sala_id}", json=payload
            )
            response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx

            # Retorna a resposta como um dicionário JSON
            return response.json()

        except requests.RequestException as e:
            logging.error(f"Erro ao acessar a API: {e}")
            return None

    def update_historico_devolucao(self, room_id: int, user_id: int, token) -> Optional[dict]:
        """
        Atualiza o campo data_hora_devolucao de um registro específico no histórico de acesso.
        A data e hora são registradas automaticamente pelo servidor.

        Parameters:
            room_id (int): O ID da sala
            user_id (int): O ID do usuário
        """
        try:
            headers = {
                "Authorization": f"Bearer {token}"  # Adiciona o token no cabeçalho
            }
            # Requisição PATCH para atualizar o campo de devolução com base no `room_id` e `user_id`
            response = requests.patch(
                f"{self.base_url}/api/v1/historicos/historico/devolver/{room_id}/{user_id}", headers=headers
            )
            response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx

            # Retorna a resposta como um dicionário JSON
            return response.json()

        except requests.RequestException as e:
            # Caso ocorra erro na requisição
            logging.error(f"Erro ao acessar a API: {e}")
            return None
    def get_historico_user(self, historico_id: int, token) -> Optional[dict]:
        try:
            headers = {
                "Authorization": f"Bearer {token}"  # Adiciona o token no cabeçalho
            }
            # Requisição GET para obter o histórico de um usuário com base no ID
            response = requests.get(f"{self.base_url}/api/v1/historicos/historicos/{historico_id}", headers=headers)
            response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx

            # Converte a resposta para JSON
            historico = response.json()

            # Se for uma lista, pega o primeiro item
            if isinstance(historico, list) and historico:
                historico = historico[0]

            # Verifica a existência de chaves e retorna o resultado desejado
            resultado = {
                "user_id": historico.get("usuario_id"),
                "nome": historico.get("nome", "Nome não disponível"),
                "funcao": historico.get("funcao", "Função não disponível"),
                "email": historico.get("email", "Email não disponível"),
                "telefone": historico.get("telefone", "Telefone não disponível"),
                "data_hora_retirada": historico.get("data_hora_retirada", "Data não disponível"),
            }

            return resultado

        except requests.RequestException as e:
            # Caso ocorra erro na requisição
            logging.error(f"Erro ao acessar a API 333: {e}")
            return None


'''async def main():
    api_client = APIClientSalas("http://localhost:8000")  # Altere para a URL correta da sua API
    salas = await api_client.get_salas()
    if salas is not None:
        for sala in salas:
            print(f"Número: {sala['numero']}, Nome: {sala['nome']}, Ocupada: {sala['is_ocupada']}")
'''
