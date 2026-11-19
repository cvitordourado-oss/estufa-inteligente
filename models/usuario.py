class Usuario:
    """Representa os dados de um usuário do sistema."""

    def __init__(self, nome, email, senha_hash=None, id_usuario=None):
        self.id_usuario = id_usuario    # gerado pelo MySQL (AUTO_INCREMENT)
        self.nome = nome
        self.email = email
        self.senha_hash = senha_hash    # hash do bcrypt, nunca a senha pura

    def dados_publicos(self):
        """Dados que podem ser exibidos (sem o hash da senha)."""
        return {
            "id": self.id_usuario,
            "nome": self.nome,
            "email": self.email,
        }

    def __repr__(self):
        # Não inclui o hash para não vazar em prints/logs
        return f"Usuario(id={self.id_usuario}, nome={self.nome!r}, email={self.email!r})"
