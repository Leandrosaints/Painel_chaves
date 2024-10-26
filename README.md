# Painel de chave

Este projeto é uma aplicação simples desenvolvida utilizando a biblioteca Kivy e KivyMD. A aplicação apresenta uma interface gráfica com um menu de navegação, permitindo a troca entre diferentes telas.

## Funcionalidades

- **Navegação:** A aplicação possui um menu lateral que permite ao usuário navegar entre três telas diferentes.
- **Botões Rotacionáveis:** Cada tela contém botões que podem ser rotacionados ao serem clicados.
- **ScrollView:** A primeira tela utiliza um `ScrollView` para permitir a rolagem quando o número de botões excede a altura da tela.
- **Limitação de Tamanho da Janela:** A janela da aplicação possui tamanhos mínimo e máximo definidos, evitando que o usuário redimensione a janela para além desses limites.

## Estrutura do Código

O código está dividido em partes principais:

1. **Imports:** Importa as bibliotecas necessárias do Kivy e KivyMD.
2. **Definições de Janela:** Define o tamanho inicial, mínimo e máximo da janela.
3. **Interface em KV:** Define a interface do usuário utilizando a linguagem KV, que descreve a estrutura da aplicação.
4. **Classes:**
   - `RotatableButton`: Classe que representa um botão que pode ser rotacionado.
   - `MainScreen`: Classe que gerencia a tela principal e os botões contidos nela.
   - `MyApp`: Classe principal que inicia a aplicação.

## Como Executar

Para executar a aplicação, siga os passos abaixo:

1. **Clone o repositório:**
   ```bash
   git clone <URL do repositório>
   cd <diretório do repositório>
