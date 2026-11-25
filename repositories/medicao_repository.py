from database.conexao import Conexao


class MedicaoRepository:

    @staticmethod
    def inserir(medicao):
        conexao = None
        cursor = None

        try:
            conexao = Conexao.conectar()
            cursor = conexao.cursor()

            sql = """
                INSERT INTO medicao
                    (id_Sensor, valor)
                VALUES (%s, %s)
            """

            valores = (
                medicao.id_sensor,
                medicao.valor
            )

            cursor.execute(sql, valores)
            conexao.commit()

            return True

        except Exception as erro:
            if conexao is not None:
                conexao.rollback()

            print(f"Erro ao cadastrar medição: {erro}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

            if conexao is not None and conexao.is_connected():
                conexao.close()