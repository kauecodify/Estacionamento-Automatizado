import tkinter as tk
from datetime import datetime, timedelta

class VagaEstacionamento:
    def __init__(self, numero, carro=None):
        self.numero = numero
        self.carro = carro
        self.inicio = None

class EstacionamentoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Estacionamento App")

        self.vagas_estacionamento = [VagaEstacionamento(numero=i+1) for i in range(4)]
        self.valor_por_segundo = 0.000001  # Valor inicial em reais por segundo (com 6 casas decimais)
        self.total_pago = 0

        self.criar_widgets()
        self.atualizar_cronometros()

    def criar_widgets(self):
        self.frame_vagas = tk.Frame(self.root)
        self.frame_vagas.pack(padx=10, pady=10)

        self.labels_vagas = []
        for vaga in self.vagas_estacionamento:
            label_vaga = tk.Label(self.frame_vagas, text=f"Vaga {vaga.numero}: Livre")
            label_vaga.pack()
            self.labels_vagas.append(label_vaga)

        self.frame_controles = tk.Frame(self.root)
        self.frame_controles.pack(padx=10, pady=10)

        self.label_placa = tk.Label(self.frame_controles, text="Placa do Carro:")
        self.label_placa.pack(side=tk.LEFT)

        self.entry_placa = tk.Entry(self.frame_controles)
        self.entry_placa.pack(side=tk.LEFT)

        self.label_modelo = tk.Label(self.frame_controles, text="Modelo do Carro:")
        self.label_modelo.pack(side=tk.LEFT)

        self.entry_modelo = tk.Entry(self.frame_controles)
        self.entry_modelo.pack(side=tk.LEFT)

        self.label_vaga = tk.Label(self.frame_controles, text="Vaga:")
        self.label_vaga.pack(side=tk.LEFT)

        self.entry_vaga = tk.Entry(self.frame_controles)
        self.entry_vaga.pack(side=tk.LEFT)

        self.btn_alocar = tk.Button(self.frame_controles, text="Alocar Carro", command=self.alocar_carro)
        self.btn_alocar.pack(side=tk.LEFT)

        self.btn_liberar = tk.Button(self.frame_controles, text="Liberar Vaga", command=self.liberar_vaga)
        self.btn_liberar.pack(side=tk.LEFT)

        self.label_tempo_vaga = tk.Label(self.root, text="Tempo na Vaga:")
        self.label_tempo_vaga.pack()

        self.label_tempo_total = tk.Label(self.root, text="Tempo Total:")
        self.label_tempo_total.pack()

        self.label_valor_hora = tk.Label(self.root, text="Valor por Hora: R$ 0.00")
        self.label_valor_hora.pack()

        self.label_valor_segundo = tk.Label(self.root, text="Valor por Segundo: R$ 0.000000")
        self.label_valor_segundo.pack()

        self.label_total_pago = tk.Label(self.root, text="Total Pago: R$ 0.00")
        self.label_total_pago.pack(pady=10)

    def atualizar_cronometros(self):
        for i, vaga in enumerate(self.vagas_estacionamento):
            if vaga.carro is not None and vaga.inicio is not None:
                tempo_decorrido_vaga = datetime.now() - vaga.inicio
                self.labels_vagas[i].config(text=f"Vaga {vaga.numero}: {vaga.carro} | Tempo: {self.formatar_tempo(tempo_decorrido_vaga)}")

        tempo_decorrido_total = datetime.now() - self.vagas_estacionamento[0].inicio if self.vagas_estacionamento[0].inicio else timedelta(seconds=0)
        self.label_tempo_total.config(text=f"Tempo Total: {self.formatar_tempo(tempo_decorrido_total)}")

        valor_hora_total = self.calcular_valor_hora_total()
        self.label_valor_hora.config(text=f"Valor por Hora: R$ {valor_hora_total:.2f}")

        self.valor_por_segundo = self.calcular_valor_segundo()
        self.label_valor_segundo.config(text=f"Valor por Segundo: R$ {self.valor_por_segundo:.6f}")

        self.root.after(1000, self.atualizar_cronometros)  # Agendar próxima atualização após 1 segundo

    def formatar_tempo(self, tempo):
        segundos = tempo.total_seconds()
        horas = int(segundos // 3600)
        minutos = int((segundos % 3600) // 60)
        segundos = int(segundos % 60)
        return f"{horas:02}:{minutos:02}:{segundos:02}"

    def calcular_valor(self, tempo_decorrido):
        segundos = tempo_decorrido.total_seconds()
        valor_a_pagar = segundos * self.valor_por_segundo
        return valor_a_pagar

    def calcular_valor_hora_total(self):
        tempo_total = sum([(datetime.now() - vaga.inicio).total_seconds() for vaga in self.vagas_estacionamento if vaga.inicio])
        horas_total = tempo_total / 3600  # Converter segundos para horas
        valor_hora_total = horas_total * self.valor_por_segundo * 3600  # Valor da hora total
        return valor_hora_total

    def calcular_valor_segundo(self):
        carros_ocupados = [vaga for vaga in self.vagas_estacionamento if vaga.inicio]
        total_tempo_ocupacao = sum([(datetime.now() - vaga.inicio).total_seconds() for vaga in carros_ocupados])
        total_segundos = len(carros_ocupados) * total_tempo_ocupacao
        valor_segundo = self.total_pago / total_segundos if total_segundos > 0 else 0
        return valor_segundo

    def alocar_carro(self):
        numero_vaga = int(self.entry_vaga.get()) - 1  # Índice da lista começa em 0
        if 0 <= numero_vaga < len(self.vagas_estacionamento):
            placa = self.entry_placa.get()
            modelo = self.entry_modelo.get()
            carro = f"{modelo} ({placa})"
            self.vagas_estacionamento[numero_vaga].carro = carro
            self.vagas_estacionamento[numero_vaga].inicio = datetime.now()
            self.labels_vagas[numero_vaga].config(text=f"Vaga {numero_vaga+1}: {carro}")
            self.entry_placa.delete(0, tk.END)  # Limpar o campo após alocar
            self.entry_modelo.delete(0, tk.END)  # Limpar o campo após alocar
            self.entry_vaga.delete(0, tk.END)  # Limpar o campo após alocar
            self.valor_por_segundo = self.calcular_valor_segundo()  # Atualizar o valor por segundo

    def liberar_vaga(self):
        numero_vaga = int(self.entry_vaga.get()) - 1  # Índice da lista começa em 0
        if 0 <= numero_vaga < len(self.vagas_estacionamento):
            vaga = self.vagas_estacionamento[numero_vaga]
            if vaga.carro:
                tempo_decorrido = datetime.now() - vaga.inicio
                valor_a_pagar = self.calcular_valor(tempo_decorrido)
                self.total_pago += valor_a_pagar
                self.label_total_pago.config(text=f"Total Pago: R$ {self.total_pago:.2f}")
                self.vagas_estacionamento[numero_vaga].carro = None
                self.vagas_estacionamento[numero_vaga].inicio = None
                self.labels_vagas[numero_vaga].config(text=f"Vaga {numero_vaga+1}: Livre")
                self.valor_por_segundo = self.calcular_valor_segundo()  # Atualizar o valor por segundo

if __name__ == "__main__":
    root = tk.Tk()
    app = EstacionamentoApp(root)
    root.mainloop()
