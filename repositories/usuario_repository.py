import mysql.connector

from database.conexao import Conexao
from models.usuario import Usuario


class EmailDuplicadoError(Exception):
    """Lançada quando o MySQL recusa um e-mail repetido (UNIQUE)."""


class UsuarioRepository:
    """Todo o SQL da tabela Usuario fica aqui.

    Todas as consultas são PARAMETRIZADAS: o SQL tem marcadores (%s) e os
    valores vão separados, no segundo argumento do execute(). Assim, o que o
    usuário digita é sempre tratado como DADO, nunca como parte do comando SQL.
    """

    @staticmethod
    def inserir(usuario):
        """Insere o usuário e devolve o ID gerado pelo MySQL."""
        conexao = None
        cursor = None
        try:
            conexao = Conexao.conectar()
            cursor = conexao.cursor()

            sql = "INSERT INTO Usuario (nome, email, senha) VALUES (%s, %s, %s)"
            cursor.execute(sql, (usuario.nome, usuario.email, usuario.senha_hash))
            conexao.commit()

            return cursor.lastrowid

        except mysql.connector.Error as erro:
            if conexao is not None:
                conexao.rollback()
            # 1062 = "Duplicate entry" (violou o UNIQUE do e-mail)
            if getattr(erro, "errno", None) == 1062:
                raise EmailDuplicadoError("E-mail já cadastrado.") from erro
            raise

        finally:
            if cursor is not None:
                cursor.close()
            if conexao is not None and conexao.is_connected():
                conexao.close()

    @staticmethod
    def email_existe(email):
        """True se já existe usuário com esse e-mail."""
        conexao = None
        cursor = None
        try:
            conexao = Conexao.conectar()
            cursor = conexao.cursor()

            sql = "SELECT 1 FROM Usuario WHERE email = %s LIMIT 1"
            cursor.execute(sql, (email,))

            return cursor.fetchone() is not None

        finally:
            if cursor is not None:
                cursor.close()
            if conexao is not None and conexao.is_connected():
                conexao.close()

    @staticmethod
    def buscar_por_email(email):
        """Devolve um Usuario (com o hash da senha) ou None se não existir."""
        conexao = None
        cursor = None
        try:
            conexao = Conexao.conectar()
            cursor = conexao.cursor()

            sql = "SELECT idUsuario, nome, email, senha FROM Usuario WHERE email = %s"
            cursor.execute(sql, (email,))
            linha = cursor.fetchone()

            if linha is None:
                return None

            return Usuario(
                id_usuario=linha[0],
                nome=linha[1],
                email=linha[2],
                senha_hash=linha[3],
            )

        finally:
            if cursor is not None:
                cursor.close()
            if conexao is not None and conexao.is_connected():
                conexao.close()

    @staticmethod
    def excluir_por_email(email):
        """Usado só na limpeza dos testes (executar_testes.py)."""
        conexao = None
        cursor = None
        try:
            conexao = Conexao.conectar()
            cursor = conexao.cursor()

            sql = "DELETE FROM Usuario WHERE email = %s"
            cursor.execute(sql, (email,))
            conexao.commit()

        finally:
            if cursor is not None:
                cursor.close()
            if conexao is not None and conexao.is_connected():
                conexao.close()
