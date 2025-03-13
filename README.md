🕹️ Puppet Master

📌 Visão Geral

Puppet Master é um sistema de automação e gerenciamento de robôs que permite executar, agendar e monitorar processos automatizados. O sistema conta com uma interface gráfica intuitiva para facilitar a gestão dos robôs e oferece integração com a Evolution API, permitindo interação e controle via WhatsApp.

🔥 Principais Funcionalidades

✅ Gerenciamento de Robôs

Exibição de todos os robôs disponíveis na pasta configurada.

Interface gráfica para seleção e execução dos robôs.

Ícones personalizados para melhor identificação.

⏳ Agendamento de Execuções

Interface para agendar execuções futuras dos robôs.

Seleção de data e horário via calendário interativo.

Opção para agendamento recorrente, permitindo repetições em intervalos específicos.

Salvamento das execuções agendadas em banco de dados SQLite.

📊 Verificação de Logs de Execução

Registro das execuções realizadas com status e timestamps.

Exibição de logs para análise e solução de problemas.

Filtro de logs por data, status ou robô específico.

📱 Integração com Evolution API (WhatsApp)

Envio de notificações sobre execuções concluídas ou erros encontrados.

Comandos via WhatsApp para executar, agendar e consultar logs dos robôs.

Respostas automáticas informando o status das execuções.

🏗️ Tecnologias Utilizadas

Python 3 🐍 (Linguagem principal)

CustomTkinter 🎨 (Interface gráfica moderna e responsiva)

SQLite 🗄️ (Banco de dados local para armazenamento de agendamentos e logs)

TkCalendar 📆 (Seleção de datas para agendamentos)

Evolution API 📲 (Integração com WhatsApp)

Subprocess ⚙️ (Execução e monitoramento de processos automatizados)

🔧 Como Executar o Projeto

Clone o repositório

git clone https://github.com/seuusuario/puppet_master.git
cd puppet_master

Instale as dependências

pip install -r requirements.txt

Execute o programa

python PUPPET_MASTER/main.py

⚡ Comandos Disponíveis via WhatsApp

Após a integração com a Evolution API, os seguintes comandos podem ser enviados para o bot do WhatsApp:

!executar NomeDoRobo → Executa um robô imediatamente.

!agendar NomeDoRobo 10/03/2025 15:30 → Agenda uma execução.

!status NomeDoRobo → Retorna o status da última execução.

!logs NomeDoRobo → Exibe os logs recentes do robô.

📌 Próximos Passos

✅ Criar banco SQLite para salvar dados de agendamento e execução.

✅ Criar lógica da tela 'Agendar Execução'.

✅ Criar tela 'Consultar Execução' e a lógica correspondente.

✅ Criar webhook para a instância do WhatsApp já configurada.

✅ Configurar a lógica para que os robôs possam ser acessados via WhatsApp

📊 Melhorias na interface de logs, incluindo gráficos de desempenho.

🔔 Integração com e-mail para envio de relatórios automáticos.

💡 Contribuições

Contribuições são bem-vindas! Se você deseja ajudar no desenvolvimento do Puppet Master, sinta-se à vontade para abrir issues e pull requests.

📄 Licença

Este projeto está sob a licença MIT. Sinta-se livre para usar e modificar conforme necessário.

Desenvolvido por: Emerson Bruno de Queiroz
