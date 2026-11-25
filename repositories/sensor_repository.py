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

    @staticmethod
    def listar():
        conexao = None
        cursor = None

        try:
            conexao = Conexao.conectar()
            cursor = conexao.cursor(dictionary=True)

            sql = """
                SELECT
                    idSensor,
                    tipo,
                    descricao,
                    unidadeMedida,
                    statusSensor,
                    id_usuario_cadastro
                FROM sensor
                ORDER BY idSensor
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as erro:
            print(f"Erro ao listar sensores: {erro}")
            return []

        finally:
            if cursor is not None:
                cursor.close()

            if conexao is not None and conexao.is_connected():
                conexao.close()

    @staticmethod
    def alterar_status(id_sensor, novo_status):
        conexao = None
        cursor = None

        try:
            conexao = Conexao.conectar()
            cursor = conexao.cursor()

            sql = """
                UPDATE sensor
                SET statusSensor = %s
                WHERE idSensor = %s
            """

            cursor.execute(sql, (novo_status, id_sensor))
            conexao.commit()

            return cursor.rowcount > 0

        except Exception as erro:
            if conexao is not None:
                conexao.rollback()

            print(f"Erro ao alterar o status do sensor: {erro}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

            if conexao is not None and conexao.is_connected():
                conexao.close()