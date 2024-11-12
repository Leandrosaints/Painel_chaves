import asyncio
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
            if response:

                return response.json()  # Retorna o JSON com o histórico criado
            else:
                print(f"Erro ao enviar histórico: {response.status_code}, {response.text}")
                return None  # Caso de erro, retorna None

    async def fetch_historico(self, user_historico_id: int):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/api/v1/usuarios/historicos/{user_historico_id}")

            if response.status_code == 200:
                historico_data = response.json()  # Converte a resposta para JSON

                # Verificar se a resposta é uma lista
                if isinstance(historico_data, list):
                    historicos = []
                    for h in historico_data:
                        sala_nome = h.get('sala_nome', 'Nome da sala não encontrado')
                        usuario_nome = h.get('usuario_nome', 'Nome do usuário não encontrado')
                        data_hora_entrada = h.get('data_hora_retirada', 'Data de entrada não disponível')
                        data_hora_saida = h.get('data_hora_devolucao', 'Data de saída não disponível')

                        historicos.append({
                            "sala_nome": sala_nome,
                            "usuario_nome": usuario_nome,
                            "entrada": data_hora_entrada,
                            "saida": data_hora_saida
                        })

                    return historicos

            elif response.status_code == 404:
                print(f"Histórico com ID {user_historico_id} não encontrado!")
            else:
                print(f"Erro ao buscar histórico: {response.text}")

    async def update_usuario(self, user_id: int, user_data: dict):
        # Define a URL com o ID do usuário a ser atualizado
        url = f"{self.base_url}/api/v1/usuarios/{user_id}"
        async with httpx.AsyncClient() as client:
            # Envia a requisição PUT com os dados do usuário
            response = await client.patch(url, json=user_data)
            # Verifica o status da resposta
            if response.status_code == 202:
                # Retorna os dados atualizados
                return response.json()
            elif response.status_code == 404:
                # Lida com caso de usuário não encontrado
                print("Usuário não encontrado.")
                return None
            else:
                # Lida com outros possíveis erros
                print(f"Erro ao atualizar usuário: {response.status_code}")
                return None

    async def update_password(self, email: str, new_password: str):
        # Define a URL com o endpoint correto
        url = f"{self.base_url}/api/v1/usuarios/reset-password"

        # Dados a serem enviados no corpo da requisição
        user_data = {
            "email": email,
            "senha": new_password  # Certifique-se de que o campo é "senha" no lado do servidor
        }

        # Envia a requisição POST com os dados de redefinição de senha
        async with httpx.AsyncClient() as client:
            response = await client.patch(url, json=user_data)

            # Verifica o status da resposta
            if response.status_code == 200:
                # Retorna a resposta com a confirmação de sucesso
                return response.json()
            elif response.status_code == 404:
                print("Usuário não encontrado.")
                return None
            elif response.status_code == 400:
                print("Dados inválidos. Verifique o email ou a senha.")
                return None
            elif response.status_code == 422:
                print("Erro 422: Dados inválidos, verifique os requisitos da API.")
                print(f"Detalhes do erro: {response.json()}")  # Exibe detalhes do erro retornado pela API
                return None
            else:
                print(f"Erro ao redefinir senha: {response.status_code}")
                return None

class APIClientSalas:
    def __init__(self, base_url):
        self.base_url = base_url

    async def get_salas(self):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/v1/salas/salas")
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

                # Contar o número de salas
                total_salas = len(salas)
                print(f"Total de salas: {total_salas}")

                return resultado  # Retorna a lista de dicionários com os detalhes das salas

        except httpx.RequestError as e:
            print(f"Erro ao acessar a API: {e}")
            return None

    async def update_sala_status(self, sala_id: int, is_ocupada: bool):
        try:
            async with httpx.AsyncClient() as client:
                # Monta o corpo da requisição para atualizar o status
                payload = {"is_ocupada": is_ocupada}
                response = await client.patch(
                    f"{self.base_url}/api/v1/salas/{sala_id}", json=payload
                )
                response.raise_for_status()

                # Retorna a resposta como um dicionário JSON
                return response.json()

        except httpx.RequestError as e:
            print(f"Erro ao acessar a API: {e}")
            return None

    async def get_historico_user(self, historico_id: int):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/v1/historicos/historicos/{historico_id}")
                response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx

                # Supondo que a resposta seja uma lista ou dicionário
                historico = response.json()
                #print(historico)
                # Se for uma lista, pega o primeiro item
                if isinstance(historico, list) and historico:
                    historico = historico[0]

                # Agora verificamos se a chave 'usuario_funcao' existe antes de acessá-la
                resultado = {
                    "user_id": historico.get("usuario_id"),
                    "nome": historico.get("nome", "Nome não disponível"),
                    # Se não encontrar, retorna "Nome não disponível"
                    "funcao": historico.get("funcao", "Função não disponível"),
                    # Se não encontrar, retorna "Função não disponível"
                    "email": historico.get("email", "Email não disponível"),
                    "telefone": historico.get("telefone", "Telefone não disponível"),
                    "data_hora_retirada": historico.get("data_hora_retirada", "Data não disponível"),
                    "data_hora_devolucao": historico.get("data_hora_devolucao", "Data não disponível")
                }

                return resultado

        except httpx.RequestError as e:
            print(f"Erro ao acessar a API: {e}")
        return None


async def main():
    api_client = APIClientSalas("http://localhost:8000")  # Altere para a URL correta da sua API
    salas = await api_client.get_salas()
    if salas is not None:
        for sala in salas:
            print(f"Número: {sala['numero']}, Nome: {sala['nome']}, Ocupada: {sala['is_ocupada']}")

# Executar o teste
if __name__ == "__main__":
    asyncio.run(main())