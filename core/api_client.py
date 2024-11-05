import httpx

class APIClient:
    def __init__(self, base_url):
        self.base_url = base_url

    async def authenticator(self, username: str, password: str):
        url = f"{self.base_url}/api/v1/usuarios/login"
        async with httpx.AsyncClient() as client:
            response = await client.post(url, data={"username": username, "password": password})

            if response.status_code == 200:
                # Agora, sem usar "await", pois `response.json()` já retorna um dicionário.
                data = response.json()
                return {
                    "token": data.get("acess_token"),
                    "user_id": data.get("user_id")
                }
            else:
                return None

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
    async def get_data(self, endpoint):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/{endpoint}")
                response.raise_for_status()  # Levanta um erro para códigos de status 4xx/5xx
                return response.json()
        except httpx.RequestError as e:
            print(f"Erro ao acessar a API: {e}")
            return None
