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
                return

        except ValueError:
            print("O ID do sensor deve ser um número inteiro.")
            return

        try:
            valor = Decimal(valor.replace(",", "."))

        except InvalidOperation:
            print("O valor da medição deve ser um número.")
            return

        medicao = Medicao(
            id_sensor=id_sensor,
            valor=valor
        )

        if MedicaoRepository.inserir(medicao):
            print("\nMedição cadastrada com sucesso!")
            print(f"Sensor: {medicao.id_sensor}")
            print(f"Valor: {medicao.valor}")