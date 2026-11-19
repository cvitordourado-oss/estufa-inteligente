import re

import bcrypt
import mysql.connector

from models.usuario import Usuario
from repositories.usuario_repository import UsuarioRepository, EmailDuplicadoError

MAX_TENTATIVAS = 5
TAMANHO_MIN_SENHA = 6
TAMANHO_MAX_SENHA_BYTES = 72   # limite do bcrypt

PADRAO_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class AuthService:
    """Regras de negócio de cadastro e login."""

    def __init__(self, sessao):
        self.sessao = sessao
        self._tentativas = 0

    # ------------------------------------------------------------------
    # Senha (bcrypt)
    # ------------------------------------------------------------------
    @staticmethod
    def gerar_hash(senha):
        """Transforma a senha em hash bcrypt (o salt já vai dentro do hash)."""
        hash_bytes = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())
        return hash_bytes.decode("utf-8")

    @staticmethod
    def verificar_senha(senha, hash_armazenado):
        """Compara a senha digitada com o hash guardado no banco."""
        try:
            return bcrypt.checkpw(
                senha.encode("utf-8"),
                hash_armazenado.encode("utf-8"),
            )
        except ValueError:
            # hash malformado no banco: trata como senha incorreta
            return False

    # ------------------------------------------------------------------
    # Validação do cadastro
    # ------------------------------------------------------------------
    @staticmethod
    def validar_cadastro(nome, email, senha):
        """Devolve a lista de problemas encontrados (vazia = tudo certo)."""
        erros = []

        if not nome:
            erros.append("O nome é obrigatório.")
        elif len(nome) > 50:
            erros.append("O nome deve ter no máximo 50 caracteres.")

        if not email:
            erros.append("O e-mail é obrigatório.")
        elif len(email) > 100:
            erros.append("O e-mail deve ter no máximo 100 caracteres.")
        elif not PADRAO_EMAIL.match(email):
            erros.append("O e-mail informado está em formato inválido.")

        if not senha:
            erros.append("A senha é obrigatória.")
        elif len(senha) < TAMANHO_MIN_SENHA:
            erros.append(f"A senha deve ter no mínimo {TAMANHO_MIN_SENHA} caracteres.")
        elif len(senha.encode("utf-8")) > TAMANHO_MAX_SENHA_BYTES:
            erros.append("A senha é muito longa (máximo de 72 bytes).")

        return erros

    # ------------------------------------------------------------------
    # Cadastro
    # ------------------------------------------------------------------
    def cadastrar(self, nome, email, senha):
        """Cadastra o usuário e inicia a sessão.

        Devolve (sucesso, mensagem).
        """
        nome = nome.strip()
        email = email.strip().lower()

        erros = self.validar_cadastro(nome, email, senha)
        if erros:
            return False, "\n".join(erros)

        try:
            if UsuarioRepository.email_existe(email):
                return False, "Este e-mail já está cadastrado."

            usuario = Usuario(nome=nome, email=email, senha_hash=self.gerar_hash(senha))
            usuario.id_usuario = UsuarioRepository.inserir(usuario)

        except EmailDuplicadoError:
            # Dois cadastros ao mesmo tempo: o UNIQUE do banco é a última barreira
            return False, "Este e-mail já está cadastrado."
        except (mysql.connector.Error, ValueError) as erro:
            return False, f"Erro ao acessar o banco de dados: {erro}"

        self.sessao.iniciar(usuario)
        return True, f"Cadastro realizado com sucesso! Bem-vindo(a), {usuario.nome}."

    # ------------------------------------------------------------------
    # Login (máximo de 5 tentativas)
    # ------------------------------------------------------------------
    def bloqueado(self):
        return self._tentativas >= MAX_TENTATIVAS

    def tentativas_restantes(self):
        return MAX_TENTATIVAS - self._tentativas

    def reiniciar_tentativas(self):
        self._tentativas = 0

    def _registrar_falha(self, mensagem):
        self._tentativas += 1
        if self.bloqueado():
            return False, f"{mensagem}\nLimite de {MAX_TENTATIVAS} tentativas atingido."
        return False, f"{mensagem}\nTentativas restantes: {self.tentativas_restantes()}."

    def login(self, email, senha):
        """Autentica por e-mail e senha. Devolve (sucesso, mensagem)."""
        if self.bloqueado():
            return False, f"Limite de {MAX_TENTATIVAS} tentativas atingido."

        email = email.strip().lower()

        try:
            usuario = UsuarioRepository.buscar_por_email(email)
        except (mysql.connector.Error, ValueError) as erro:
            return self._registrar_falha(f"Erro ao acessar o banco de dados: {erro}")

        # Mesma mensagem para "e-mail não existe" e "senha errada":
        # assim ninguém descobre quais e-mails estão cadastrados.
        if usuario is None or not self.verificar_senha(senha, usuario.senha_hash):
            return self._registrar_falha("E-mail ou senha incorretos.")

        self.reiniciar_tentativas()
        self.sessao.iniciar(usuario)
        return True, f"Login realizado com sucesso! Bem-vindo(a), {usuario.nome}."
