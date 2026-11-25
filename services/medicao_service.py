from decimal import Decimal, InvalidOperation

from models.medicao import Medicao
from repositories.medicao_repository import MedicaoRepository


class MedicaoService:

    @staticmethod
    def cadastrar(id_sensor, valor):
        try:
            id_sensor = int(id_sensor)

            if id_sensor <= 0:
                print("O ID do sensor deve ser maior que zero.")
                return False

        except ValueError:
            print("O ID do sensor deve ser um número inteiro.")
            return False

        if not MedicaoRepository.sensor_existe(id_sensor):
            print("Sensor não encontrado.")
            return False

        if not valor.strip():
            print("O valor da medição é obrigatório.")
            return False

        try:
            valor = Decimal(valor.replace(",", "."))

        except InvalidOperation:
            print("O valor da medição deve ser numérico.")
            return False

        medicao = Medicao(
            id_sensor=id_sensor,
            valor=valor
        )

        if MedicaoRepository.inserir(medicao):
            print("\nMedição cadastrada com sucesso!")
            print(f"Sensor selecionado: {medicao.id_sensor}")
            print(f"Valor registrado: {medicao.valor}")
            return True

        return False

    @staticmethod
    def listar():
        medicoes = MedicaoRepository.listar()

        print("\n--- Histórico de medições ---")

        if not medicoes:
            print("Nenhuma medição cadastrada.")
            return

        for medicao in medicoes:
            print("\n----------------------------")
            print(f"ID da medição: {medicao['idMedicao']}")
            print(f"ID do sensor: {medicao['id_Sensor']}")
            print(f"Tipo: {medicao['tipo']}")
            print(f"Descrição: {medicao['descricao']}")
            print(f"Data e hora: {medicao['dataHora']}")
            print(
                f"Valor: {medicao['valor']} "
                f"{medicao['unidadeMedida']}"
            )

        print("\n----------------------------")