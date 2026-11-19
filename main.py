from getpass import getpass

from services.sessao import Sessao
from services.auth_service import AuthService, MAX_TENTATIVAS


def exibir_menu(sessao):
    """O menu muda conforme exista (ou não) um usuário autenticado."""
    if sessao.existe_sessao():
        usuario = sessao.usuario_atual()
        print(f"\n=== Estufa Inteligente | logado como {usuario.nome} ===")
        print("1 - Ver meus dados")
        print("2 - Encerrar sessão")
        print("0 - Sair do programa")
    else:
        print("\n=== Estufa Inteligente ===")
        print("1 - Cadastrar usuário")
        print("2 - Realizar login")
        print("0 - Sair do programa")


def fluxo_cadastro(auth):
    print("\n--- Cadastro de usuário ---")
    while True:
        nome = input("Nome: ")
        email = input("E-mail: ")
        senha = getpass("Senha: ")

        sucesso, mensagem = auth.cadastrar(nome, email, senha)
        print(mensagem)

        if sucesso:
            return

        # Dados inválidos: informa o problema e pede os dados de novo
        if input("Deseja tentar novamente? (s/n): ").strip().lower() != "s":
            return


def fluxo_login(auth):
    print("\n--- Login ---")
    auth.reiniciar_tentativas()

    while not auth.bloqueado():
        email = input("E-mail: ")
        senha = getpass("Senha: ")

        sucesso, mensagem = auth.login(email, senha)
        print(mensagem)

        if sucesso:
            return

    print(f"Você errou {MAX_TENTATIVAS} vezes. Voltando ao menu inicial.")
    auth.reiniciar_tentativas()


def mostrar_dados(sessao):
    usuario = sessao.usuario_atual()
    print("\n--- Meus dados ---")
    print(f"ID:     {usuario.id_usuario}")
    print(f"Nome:   {usuario.nome}")
    print(f"E-mail: {usuario.email}")


def encerrar_sessao(sessao):
    # Etapa 4: verifica -> encerra -> limpa os dados -> volta ao menu inicial
    if not sessao.existe_sessao():
        print("Não há sessão ativa.")
        return

    nome = sessao.usuario_atual().nome
    sessao.encerrar()
    print(f"Sessão de {nome} encerrada. Voltando ao menu inicial.")


def main():
    sessao = Sessao()
    auth = AuthService(sessao)

    while True:
        exibir_menu(sessao)
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "0":
            print("Até logo!")
            break

        if sessao.existe_sessao():
            if opcao == "1":
                mostrar_dados(sessao)
            elif opcao == "2":
                encerrar_sessao(sessao)
            else:
                print("Opção inválida.")
        else:
            if opcao == "1":
                fluxo_cadastro(auth)
            elif opcao == "2":
                fluxo_login(auth)
            else:
                print("Opção inválida.")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")
