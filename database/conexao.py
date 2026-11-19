import os
import mysql.connector
from dotenv import load_dotenv

# Lê o arquivo .env e coloca as variáveis no ambiente (os.getenv)
load_dotenv()


class Conexao:

    @staticmethod
    def conectar():
        """Abre e devolve uma conexão com o MySQL usando os dados do .env."""
        host = os.getenv("DB_HOST")
        porta = os.getenv("DB_PORT")
        usuario = os.getenv("DB_USER")
        senha = os.getenv("DB_PASSWORD")
        banco = os.getenv("DB_NAME")

        # Verifica se as configurações obrigatórias existem
        if not all([host, porta, usuario, banco]):
            raise ValueError("Verifique as configurações do arquivo .env")

        conexao = mysql.connector.connect(
            host=host,
            port=int(porta),
            user=usuario,
            password=senha,
            database=banco
        )

        # Devolve a conexão (o objeto), não a classe
        return conexao


# Teste rápido: só roda quando este arquivo é executado diretamente
# (python -m database.conexao). Ao ser importado por outros arquivos, não executa.
if __name__ == "__main__":
    conexao = None
    try:
        conexao = Conexao.conectar()

        if conexao.is_connected():
            print("Conexão realizada com sucesso!")

    except (ValueError, mysql.connector.Error) as erro:
        print(f"Erro ao conectar com o MySQL: {erro}")

    finally:
        if conexao is not None and conexao.is_connected():
            conexao.close()
            print("Conexão encerrada")
