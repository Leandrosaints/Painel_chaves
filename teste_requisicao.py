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


'''async def protected_request(token: str):
    url = "http://127.0.0.1:8000/api/v1/protected_route"  # Exemplo de rota protegida
    headers = {"Authorization": f"Bearer {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            return response.json()  # Retorna os dados da rota protegida
        else:
            print(f"Erro: {response.json()}")
            return None'''


async def main():
    username = "le@gmail.com"
    password = "123"
    token_info = await login(username, password)

    if token_info:
        print("Login bem-sucedido!", token_info)
        access_token = token_info["acess_token"]  # Corrigido aqui
        # Aqui você pode chamar a função protected_request, se necessário
    else:
        print("Falha no login.")


# Executa a função principal
if __name__ == "__main__":
    asyncio.run(main())
