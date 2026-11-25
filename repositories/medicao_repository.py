from database.conexao import Conexao


class MedicaoRepository:

    @staticmethod
    def sensor_existe(id_sensor):
        conexao = None
        cursor = None

        try:
            conexao = Conexao.conectar()
            cursor = conexao.cursor()

            sql = """
                SELECT idSensor
                FROM sensor
                WHERE idSensor = %s
            """

            cursor.execute(sql, (id_sensor,))

            return cursor.fetchone() is not None

        except Exception as erro:
            print(f"Erro ao verificar o sensor: {erro}")
            return False

        finally:
            if cursor is not None:
                cursor.close()

            if conexao is not None and conexao.is_connected():
                conexao.close()

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

    @staticmethod
    def listar():
        conexao = None
        cursor = None

        try:
            conexao = Conexao.conectar()
            cursor = conexao.cursor(dictionary=True)

            sql = """
                SELECT
                    m.idMedicao,
                    m.id_Sensor,
                    s.tipo,
                    s.descricao,
                    s.unidadeMedida,
                    m.dataHora,
                    m.valor
                FROM medicao AS m
                INNER JOIN sensor AS s
                    ON s.idSensor = m.id_Sensor
                ORDER BY m.dataHora DESC
            """

            cursor.execute(sql)

            return cursor.fetchall()

        except Exception as erro:
            print(f"Erro ao listar medições: {erro}")
            return []

        finally:
            if cursor is not None:
                cursor.close()

            if conexao is not None and conexao.is_connected():
                conexao.close()