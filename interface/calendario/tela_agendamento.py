import customtkinter as ctk
import tkinter as tk
from tkcalendar import Calendar
from datetime import datetime
import os
import sys

# Adicionar o diretório pai ao path para importar TelaBase
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from interface.tela_base import TelaBase

# Lista para armazenar agendamentos
agendamentos = []

class TelaAgendamento(TelaBase):
    """Classe para a tela de agendamento de execução de robôs"""
    
    def __init__(self, robo_nome=None):
        """Inicializa a tela de agendamento"""
        super().__init__()
        
        # Configurações da janela
        self.janela.title("Agendar Execução")
        self.janela.geometry("700x500")
        self.alterar_titulo("Agendamento de Execução")
        
        # Variáveis de controle
        self.robo_nome = robo_nome
        self.rotina_var = tk.BooleanVar(value=False)
        
        # Configuração da grade
        self.janela.columnconfigure(0, weight=1)
        self.janela.columnconfigure(1, weight=1)
        self.janela.rowconfigure(3, weight=1)
        
        # Criar os elementos da interface
        self._criar_interface()
        
    def _criar_interface(self):
        """Cria todos os elementos da interface"""
        # Frame principal com fundo personalizado
        self.frame_principal = ctk.CTkFrame(self.janela, fg_color="#2b2b2b", corner_radius=15)
        self.frame_principal.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Configuração da grade do frame principal
        self.frame_principal.columnconfigure(0, weight=1)
        self.frame_principal.columnconfigure(1, weight=1)
        self.frame_principal.rowconfigure(4, weight=1)
        
        # Título com estilo
        if self.robo_nome:
            titulo_texto = f"Agendando execução para: {self.robo_nome}"
        else:
            titulo_texto = "Agendamento de Execução"
            
        self.label_titulo = ctk.CTkLabel(
            self.frame_principal, 
            text=titulo_texto,
            font=("Arial Bold", 18),
            text_color="#4cc2ff"
        )
        self.label_titulo.grid(row=0, column=0, columnspan=2, pady=(20, 15), sticky="n")
        
        # Subtítulo com instruções
        self.label_subtitulo = ctk.CTkLabel(
            self.frame_principal,
            text="Selecione a data e hora para a execução do robô",
            font=("Arial", 12),
            text_color="#cccccc"
        )
        self.label_subtitulo.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky="n")
        
        # Frame para o calendário com borda
        self.frame_calendario = ctk.CTkFrame(self.frame_principal, corner_radius=10, border_width=1, border_color="#555555")
        self.frame_calendario.grid(row=2, column=0, padx=20, pady=10, sticky="n")
        
        # Calendário para selecionar a data
        self.calendario = Calendar(
            self.frame_calendario, 
            selectmode="day", 
            year=datetime.now().year, 
            month=datetime.now().month, 
            day=datetime.now().day,
            background="#333333",
            foreground="white",
            bordercolor="#555555",
            headersbackground="#2b2b2b",
            headersforeground="#4cc2ff",
            selectbackground="#4cc2ff",
            normalbackground="#333333",
            weekendbackground="#3a3a3a",
            othermonthbackground="#2b2b2b",
            othermonthwebackground="#2b2b2b"
        )
        self.calendario.pack(padx=10, pady=10)
        
        # Frame para os controles de hora
        self.frame_hora = ctk.CTkFrame(self.frame_principal, corner_radius=10, fg_color="#333333")
        self.frame_hora.grid(row=2, column=1, padx=20, pady=10, sticky="n")
        
        # Label para a hora
        self.label_hora = ctk.CTkLabel(
            self.frame_hora,
            text="Horário de Execução",
            font=("Arial", 14),
            text_color="#4cc2ff"
        )
        self.label_hora.pack(pady=(15, 10))
        
        # Entrada para a hora
        self.entry_hora = ctk.CTkEntry(
            self.frame_hora, 
            placeholder_text="Hora (HH:MM)",
            width=150,
            height=35,
            corner_radius=8,
            border_width=1,
            border_color="#555555"
        )
        self.entry_hora.pack(pady=(5, 15))
        
        # Exemplo de formato
        self.label_exemplo = ctk.CTkLabel(
            self.frame_hora,
            text="Exemplo: 14:30",
            font=("Arial", 12),
            text_color="#aaaaaa"
        )
        self.label_exemplo.pack(pady=(0, 15))
        
        # Frame para configuração de repetição
        self.frame_rotina = ctk.CTkFrame(self.frame_principal, corner_radius=10, fg_color="#333333")
        self.frame_rotina.grid(row=3, column=0, columnspan=2, pady=20, padx=20, sticky="n")
        
        # Título da seção de repetição
        self.label_rotina = ctk.CTkLabel(
            self.frame_rotina,
            text="Configuração de Repetição",
            font=("Arial", 14),
            text_color="#4cc2ff"
        )
        self.label_rotina.pack(pady=(15, 10))
        
        # Frame para os controles de repetição
        self.frame_controles_rotina = ctk.CTkFrame(self.frame_rotina, fg_color="transparent")
        self.frame_controles_rotina.pack(pady=(0, 15))
        
        # Checkbox para habilitar rotina de execução
        self.checkbox_rotina = ctk.CTkCheckBox(
            self.frame_controles_rotina, 
            text="Repetir a cada", 
            variable=self.rotina_var, 
            command=self._toggle_entry,
            checkbox_width=20,
            checkbox_height=20,
            corner_radius=5,
            border_width=2,
            hover_color="#4cc2ff",
            fg_color="#4cc2ff"
        )
        self.checkbox_rotina.pack(side="left", padx=(0, 5))
        
        # Entrada para os dias de repetição
        self.entry_dias = ctk.CTkEntry(
            self.frame_controles_rotina, 
            placeholder_text="Dias", 
            width=60,
            height=30,
            state="disabled",
            corner_radius=8,
            border_width=1,
            border_color="#555555"
        )
        self.entry_dias.pack(side="left", padx=5)
        
        # Label para "dias"
        self.label_dias = ctk.CTkLabel(
            self.frame_controles_rotina, 
            text="dias", 
            font=("Arial", 12),
            text_color="#cccccc"
        )
        self.label_dias.pack(side="left", padx=(5, 0))
        
        # Frame para os botões
        self.frame_botoes = ctk.CTkFrame(self.frame_principal, fg_color="transparent")
        self.frame_botoes.grid(row=4, column=0, columnspan=2, pady=(20, 10), sticky="s")
        
        # Botão de cancelar
        self.btn_cancelar = ctk.CTkButton(
            self.frame_botoes, 
            text="Cancelar", 
            command=self.janela.destroy,
            width=120,
            height=35,
            corner_radius=8,
            fg_color="#555555",
            hover_color="#777777"
        )
        self.btn_cancelar.pack(side="left", padx=10)
        
        # Botão de agendar
        self.btn_agendar = ctk.CTkButton(
            self.frame_botoes, 
            text="Agendar", 
            command=self._confirmar_agendamento,
            width=120,
            height=35,
            corner_radius=8,
            fg_color="#4cc2ff",
            hover_color="#3a9fcc"
        )
        self.btn_agendar.pack(side="left", padx=10)
    
    def _toggle_entry(self):
        """Ativa/desativa o campo de dias de repetição"""
        if self.rotina_var.get():
            self.entry_dias.configure(state="normal")
        else:
            self.entry_dias.configure(state="disabled")
    
    def _confirmar_agendamento(self):
        """Confirma o agendamento e armazena a data/hora"""
        data_selecionada = self.calendario.get_date()
        hora_selecionada = self.entry_hora.get()
        dias_repeticao = self.entry_dias.get() if self.rotina_var.get() else None
        
        try:
            # Converter para datetime
            horario_agendado = datetime.strptime(f"{data_selecionada} {hora_selecionada}", "%m/%d/%y %H:%M")
            
            # Adicionar à lista de agendamentos
            agendamentos.append((self.robo_nome, horario_agendado, dias_repeticao))
            print(f"Robô {self.robo_nome} agendado para {horario_agendado} com repetição: {dias_repeticao} dias")
            
            # Mostrar mensagem de sucesso
            self._mostrar_mensagem_sucesso(horario_agendado, dias_repeticao)
            
            # Fechar janela após 2 segundos
            self.janela.after(2000, self.janela.destroy)
            
        except ValueError:
            self._mostrar_erro("Formato de horário inválido. Use HH:MM")
    
    def _mostrar_mensagem_sucesso(self, horario, repeticao):
        """Mostra uma mensagem de sucesso na interface"""
        # Esconder todos os widgets
        for widget in self.frame_principal.winfo_children():
            widget.grid_forget()
        
        # Frame de sucesso
        frame_sucesso = ctk.CTkFrame(self.frame_principal, fg_color="#333333", corner_radius=15)
        frame_sucesso.pack(fill="both", expand=True, padx=30, pady=30)
        
        # Ícone ou texto de sucesso
        label_sucesso = ctk.CTkLabel(
            frame_sucesso,
            text="✓",
            font=("Arial Bold", 48),
            text_color="#4cc2ff"
        )
        label_sucesso.pack(pady=(30, 10))
        
        # Mensagem de sucesso
        texto_sucesso = f"Agendamento realizado com sucesso!\n\n"
        texto_sucesso += f"Robô: {self.robo_nome}\n"
        texto_sucesso += f"Data e hora: {horario.strftime('%d/%m/%Y às %H:%M')}\n"
        
        if repeticao:
            texto_sucesso += f"Repetição: A cada {repeticao} dias"
        else:
            texto_sucesso += "Sem repetição"
            
        label_mensagem = ctk.CTkLabel(
            frame_sucesso,
            text=texto_sucesso,
            font=("Arial", 14),
            text_color="#ffffff"
        )
        label_mensagem.pack(pady=(10, 30))
    
    def _mostrar_erro(self, mensagem):
        """Mostra uma mensagem de erro na interface"""
        # Criar uma janela de erro
        janela_erro = ctk.CTkToplevel(self.janela)
        janela_erro.title("Erro")
        janela_erro.geometry("400x200")
        janela_erro.grab_set()
        
        # Frame de erro
        frame_erro = ctk.CTkFrame(janela_erro, fg_color="#3a3a3a", corner_radius=10)
        frame_erro.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Ícone ou texto de erro
        label_icone = ctk.CTkLabel(
            frame_erro,
            text="⚠",
            font=("Arial Bold", 36),
            text_color="#ff6b6b"
        )
        label_icone.pack(pady=(20, 10))
        
        # Mensagem de erro
        label_mensagem = ctk.CTkLabel(
            frame_erro,
            text=mensagem,
            font=("Arial", 14),
            text_color="#ffffff"
        )
        label_mensagem.pack(pady=(10, 20))
        
        # Botão de OK
        btn_ok = ctk.CTkButton(
            frame_erro,
            text="OK",
            command=janela_erro.destroy,
            width=100,
            height=30,
            corner_radius=8,
            fg_color="#ff6b6b",
            hover_color="#ff8c8c"
        )
        btn_ok.pack(pady=(0, 20))


def abrir_janela_agendamento(robo_nome):
    """Função para abrir a janela de agendamento a partir de outras partes do código"""
    if not robo_nome:
        print('Nenhum robô selecionado para agendar!')
        return  # Evita abrir a janela se nenhum robô estiver selecionado
    
    # Criar e exibir a tela de agendamento
    tela = TelaAgendamento(robo_nome)
    tela.exibir()


# Para testes
if __name__ == "__main__":
    app = TelaAgendamento("Teste_Robo.exe")
    app.exibir()
