import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime

# Lista para armazenar agendamentos
agendamentos = []

def abrir_janela_agendamento(robo_nome):
    """Abre uma janela para selecionar a data/hora de execução do robô"""
    if not robo_nome:
        print('Nenhum robô selecionado para agendar!')
        return  # Evita abrir a janela se nenhum robô estiver selecionado
    
    janela_agendamento = ctk.CTkToplevel()
    janela_agendamento.title("Agendar Execução")
    janela_agendamento.geometry("600x400")
    
    janela_agendamento.grab_set()

    # Configuração da grade
    janela_agendamento.columnconfigure(0, weight=1)
    janela_agendamento.columnconfigure(1, weight=1)  # Para alinhar o campo de entrada
    janela_agendamento.rowconfigure(3, weight=1)

    # Criar rótulo para o título
    label_titulo = ctk.CTkLabel(janela_agendamento, text=f"Agendando execução para: {robo_nome}")
    label_titulo.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

    # Criar o calendário para selecionar a data
    cal = Calendar(janela_agendamento, selectmode="day", year=2025, month=3, day=5)
    cal.grid(row=1, column=0, padx=0, pady=0, sticky="n")

    # Ajustar o campo da hora para ficar melhor posicionado ao lado do calendário
    entry_hora = ctk.CTkEntry(janela_agendamento, placeholder_text="Hora (HH:MM)", width=100)
    entry_hora.grid(row=1, column=1, padx=0, pady=0, sticky="sw")

    # Criar um frame para agrupar o checkbox e o campo de dias
    frame_rotina = ctk.CTkFrame(janela_agendamento)
    frame_rotina.grid(row=3, column=0, columnspan=2, pady=10, sticky="n", padx=20)

    # Criar checkbox para habilitar rotina de execução
    rotina_var = tk.BooleanVar(value=False)  # Variável de controle
    checkbox_rotina_execucao = ctk.CTkCheckBox(
        frame_rotina, text="Repetir a cada", variable=rotina_var, command=lambda: toggle_entry()
    )
    checkbox_rotina_execucao.grid(row=0, column=0, sticky="w")

    # Criar campo para digitar os dias (inicialmente desativado)
    entry_dias = ctk.CTkEntry(frame_rotina, placeholder_text="Dias", width=50, state="disabled")
    entry_dias.grid(row=0, column=1, padx=5, pady=0)

    # Criar rótulo "dias"
    label_dias = ctk.CTkLabel(frame_rotina, text="dias", font=("Arial", 12))
    label_dias.grid(row=0, column=2, sticky="w")

    # Função para ativar/desativar entry_dias
    def toggle_entry():
        if rotina_var.get():
            entry_dias.configure(state="normal")
        else:
            entry_dias.configure(state="disabled")

    def confirmar_agendamento():
        """Confirma o agendamento e armazena a data/hora"""
        data_selecionada = cal.get_date()
        hora_selecionada = entry_hora.get()
        dias_repeticao = entry_dias.get() if rotina_var.get() else None  # Captura apenas se ativado

        try:
            # Converter para datetime
            horario_agendado = datetime.strptime(f"{data_selecionada} {hora_selecionada}", "%m/%d/%y %H:%M")

            # Adicionar à lista de agendamentos
            agendamentos.append((robo_nome, horario_agendado, dias_repeticao))
            print(f"Robô {robo_nome} agendado para {horario_agendado} com repetição: {dias_repeticao} dias")

            janela_agendamento.destroy()  # Fechar janela
        except ValueError:
            print("Formato de horário inválido. Use HH:MM")

    # Criando um frame para o botão na parte inferior
    frame_botoes = ctk.CTkFrame(janela_agendamento)
    frame_botoes.grid(row=4, column=0, columnspan=2, sticky="s", pady=10)

    # Criando o botão dentro do frame e posicionando corretamente
    btn_agendar = ctk.CTkButton(frame_botoes, text="Agendar", command=confirmar_agendamento)
    btn_agendar.grid(row=0, column=0, pady=0)

