from models.usuario import Usuario


class Sessao:
    """Guarda quem está logado no programa (em memória)."""

    def __init__(self):
        self._usuario = None

    def iniciar(self, usuario):
        """Inicia a sessão com o usuário autenticado.

        Guardamos uma cópia SEM o hash da senha: a sessão não precisa dele.
        """
        self._usuario = Usuario(
            nome=usuario.nome,
            email=usuario.email,
            id_usuario=usuario.id_usuario,
        )

    def existe_sessao(self):
        """True se há um usuário autenticado."""
        return self._usuario is not None

    def usuario_atual(self):
        """Devolve o usuário conectado (ou None)."""
        return self._usuario

    def encerrar(self):
        """Encerra a sessão e limpa os dados do usuário.

        Devolve True se havia sessão ativa, False se não havia.
        """
        if not self.existe_sessao():
            return False

        self._usuario = None
        return True
