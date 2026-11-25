from models.sensor import Sensor
from repositories.sensor_repository import SensorRepository


class SensorService:

    @staticmethod
    def cadastrar(tipo, descricao, unidade_medida, usuario):

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
            print("\nSensor cadastrado com sucesso!")
            print(f"Tipo: {sensor.tipo}")
            print(f"Descrição: {sensor.descricao}")
            print(f"Unidade: {sensor.unidade_medida}")
            print(f"Status: {sensor.status}")

    @staticmethod
    def listar():
        sensores = SensorRepository.listar()

        print("\n--- Sensores cadastrados ---")

        if not sensores:
            print("Nenhum sensor cadastrado.")
            return

        for sensor in sensores:
            status = "Ativo" if sensor["statusSensor"] == 1 else "Inativo"

            print("\n----------------------------")
            print(f"ID: {sensor['idSensor']}")
            print(f"Tipo: {sensor['tipo']}")
            print(f"Descrição: {sensor['descricao']}")
            print(f"Unidade: {sensor['unidadeMedida']}")
            print(f"Status: {status}")
            print(
                f"Cadastrado pelo usuário: "
                f"{sensor['id_usuario_cadastro']}"
            )

        print("\n----------------------------")

    @staticmethod
    def alterar_status(id_sensor, opcao_status):

        try:
            id_sensor = int(id_sensor)
        except ValueError:
            print("O ID do sensor deve ser um número.")
            return

        if id_sensor <= 0:
            print("O ID do sensor deve ser maior que zero.")
            return

        if opcao_status == "1":
            novo_status = 1
            nome_status = "Ativo"

        elif opcao_status == "2":
            novo_status = 0
            nome_status = "Inativo"

        else:
            print("Opção de status inválida.")
            return

        alterado = SensorRepository.alterar_status(
            id_sensor,
            novo_status
        )

        if alterado:
            print(
                f"Sensor {id_sensor} alterado para "
                f"{nome_status} com sucesso!"
            )
        else:
            print("Sensor não encontrado ou o status já era o escolhido.")