class Sensor:
    def __init__(
        self,
        tipo,
        descricao,
        unidade_medida,
        status,
        id_usuario_cadastro,
        id_sensor=None
    ):
        self.id_sensor = id_sensor
        self.tipo = tipo
        self.descricao = descricao
        self.unidade_medida = unidade_medida
        self.status = status
        self.id_usuario_cadastro = id_usuario_cadastro

    def __str__(self):
        return (
            f"Sensor(ID={self.id_sensor}, "
            f"Tipo={self.tipo}, "
            f"Descrição={self.descricao}, "
            f"Unidade={self.unidade_medida}, "
            f"Status={self.status})"
        )