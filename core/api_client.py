import httpx

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def authenticator(self, username: str, password: str):
        url = f"{self.base_url}/api/v1/usuarios/login"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data={"username": username, "password": password})

            if response.status_code == 200:
                return response.json()  # Retorna o token de acesso
            else:
                print(f"Erro: {response.json()}")
                return None

    async def get_data(self, endpoint):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/{endpoint}")
                response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx
                return response.json()
        except httpx.RequestError as e:
            print(f"Erro ao acessar a API: {e}")
            return None
