from datetime import datetime
from typing import Optional

import httpx

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    #Metodo que faz uma requisao no metodo get da api realizando o login retonando o token e id
    async def authenticator(self, username: str, password: str):
        url = f"{self.base_url}/api/v1/usuarios/login"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data={"username": username, "password": password})

            if response.status_code == 200:

                data = response.json()
                return {
                    "token": data.get("acess_token"),
                    "user_id": data.get("user_id")
                }
            else:
                return None
    #METODO que faz requisicao no metodo post e retona os dado do usuarios filtrado pelo ID
    async def fetch_user(self, user_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/v1/usuarios/{user_id}")

            if response.status_code == 200:
                user_data = response.json()
                return user_data
            elif response.status_code == 404:
                print("Usuário não encontrado!")
            else:
                print("Erro ao buscar usuário:", response.text)

    async def register_user_now(self, user_data):
        url = f"{self.base_url}/api/v1/usuarios/register"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=user_data)

            if response.status_code == 201:
                # Supondo que o registro foi bem-sucedido e o servidor retorna os dados do usuário registrado
                data = response.json()
                return data
            else:
                # Tratar o erro e obter a mensagem de erro do servidor, se houver
                error_message = response.json().get("detail", "Erro desconhecido")
                raise Exception(f"Erro ao registrar usuário: {error_message}")

    async def get_data(self, endpoint):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/{endpoint}")
                response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx
                return response.json()
        except httpx.RequestError as e:
            print(f"Erro ao acessar a API: {e}")
            return None



    ########### requisicoes de historico de salas #########

    async def enviar_historico(self, data_historico: dict) -> Optional[dict]:
        url = f"{self.base_url}/api/v1/historicos/register"

        # Enviar os dados recebidos em formato JSON
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=data_historico)

            # Verificar a resposta e retornar o resultado
            if response.status_code == 201:
                return response.json()  # Retorna o JSON com o histórico criado
            else:
                print(f"Erro ao enviar histórico: {response.status_code}, {response.text}")
                return None  # Caso de erro, retorna None
