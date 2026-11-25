class Medicao:
    def __init__(
        self,
        id_sensor,
        valor,
        id_medicao=None,
        data_hora=None
    ):
        self.id_medicao = id_medicao
        self.id_sensor = id_sensor
        self.valor = valor
        self.data_hora = data_hora