# Estufa Inteligente - Login, Sessão e Cadastro de Sensores

Descrição do projeto aqui.

## Estrutura do projeto
```text
estufa/
├── database/
│   └── conexao.py
├── models/
│   ├── usuario.py
│   └── sensor.py
├── repositories/
│   ├── usuario_repository.py
│   └── sensor_repository.py
├── services/
│   ├── sessao.py
│   ├── auth_service.py
│   └── sensor_service.py
├── main.py
├── executar_testes.py
├── requirements.txt
└── .env.example


## Como executar

1. Crie o banco no MySQL Workbench.
2. Instale as dependências.
3. Execute o sistema.

## Cadastro de usuários

- O usuário informa nome, e-mail e senha.
- A senha é protegida com bcrypt.

## Login e sessão

- O usuário possui cinco tentativas.
- O menu muda após o login.

## Cadastro de sensores

- Somente usuários logados podem cadastrar sensores.
- Os sensores são armazenados no MySQL.
- Cada sensor fica vinculado ao usuário que fez o cadastro.

## Segurança

- Bcrypt para proteger senhas.
- Consultas parametrizadas contra SQL Injection.
- Try, except e finally para tratamento de erros.

## Testes

Execute:

python executar_testes.py
