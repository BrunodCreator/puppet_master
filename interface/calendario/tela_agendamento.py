import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
from interface.tela_base import TelaBase

# Lista para armazenar agendamentos
agendamentos = []

class TelaAgendamento(TelaBase):
    def __init__(self, janela_pai=None, robo_nome=None, tela_anterior=None):
        # Inicializar a classe base
        super().__init__()
        
        # Se uma janela pai for fornecida, destrua a janela criada pela classe base
        # e use a janela pai
        if janela_pai:
            self.janela.destroy()
            self.janela = janela_pai
            
        # Armazenar referência à tela anterior para poder voltar
        self.tela_anterior = tela_anterior
        self.robo_nome = robo_nome
        
        # Alterar o título para indicar que estamos na tela de agendamento
        self.alterar_titulo("Agendamento")
        
        if not robo_nome:
            print('Nenhum robô selecionado para agendar!')
            if self.tela_anterior:
                self.tela_anterior.voltar_ao_menu()
            return  # Evita continuar se nenhum robô estiver selecionado
        
        # Configuração da grade
        self.janela.columnconfigure(0, weight=1)
        self.janela.columnconfigure(1, weight=1)  # Para alinhar o campo de entrada
        self.janela.rowconfigure(3, weight=1)

        # Criar rótulo para o título
        label_titulo = ctk.CTkLabel(self.janela, text=f"Agendando execução para: {robo_nome}")
        label_titulo.grid(row=0, column=0, columnspan=2, pady=10, sticky="n")

        # Criar o calendário para selecionar a data
        self.cal = Calendar(self.janela, selectmode="day", year=2025, month=3, day=5)
        self.cal.grid(row=1, column=0, padx=0, pady=0, sticky="n")

        # Ajustar o campo da hora para ficar melhor posicionado ao lado do calendário
        self.entry_hora = ctk.CTkEntry(self.janela, placeholder_text="Hora (HH:MM)", width=100)
        self.entry_hora.grid(row=1, column=1, padx=0, pady=0, sticky="sw")

        # Criar um frame para agrupar o checkbox e o campo de dias
        frame_rotina = ctk.CTkFrame(self.janela)
        frame_rotina.grid(row=3, column=0, columnspan=2, pady=10, sticky="n", padx=20)

        # Criar checkbox para habilitar rotina de execução
        self.rotina_var = tk.BooleanVar(value=False)  # Variável de controle
        checkbox_rotina_execucao = ctk.CTkCheckBox(
            frame_rotina, text="Repetir a cada", variable=self.rotina_var, command=self.toggle_entry
        )
        checkbox_rotina_execucao.grid(row=0, column=0, sticky="w")

        # Criar campo para digitar os dias (inicialmente desativado)
        self.entry_dias = ctk.CTkEntry(frame_rotina, placeholder_text="Dias", width=50, state="disabled")
        self.entry_dias.grid(row=0, column=1, padx=5, pady=0)

        # Criar rótulo "dias"
        label_dias = ctk.CTkLabel(frame_rotina, text="dias", font=("Arial", 12))
        label_dias.grid(row=0, column=2, sticky="w")

        # Criando um frame para os botões na parte inferior
        frame_botoes = ctk.CTkFrame(self.janela)
        frame_botoes.grid(row=4, column=0, columnspan=2, sticky="s", pady=10)

        # Criando o botão de agendar
        btn_agendar = ctk.CTkButton(frame_botoes, text="Agendar", command=self.confirmar_agendamento)
        btn_agendar.grid(row=0, column=0, pady=0, padx=10)
        
        # Criando o botão de voltar
        btn_voltar = ctk.CTkButton(frame_botoes, text="Voltar", command=self.voltar)
        btn_voltar.grid(row=0, column=1, pady=0, padx=10)
        
        # Iniciar a interface
        self.exibir()

    def toggle_entry(self):
        """Ativa/desativa entry_dias"""
        if self.rotina_var.get():
            self.entry_dias.configure(state="normal")
        else:
            self.entry_dias.configure(state="disabled")

    def confirmar_agendamento(self):
        """Confirma o agendamento e armazena a data/hora"""
        data_selecionada = self.cal.get_date()
        hora_selecionada = self.entry_hora.get()
        dias_repeticao = self.entry_dias.get() if self.rotina_var.get() else None  # Captura apenas se ativado

        try:
            # Converter para datetime
            horario_agendado = datetime.strptime(f"{data_selecionada} {hora_selecionada}", "%m/%d/%y %H:%M")

            # Adicionar à lista de agendamentos
            agendamentos.append((self.robo_nome, horario_agendado, dias_repeticao))
            print(f"Robô {self.robo_nome} agendado para {horario_agendado} com repetição: {dias_repeticao} dias")

            # Voltar para a tela anterior
            self.voltar()
        except ValueError:
            print("Formato de horário inválido. Use HH:MM")
            
    def voltar(self):
        """Volta para a tela anterior"""
        if self.tela_anterior:
            self.tela_anterior.voltar_ao_menu()
        else:
            # Se não houver tela anterior, apenas fecha esta janela
            self.janela.destroy()


# Função legada para compatibilidade com código existente
def abrir_janela_agendamento(robo_nome):
    """Função legada para compatibilidade com código existente"""
    tela = TelaAgendamento(None, robo_nome)
    return tela
