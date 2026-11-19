from models.sensor import Sensor
from repositories.sensor_repository import SensorRepository


class SensorService:

    @staticmethod
    def cadastrar(
        tipo,
        descricao,
        unidade_medida,
        usuario
    ):

        if not tipo.strip():
            print("Tipo é obrigatório.")
            return

        if not descricao.strip():
            print("Descrição é obrigatória.")
            return

        if not unidade_medida.strip():
            print("Unidade de medida é obrigatória.")
            return

        sensor = Sensor(
            tipo=tipo,
            descricao=descricao,
            unidade_medida=unidade_medida,
            status="Ativo",
            id_usuario_cadastro=usuario.id_usuario
        )

        if SensorRepository.inserir(sensor):
            print("\nSensor cadastrado com sucesso!\n")
            print(f"Tipo: {sensor.tipo}")
            print(f"Descrição: {sensor.descricao}")
            print(f"Unidade: {sensor.unidade_medida}")
            print(f"Status: {sensor.status}")
