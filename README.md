# Estufa Inteligente - Usuários, Sensores e Medições

Sistema desenvolvido em Python com MySQL para cadastrar usuários, sensores e medições.

## Estrutura do Projeto

O projeto está organizado seguindo uma arquitetura em camadas, separando modelos, serviços, repositórios e conexão com o banco de dados.

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

O sistema utiliza Programação Orientada a Objetos (POO), persistência de 
dados em MySQL e uma arquitetura baseada em camadas para facilitar a manutenção e organização do código.

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

Os sensores podem ser cadastrados apenas por usuários autenticados. Cada sensor possui um tipo, uma descrição, uma unidade de medida e um status que pode ser alterado entre ativo e inativo.

### Medições

- Cadastro de medições para sensores existentes.
- Validação do ID do sensor.
- Validação de valor vazio ou não numérico.
- Data e hora geradas automaticamente pelo MySQL.
- Histórico completo de medições.

Cada medição é associada a um sensor existente. O sistema verifica se o sensor informado existe antes de registrar a medição no banco de dados.

As medições são armazenadas com data e hora automáticas geradas pelo MySQL, permitindo o acompanhamento histórico dos dados coletados.

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

As senhas não são armazenadas em texto puro. O bcrypt gera um hash seguro para cada senha cadastrada. Além disso, consultas parametrizadas impedem a execução de comandos SQL maliciosos enviados pelos usuários.

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

As tecnologias foram escolhidas para aplicar conceitos de Programação Orientada a Objetos, persistência de dados, segurança da informação, organização em camadas e integração entre Python e MySQL.

## Testes Automatizados

O projeto possui um arquivo chamado executar_testes.py responsável por validar automaticamente as principais funcionalidades do sistema.

Os testes verificam:

- Cadastro de usuários.
- Campos obrigatórios.
- Login com credenciais válidas.
- Login com credenciais inválidas.
- Limite de tentativas de login.
- Encerramento de sessão.
- Proteção contra SQL Injection.
- Cadastro de sensores.
- Alteração de status dos sensores.
- Cadastro de medições.
- Histórico de medições.
- Associação correta entre sensores e medições.
- Criação automática de IDs pelo MySQL.
- Registro automático de data e hora das medições.

Para executar os testes:

python executar_testes.py

## Autor

Projeto desenvolvido por Caio Vitor Dourado para fins acadêmicos, aplicando conceitos de Python, MySQL, autenticação de usuários, gerenciamento de sensores, registro de medições e boas práticas de desenvolvimento de software.