✅ Resumo técnico do projeto (Documentação)
- 📌 Conversation-CHAT

# Chat em Tempo Real com FastAPI e WebSocket

# 🧰 Tecnologias Utilizadas
- Backend:

- Python 3.x

- FastAPI

- WebSocket (via FastAPI)

- SQLite com SQLAlchemy para persistência de mensagens e usuários

# Frontend:

- HTML5

- CSS3 (estilização customizada)

- JavaScript (puro, sem frameworks)

# Outras bibliotecas:

- Font Awesome para ícones

- Fetch API para comunicação com backend REST

## 📦 Funcionalidades Implementadas
- Sistema de login e registro de usuários

- Tela de chat em tempo real, usando WebSocket

- Exibição do nome do usuário e status de online

- Lista de mensagens históricas puxadas via requisição REST

- Envio e recebimento de mensagens instantâneas

- Armazenamento das mensagens no banco de dados SQLite

- Interface visual com cores personalizadas e responsiva

- Botão de logout funcional que limpa os dados da sessão local (LocalStorage)


## 🚀 Funcionalidades

- ✅ Registro e login de usuários
- ✅ Envio e recebimento de mensagens em tempo real
- ✅ Interface moderna e amigável
- ✅ Histórico de mensagens
- ✅ Logout e segurança básica com LocalStorage

## 🧰 Tecnologias Usadas

### Backend:
- [Python](https://www.python.org/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSockets_API) via FastAPI
- [SQLite](https://www.sqlite.org/index.html) com SQLAlchemy

### Frontend:
- HTML5
- CSS3
- JavaScript
- Font Awesome (ícones)

## 📦 Como rodar o projeto

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   cd seu-repo
   ```
- Crie um ambiente virtual e ative:

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
``` 
- Instale as dependências:

```bash

pip install fastapi uvicorn sqlalchemy
Execute o servidor:
```

```bash

uvicorn main:app --reload
Abra o navegador e acesse:

http://127.0.0.1:8000
```

## 👤 Usuários e Sessão
- O sistema usa LocalStorage para manter a sessão do usuário (ID e nome).

- A navbar mostra o status do usuário logado.

- Ao clicar em "Sair", a sessão é encerrada e o usuário é redirecionado.

## 📁 Estrutura do Projeto (exemplo)
```cpp

.
├── backend/
│   ├── main.py
│   ├── models.py
│   ├── database.py
│   └── ...
├── templates/
│   └── chat.html...
└── README.md
```

## 📝 Considerações Finais
- Este projeto é ideal para quem quer aprender como integrar FastAPI com WebSocket em um projeto real e funcional. Ele também pode servir como base para sistemas maiores, como chats privados, suporte online ou integrações com bots.

- Sinta-se à vontade para melhorar, adaptar ou contribuir com sugestões!

💡 Desenvolvido por [@Devmoises79] 🙌

