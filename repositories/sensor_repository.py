from database.conexao import Conexao


class SensorRepository:

    @staticmethod
    def inserir(sensor):
        conexao = None
        cursor = None

        try:
            conexao = Conexao.conectar()
            cursor = conexao.cursor()

            sql = """
                INSERT INTO sensor
                    (
                        tipo,
                        descricao,
                        unidadeMedida,
                        statusSensor,
                        id_usuario_cadastro
                    )
                VALUES (%s, %s, %s, %s, %s)
            """

            valores = (
                sensor.tipo,
                sensor.descricao,
                sensor.unidade_medida,
                1,
                sensor.id_usuario_cadastro
            )

            cursor.execute(sql, valores)
            conexao.commit()

            return True

        except Exception as erro:
            if conexao is not None:
                conexao.rollback()

            print(f"Erro ao cadastrar sensor: {erro}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

            if conexao is not None and conexao.is_connected():
                conexao.close()