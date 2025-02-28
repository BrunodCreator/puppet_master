import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
import threading
import time

# Lista para armazenar agendamentos
agendamentos = []

def abrir_janela_agendamento(robo_selecionado):
    """Abre uma janela para selecionar a data/hora de execução do robô"""
    janela_agendamento = ctk.CTkToplevel()  # Criando uma nova janela
    janela_agendamento.title("Agendar Execução")
    janela_agendamento.geometry("400x300")

    ctk.CTkLabel(janela_agendamento, text=f"Agendar execução para: {robo_selecionado}").pack(pady=10)

    # Criar o calendário para selecionar a data
    cal = Calendar(janela_agendamento, selectmode="day", year=2024, month=2, day=28)
    cal.pack(pady=10)

    # Campo para selecionar o horário
    entry_hora = ctk.CTkEntry(janela_agendamento, placeholder_text="Hora (HH:MM)")
    entry_hora.pack(pady=5)

    def confirmar_agendamento():
        """Confirma o agendamento e armazena a data/hora"""
        data_selecionada = cal.get_date()
        hora_selecionada = entry_hora.get()

        try:
            # Converter para datetime
            horario_agendado = datetime.strptime(f"{data_selecionada} {hora_selecionada}", "%m/%d/%y %H:%M")

            # Adicionar à lista de agendamentos
            agendamentos.append((robo_selecionado, horario_agendado))
            print(f"Robô {robo_selecionado} agendado para {horario_agendado}")

            janela_agendamento.destroy()  # Fechar janela
        except ValueError:
            print("Formato de horário inválido. Use HH:MM")

    ctk.CTkButton(janela_agendamento, text="Agendar", command=confirmar_agendamento).pack(pady=10)

    janela_agendamento.mainloop()

# Simulando a seleção de um robô e a chamada da função
robo_selecionado = "MeuRobo.exe"
abrir_janela_agendamento(robo_selecionado)
