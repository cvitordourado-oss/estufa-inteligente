"""Testes da Etapa 5 — rodam contra o MySQL real configurado no .env.

Uso (na pasta do projeto, com o ambiente virtual ativo):
    python executar_testes.py

Os usuários criados aqui têm e-mails aleatórios (teste_xxxxxxxx@estufa.com)
e são apagados no final.
"""
import sys
import uuid

import bcrypt

from repositories.usuario_repository import UsuarioRepository
from services.auth_service import AuthService, MAX_TENTATIVAS
from services.sessao import Sessao

resultados = []


def verificar(descricao, condicao, detalhe=""):
    status = "PASSOU" if condicao else "FALHOU"
    resultados.append(condicao)
    linha = f"[{status}] {descricao}"
    if detalhe:
        linha += f"\n         -> {detalhe}"
    print(linha)


def novo_servico():
    sessao = Sessao()
    return sessao, AuthService(sessao)


def executar():
    sufixo = uuid.uuid4().hex[:8]
    email = f"teste_{sufixo}@estufa.com"
    email_injecao = f"injecao_{sufixo}@estufa.com"
    senha = "Senha@123"
    criados = [email, email_injecao]

    try:
        # 1. Cadastro com todos os dados preenchidos
        sessao, auth = novo_servico()
        ok, msg = auth.cadastrar("Usuário de Teste", email, senha)
        verificar("1. Cadastrar usuário com todos os dados", ok, msg)
        verificar("1b. Sessão iniciada automaticamente após o cadastro", sessao.existe_sessao())

        salvo = UsuarioRepository.buscar_por_email(email)
        verificar(
            "1c. Dados gravados no banco com ID gerado pelo MySQL",
            salvo is not None and isinstance(salvo.id_usuario, int) and salvo.id_usuario > 0,
            f"ID = {salvo.id_usuario if salvo else None}",
        )

        # 2. Cadastro com campos vazios
        casos_vazios = {
            "nome vazio": ("", f"vazio1_{sufixo}@estufa.com", senha),
            "e-mail vazio": ("Fulano", "", senha),
            "senha vazia": ("Fulano", f"vazio2_{sufixo}@estufa.com", ""),
            "todos vazios": ("", "", ""),
        }
        for nome_caso, (n, e, s) in casos_vazios.items():
            sessao, auth = novo_servico()
            ok, msg = auth.cadastrar(n, e, s)
            verificar(
                f"2. Cadastro recusado com {nome_caso}",
                (not ok) and (not sessao.existe_sessao()),
                msg.replace("\n", " | "),
            )

        # 3. E-mail já existente
        sessao, auth = novo_servico()
        ok, msg = auth.cadastrar("Outra Pessoa", email, "outraSenha1")
        verificar("3. Cadastro recusado com e-mail já existente", (not ok) and (not sessao.existe_sessao()), msg)

        # 4. Senha armazenada como hash
        hash_salvo = salvo.senha_hash
        verificar("4. Senha gravada NÃO é a senha pura", hash_salvo != senha)
        verificar("4b. Valor gravado tem formato bcrypt ($2b$...)", hash_salvo.startswith("$2"), hash_salvo[:20] + "...")
        verificar(
            "4c. bcrypt.checkpw confirma que o hash corresponde à senha",
            bcrypt.checkpw(senha.encode("utf-8"), hash_salvo.encode("utf-8")),
        )

        # 5. Login com credenciais corretas
        sessao, auth = novo_servico()
        ok, msg = auth.login(email, senha)
        verificar("5. Login com credenciais corretas", ok and sessao.existe_sessao(), msg)

        # 6. Login com senha incorreta
        sessao, auth = novo_servico()
        ok, msg = auth.login(email, "senhaErrada")
        verificar("6. Login com senha incorreta é recusado", (not ok) and (not sessao.existe_sessao()), msg.replace("\n", " | "))

        # 7. Limite de 5 tentativas
        sessao, auth = novo_servico()
        for _ in range(MAX_TENTATIVAS):
            auth.login(email, "senhaErrada")
        verificar(f"7. Bloqueio após {MAX_TENTATIVAS} tentativas erradas", auth.bloqueado())
        ok, msg = auth.login(email, senha)  # agora com a senha CERTA
        verificar(
            "7b. Depois do limite, nem a senha correta entra",
            (not ok) and (not sessao.existe_sessao()),
            msg,
        )

        # 8. Encerrar sessão
        sessao, auth = novo_servico()
        auth.login(email, senha)
        encerrou = sessao.encerrar()
        verificar(
            "8. Encerrar sessão limpa os dados do usuário",
            encerrou and (not sessao.existe_sessao()) and sessao.usuario_atual() is None,
        )
        verificar("8b. Encerrar sem sessão ativa devolve False", sessao.encerrar() is False)

        # 9. SQL Injection
        payloads = [
            "' OR '1'='1",
            "' OR 1=1 --",
            "admin'--",
            f"{email}' --",
            "x'; DROP TABLE Usuario; --",
        ]
        for payload in payloads:
            sessao, auth = novo_servico()
            ok_a, _ = auth.login(payload, payload)         # injeção no e-mail e na senha
            sessao2, auth2 = novo_servico()
            ok_b, _ = auth2.login(email, payload)          # e-mail real, senha maliciosa
            verificar(
                f"9. Login com payload {payload!r} é recusado",
                (not ok_a) and (not ok_b) and (not sessao.existe_sessao()) and (not sessao2.existe_sessao()),
            )

        verificar(
            "9b. Tabela Usuario continua existindo e intacta após os ataques",
            UsuarioRepository.email_existe(email),
        )

        # 9c. Aspas e SQL dentro de um campo de cadastro viram TEXTO, não comando
        nome_malicioso = "Robert'); DROP TABLE Usuario;--"
        sessao, auth = novo_servico()
        ok, msg = auth.cadastrar(nome_malicioso, email_injecao, senha)
        guardado = UsuarioRepository.buscar_por_email(email_injecao)
        verificar(
            "9c. Nome com SQL é gravado como texto literal (e a tabela sobrevive)",
            ok and guardado is not None and guardado.nome == nome_malicioso
            and UsuarioRepository.email_existe(email),
            msg,
        )

    finally:
        for e in criados:
            try:
                UsuarioRepository.excluir_por_email(e)
            except Exception as erro:  # limpeza nunca deve esconder o resultado
                print(f"(aviso) não consegui apagar {e}: {erro}")

    total = len(resultados)
    passou = sum(resultados)
    print(f"\nResultado: {passou}/{total} verificações passaram.")
    return passou == total


if __name__ == "__main__":
    sys.exit(0 if executar() else 1)
