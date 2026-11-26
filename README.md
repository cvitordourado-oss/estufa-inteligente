##Estufa Inteligente - Usuários, Sensores e Medições

Sistema desenvolvido em Python com MySQL para cadastrar usuários, sensores e medições.

- database/conexao.py
- models/usuario.py
- models/sensor.py
- models/medicao.py
- repositories/usuario_repository.py
- repositories/sensor_repository.py
- repositories/medicao_repository.py
- services/sessao.py
- services/auth_service.py
- services/sensor_service.py
- services/medicao_service.py
- main.py
- executar_testes.py
- requirements.txt
- .env.example

## Funcionalidades

### Usuários

- Cadastro de usuário com nome, e-mail e senha.
- Login com limite de cinco tentativas.
- Senha protegida com bcrypt.
- Controle de sessão.

### Sensores

- Cadastro de sensores.
- Listagem dos sensores cadastrados.
- Ativação e desativação de sensores.
- Sensor vinculado ao usuário responsável pelo cadastro.

### Medições

- Cadastro de medições para sensores existentes.
- Validação do ID do sensor.
- Validação de valor vazio ou não numérico.
- Data e hora geradas automaticamente pelo MySQL.
- Histórico completo de medições.

## Banco de dados

O projeto utiliza o banco estufa_inteligente_iot01.

Tabelas utilizadas:

- usuario
- sensor
- medicao

Cada sensor fica vinculado ao usuário que realizou o cadastro. Cada medição fica vinculada ao sensor selecionado.

## Segurança

- Senhas protegidas com bcrypt.
- Consultas parametrizadas contra SQL Injection.
- Tratamento de erros com try, except e finally.
- Credenciais do MySQL armazenadas no arquivo .env.

## Banco de dados

O projeto utiliza o banco estufa_inteligente_iot01.

Tabelas utilizadas:

- usuario
- sensor
- medicao

Cada sensor fica vinculado ao usuário que realizou o cadastro. Cada medição fica vinculada ao sensor selecionado.

## Segurança

- Senhas protegidas com bcrypt.
- Consultas parametrizadas contra SQL Injection.
- Tratamento de erros com try, except e finally.
- Credenciais do MySQL armazenadas no arquivo .env.

## Como executar

1. Crie o banco e as tabelas no MySQL Workbench.
2. Crie o ambiente virtual com: python -m venv .venv
3. Ative o ambiente com: .venv\Scripts\activate
4. Instale as dependências com: pip install -r requirements.txt
5. Configure o arquivo .env com os dados do MySQL.
6. Execute o sistema com: python main.py
7. Execute os testes com: python executar_testes.

## Menu do sistema

Após o login, o sistema apresenta:

1 - Ver meus dados  
2 - Cadastrar sensor  
3 - Listar sensores  
4 - Ativar ou desativar sensor  
5 - Cadastrar medição  
6 - Histórico de medições  
7 - Encerrar sessão  
0 - Sair do programa  

## Tecnologias utilizadas

- Python
- MySQL
- MySQL Connector
- bcrypt
- python-dotenv
- Git
- GitHub
- Visual Studio Code