# Estufa Inteligente — Login e Gerenciamento de Sessão

Atividade em Python com MySQL: cadastro de usuários, login com senha protegida por
bcrypt, consultas parametrizadas (proteção contra SQL Injection) e controle de sessão
em um menu de terminal.

## Estrutura do projeto

```
estufa/
├── database/
│   └── conexao.py                  # Conexao.conectar() — lê o .env e abre a conexão
├── models/
│   └── usuario.py                  # classe Usuario
├── repositories/
│   └── usuario_repository.py       # todo o SQL (parametrizado) da tabela Usuario
├── services/
│   ├── sessao.py                   # classe Sessao
│   └── auth_service.py             # regras de cadastro/login, bcrypt, limite de 5 tentativas
├── main.py                         # menu interativo
├── executar_testes.py              # testes da Etapa 5
├── requirements.txt
└── .env.example
```

## Como executar

1. Crie o banco e as tabelas no MySQL Workbench (script SQL da atividade).
2. Crie e ative o ambiente virtual, depois instale as dependências:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Copie `.env.example` para `.env` e preencha com os seus dados do MySQL.
4. Teste a conexão: `python -m database.conexao`
5. Rode o sistema: `python main.py`
6. Rode os testes: `python executar_testes.py`

## Regras implementadas

**Cadastro**
- Todos os campos são obrigatórios (nome, e-mail, senha); e-mail com formato válido.
- O ID não é pedido: é gerado pelo MySQL (`AUTO_INCREMENT`).
- E-mail duplicado é recusado (checagem na aplicação + `UNIQUE` no banco).
- A senha é guardada como hash bcrypt; a senha pura nunca vai para o banco.
- Se os dados forem inválidos, o sistema mostra o problema e pede os dados novamente.
- Cadastro com sucesso inicia a sessão automaticamente.

**Login**
- E-mail e senha; o usuário é buscado no banco e a senha conferida com `bcrypt.checkpw`.
- Máximo de 5 tentativas; depois disso volta ao menu inicial.
- Mensagem igual para "e-mail inexistente" e "senha errada", para não revelar quais e-mails existem.

**Sessão**
- `Sessao` inicia, verifica, recupera o usuário atual e encerra.
- A opção "Encerrar sessão" só aparece no menu quando há usuário autenticado.
- A sessão guarda o usuário sem o hash da senha.

## Conceitos

**1. Try, Except e Finally**
`try` contém o código que pode falhar (conectar ao banco, executar SQL). `except` trata o
erro em vez de deixar o programa quebrar (ex.: `.env` incompleto, MySQL desligado, e-mail
duplicado). `finally` roda **sempre**, com ou sem erro; aqui serve para fechar o cursor e a
conexão, evitando conexões abertas.

**2. @staticmethod**
Marca um método que pertence à classe, não a um objeto: não recebe `self` e é chamado
direto, sem instanciar (`Conexao.conectar()`, `UsuarioRepository.inserir(...)`,
`AuthService.gerar_hash(...)`). Foi usado nos métodos que não dependem de estado de objeto.

**3. SQL Injection e como prevenir**
Ataque em que o usuário digita trechos de SQL (`' OR '1'='1`) em um campo e, se o programa
monta o comando concatenando texto, esse trecho passa a fazer parte do comando e altera
seu significado (ex.: entrar sem senha, apagar tabelas). Prevenção: **consultas
parametrizadas** — `cursor.execute("... WHERE email = %s", (email,))`. O SQL e os valores
viajam separados e o banco trata o que foi digitado sempre como dado, nunca como comando.

**4. Função do bcrypt**
Biblioteca de hash de senhas. Gera um hash de mão única (não dá para voltar à senha), com
**salt** aleatório embutido (duas senhas iguais geram hashes diferentes) e **custo ajustável**
(é propositalmente lento, o que dificulta ataques de força bruta). No cadastro usa-se
`bcrypt.hashpw`; no login, `bcrypt.checkpw` compara a senha digitada com o hash guardado.

## Testes (Etapa 5)

`python executar_testes.py` cobre: cadastro completo, campos vazios, e-mail duplicado,
senha gravada como hash, login correto e incorreto, limite de 5 tentativas, encerramento
de sessão e tentativas de SQL Injection (a estrutura das consultas não é alterada e a
tabela continua intacta). Os usuários de teste são apagados no final.
