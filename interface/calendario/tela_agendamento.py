import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
from interface.tela_base import TelaBase
from PIL import Image, ImageTk
import os

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
        
        # Definir cores e estilos
        self.cor_primaria = "#3a7ebf"
        self.cor_secundaria = "#2a5885"
        self.cor_fundo = "#f0f0f0"
        self.cor_erro = "#e74c3c"
        self.cor_sucesso = "#2ecc71"
        
        # Verificar se um robô foi selecionado
        if not robo_nome:
            print('Nenhum robô selecionado para agendar!')
            if self.tela_anterior:
                self.tela_anterior.voltar_ao_menu()
            return  # Evita continuar se nenhum robô estiver selecionado
        
        # Configuração da grade principal
        self.janela.columnconfigure(0, weight=1)
        self.janela.rowconfigure(0, weight=0)
        self.janela.rowconfigure(1, weight=1)
        self.janela.rowconfigure(2, weight=0)
        
        # Criar frame principal para conter todos os elementos
        self.frame_principal = ctk.CTkFrame(self.janela)
        self.frame_principal.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_principal.columnconfigure(0, weight=1)
        
        # Criar frame para o conteúdo de agendamento
        self.frame_agendamento = ctk.CTkFrame(self.frame_principal)
        self.frame_agendamento.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        # Criar frame para mensagens de erro/sucesso (inicialmente oculto)
        self.frame_mensagem = ctk.CTkFrame(self.frame_principal)
        self.frame_mensagem.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.frame_mensagem.grid_remove()  # Inicialmente oculto
        
        # Configurar o frame de agendamento
        self._configurar_frame_agendamento()
        
        # Configurar o frame de mensagem
        self._configurar_frame_mensagem()
        
        # Iniciar a interface
        self.exibir()
    
    def _configurar_frame_agendamento(self):
        """Configura o frame de agendamento com todos os elementos"""
        # Configuração da grade
        self.frame_agendamento.columnconfigure(0, weight=1)
        self.frame_agendamento.columnconfigure(1, weight=1)
        self.frame_agendamento.rowconfigure(0, weight=0)
        self.frame_agendamento.rowconfigure(1, weight=1)
        self.frame_agendamento.rowconfigure(2, weight=0)
        self.frame_agendamento.rowconfigure(3, weight=0)
        self.frame_agendamento.rowconfigure(4, weight=0)

        # Criar rótulo para o título com estilo moderno
        label_titulo = ctk.CTkLabel(
            self.frame_agendamento, 
            text=f"Agendando execução para: {self.robo_nome}",
            font=("Arial", 18, "bold")
        )
        label_titulo.grid(row=0, column=0, columnspan=2, pady=(0, 20), sticky="n")

        # Criar frame para o calendário e hora
        frame_data_hora = ctk.CTkFrame(self.frame_agendamento)
        frame_data_hora.grid(row=1, column=0, columnspan=2, padx=20, pady=10, sticky="nsew")
        frame_data_hora.columnconfigure(0, weight=1)
        frame_data_hora.columnconfigure(1, weight=1)
        
        # Adicionar rótulo para a data
        label_data = ctk.CTkLabel(
            frame_data_hora, 
            text="Data de execução:",
            font=("Arial", 14)
        )
        label_data.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")
        
        # Criar o calendário para selecionar a data com estilo moderno
        self.cal = Calendar(
            frame_data_hora, 
            selectmode="day", 
            year=2025, 
            month=3, 
            day=5,
            background=self.cor_primaria,
            foreground="white",
            bordercolor=self.cor_secundaria,
            headersbackground=self.cor_secundaria,
            headersforeground="white",
            selectbackground=self.cor_secundaria
        )
        self.cal.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # Criar frame para a hora
        frame_hora = ctk.CTkFrame(frame_data_hora)
        frame_hora.grid(row=1, column=1, padx=10, pady=5, sticky="n")
        
        # Adicionar rótulo para a hora
        label_hora = ctk.CTkLabel(
            frame_data_hora, 
            text="Horário:",
            font=("Arial", 14)
        )
        label_hora.grid(row=0, column=1, padx=10, pady=(10, 5), sticky="w")
        
        # Ajustar o campo da hora com estilo moderno
        self.entry_hora = ctk.CTkEntry(
            frame_hora, 
            placeholder_text="HH:MM", 
            width=120,
            height=40,
            font=("Arial", 14)
        )
        self.entry_hora.pack(padx=10, pady=10)
        
        # Adicionar texto de ajuda para o formato da hora
        label_formato = ctk.CTkLabel(
            frame_hora, 
            text="Formato: 24h (ex: 14:30)",
            font=("Arial", 12),
            text_color="gray"
        )
        label_formato.pack(padx=10, pady=(0, 10))

        # Criar um frame para agrupar o checkbox e o campo de dias
        frame_rotina = ctk.CTkFrame(self.frame_agendamento)
        frame_rotina.grid(row=2, column=0, columnspan=2, padx=20, pady=20, sticky="nsew")
        
        # Adicionar rótulo para a seção de repetição
        label_repeticao = ctk.CTkLabel(
            frame_rotina, 
            text="Configuração de repetição:",
            font=("Arial", 14, "bold")
        )
        label_repeticao.pack(anchor="w", padx=10, pady=(10, 15))

        # Criar frame para os controles de repetição
        frame_controles = ctk.CTkFrame(frame_rotina)
        frame_controles.pack(fill="x", padx=10, pady=5)

        # Criar checkbox para habilitar rotina de execução
        self.rotina_var = tk.BooleanVar(value=False)  # Variável de controle
        checkbox_rotina_execucao = ctk.CTkCheckBox(
            frame_controles, 
            text="Repetir a cada", 
            variable=self.rotina_var, 
            command=self.toggle_entry,
            font=("Arial", 13)
        )
        checkbox_rotina_execucao.pack(side="left", padx=(10, 5), pady=10)

        # Criar campo para digitar os dias (inicialmente desativado)
        self.entry_dias = ctk.CTkEntry(
            frame_controles, 
            placeholder_text="Dias", 
            width=70, 
            height=30,
            state="disabled",
            font=("Arial", 13)
        )
        self.entry_dias.pack(side="left", padx=5, pady=10)

        # Criar rótulo "dias"
        label_dias = ctk.CTkLabel(
            frame_controles, 
            text="dias", 
            font=("Arial", 13)
        )
        label_dias.pack(side="left", padx=(5, 10), pady=10)

        # Criar frame para mensagens de validação
        self.frame_validacao = ctk.CTkFrame(self.frame_agendamento)
        self.frame_validacao.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
        self.frame_validacao.grid_remove()  # Inicialmente oculto
        
        # Criar label para mensagens de validação
        self.label_validacao = ctk.CTkLabel(
            self.frame_validacao, 
            text="", 
            font=("Arial", 13),
            text_color=self.cor_erro
        )
        self.label_validacao.pack(padx=10, pady=10, fill="x")

        # Criando um frame para os botões na parte inferior
        frame_botoes = ctk.CTkFrame(self.frame_agendamento)
        frame_botoes.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="ew")

        # Criando o botão de agendar com estilo moderno
        btn_agendar = ctk.CTkButton(
            frame_botoes, 
            text="Agendar", 
            command=self.confirmar_agendamento,
            font=("Arial", 14, "bold"),
            fg_color=self.cor_primaria,
            hover_color=self.cor_secundaria,
            height=40
        )
        btn_agendar.pack(side="left", padx=10, pady=10, expand=True, fill="x")
        
        # Criando o botão de voltar com estilo moderno
        btn_voltar = ctk.CTkButton(
            frame_botoes, 
            text="Voltar", 
            command=self.voltar,
            font=("Arial", 14),
            fg_color="#6c757d",
            hover_color="#5a6268",
            height=40
        )
        btn_voltar.pack(side="right", padx=10, pady=10, expand=True, fill="x")
    
    def _configurar_frame_mensagem(self):
        """Configura o frame de mensagem para erro e sucesso"""
        # Configuração da grade
        self.frame_mensagem.columnconfigure(0, weight=1)
        self.frame_mensagem.rowconfigure(0, weight=0)
        self.frame_mensagem.rowconfigure(1, weight=1)
        self.frame_mensagem.rowconfigure(2, weight=0)
        
        # Criar label para o ícone (será configurado dinamicamente)
        self.label_icone = ctk.CTkLabel(self.frame_mensagem, text="", font=("Arial", 48))
        self.label_icone.grid(row=0, column=0, pady=(30, 20))
        
        # Criar label para a mensagem (será configurado dinamicamente)
        self.label_mensagem = ctk.CTkLabel(
            self.frame_mensagem, 
            text="", 
            font=("Arial", 18, "bold"),
            wraplength=400
        )
        self.label_mensagem.grid(row=1, column=0, padx=20, pady=20)
        
        # Criar botão para voltar ao menu
        self.btn_voltar_menu = ctk.CTkButton(
            self.frame_mensagem, 
            text="Voltar ao Menu Principal", 
            command=self.voltar,
            font=("Arial", 14, "bold"),
            fg_color=self.cor_primaria,
            hover_color=self.cor_secundaria,
            height=40,
            width=200
        )
        self.btn_voltar_menu.grid(row=2, column=0, pady=(20, 30))

    def toggle_entry(self):
        """Ativa/desativa entry_dias"""
        if self.rotina_var.get():
            self.entry_dias.configure(state="normal")
        else:
            self.entry_dias.configure(state="disabled")

    def mostrar_erro(self, mensagem):
        """Mostra mensagem de erro na interface"""
        self.frame_validacao.grid()
        self.label_validacao.configure(text=mensagem)
    
    def mostrar_tela_erro(self, mensagem):
        """Mostra a tela de erro completa"""
        # Configurar a mensagem de erro
        self.label_icone.configure(text="❌", text_color=self.cor_erro)
        self.label_mensagem.configure(
            text=f"Erro no agendamento:\n\n{mensagem}",
            text_color=self.cor_erro
        )
        
        # Esconder o frame de agendamento e mostrar o frame de mensagem
        self.frame_agendamento.grid_remove()
        self.frame_mensagem.grid()
    
    def mostrar_tela_sucesso(self, data_hora, repeticao):
        """Mostra a tela de sucesso"""
        # Configurar a mensagem de sucesso
        self.label_icone.configure(text="✅", text_color=self.cor_sucesso)
        
        # Formatar a mensagem de sucesso
        mensagem = f"Agendamento realizado com sucesso!\n\nRobô: {self.robo_nome}\nData/Hora: {data_hora.strftime('%d/%m/%Y às %H:%M')}"
        
        # Adicionar informação de repetição se aplicável
        if repeticao:
            mensagem += f"\nRepetição: A cada {repeticao} dias"
        
        self.label_mensagem.configure(
            text=mensagem,
            text_color=self.cor_sucesso
        )
        
        # Esconder o frame de agendamento e mostrar o frame de mensagem
        self.frame_agendamento.grid_remove()
        self.frame_mensagem.grid()

    def confirmar_agendamento(self):
        """Confirma o agendamento e armazena a data/hora"""
        # Limpar mensagens de erro anteriores
        self.frame_validacao.grid_remove()
        
        data_selecionada = self.cal.get_date()
        hora_selecionada = self.entry_hora.get()
        dias_repeticao = self.entry_dias.get() if self.rotina_var.get() else None
        
        # Validar entrada de hora
        if not hora_selecionada:
            self.mostrar_erro("Por favor, informe o horário do agendamento.")
            return
            
        # Validar formato da hora
        if not self._validar_formato_hora(hora_selecionada):
            self.mostrar_erro("Formato de horário inválido. Use o formato HH:MM (ex: 14:30).")
            return
            
        # Validar dias de repetição se ativado
        if self.rotina_var.get():
            if not dias_repeticao:
                self.mostrar_erro("Por favor, informe o número de dias para repetição.")
                return
                
            if not dias_repeticao.isdigit() or int(dias_repeticao) <= 0:
                self.mostrar_erro("O número de dias para repetição deve ser um número positivo.")
                return

        try:
            # Converter para datetime
            horario_agendado = datetime.strptime(f"{data_selecionada} {hora_selecionada}", "%m/%d/%y %H:%M")

            # Adicionar à lista de agendamentos
            agendamentos.append((self.robo_nome, horario_agendado, dias_repeticao))
            print(f"Robô {self.robo_nome} agendado para {horario_agendado} com repetição: {dias_repeticao} dias")

            # Mostrar tela de sucesso
            self.mostrar_tela_sucesso(horario_agendado, dias_repeticao)
            
        except ValueError as e:
            # Mostrar tela de erro
            self.mostrar_tela_erro("Formato de data/hora inválido. Verifique os dados informados.")
            print(f"Erro ao agendar: {e}")
    
    def _validar_formato_hora(self, hora):
        """Valida se a hora está no formato correto HH:MM"""
        if len(hora) != 5:
            return False
            
        if hora[2] != ':':
            return False
            
        horas, minutos = hora.split(':')
        
        if not horas.isdigit() or not minutos.isdigit():
            return False
            
        horas_int = int(horas)
        minutos_int = int(minutos)
        
        if horas_int < 0 or horas_int > 23:
            return False
            
        if minutos_int < 0 or minutos_int > 59:
            return False
            
        return True
            
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
