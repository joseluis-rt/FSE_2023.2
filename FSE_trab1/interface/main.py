import tkinter as tk
from tkinter import ttk
import os
import socket
import threading

# Configurações do servidor
HOST = '127.0.0.1'  # Escuta em todas as interfaces de rede
PORT = 10731  # Porta do servidor (10731-10740)

class TrafficControlTerminal:
    def __init__(self, root):
        self.root = root
        self.root.title("Controle de Tráfego")

       # Widget Text para o terminal
        terminal_frame = ttk.LabelFrame(root, text="Terminal")
        terminal_frame.grid(column=0, row=2, columnspan=2, padx=10, pady=5)

        # Inicializar o widget Text para o terminal, se ainda não estiver inicializado
        if not hasattr(self, 'terminal_text'):
            self.terminal_text = tk.Text(terminal_frame, wrap=tk.WORD, height=15, width=60)
            self.terminal_text.grid(row=0, column=0, padx=0, pady=0)

        # Adicione uma mensagem de boas-vindas
        self.adicionar_mensagem_terminal("Bem-vindo ao Controle de Tráfego!\n")

        # Definir o atributo client_socket
        self.client_socket = None
        # Inicialize a lista de sockets dos clientes
        self.client_sockets = []

        # Variáveis para armazenar informações de tráfego
        self.fluxo_via_principal_media = tk.StringVar()
        self.fluxo_via_principal_dir = tk.StringVar()
        self.fluxo_via_principal_esq = tk.StringVar()
        self.fluxo_via_auxiliar_media = tk.StringVar()
        self.fluxo_via_auxiliar_baixo = tk.StringVar()
        self.fluxo_via_auxiliar_cima = tk.StringVar()
        self.velocidade_via_principal_media = tk.StringVar()
        self.velocidade_via_principal_dir = tk.StringVar()
        self.velocidade_via_principal_esq = tk.StringVar()
        self.velocidade_via_auxiliar_media = tk.StringVar()
        self.velocidade_via_auxiliar_baixo = tk.StringVar()
        self.velocidade_via_auxiliar_cima = tk.StringVar()
        self.total_infracoes = tk.StringVar()
        self.avanco_sinal_infracoes = tk.StringVar()
        self.velocidade_infracoes = tk.StringVar()

        # Configurar rótulos para exibir informações
        # Quadrado de Informações
        info_frame = ttk.LabelFrame(root, text="Informações")
        info_frame.grid(column=0, row=0, columnspan=2, padx=10, pady=5)

        # Quadrado Fluxo de Trânsito (Carros/min)
        fluxo_frame = ttk.LabelFrame(info_frame, text="Fluxo de Trânsito (Carros/min)")
        fluxo_frame.grid(column=0, row=0, padx=10, pady=5, sticky="w")

        # Dentro do quadrado Fluxo de Trânsito (Carros/min)
        fluxo_frame = ttk.LabelFrame(info_frame, text="Fluxo de Trânsito (Carros/min)")
        fluxo_frame.grid(column=0, row=0, padx=10, pady=5, sticky="w")

        # Dentro do quadrado Fluxo de Trânsito (Carros/min)
        fluxo_frame = ttk.LabelFrame(info_frame, text="Fluxo de Trânsito (Carros/min)")
        fluxo_frame.grid(column=0, row=0, padx=10, pady=5, sticky="w")

        # Adicione uma linha divisória horizontal após a etiqueta "Via Principal ⇄"
        ttk.Separator(fluxo_frame, orient="horizontal").grid(column=0, row=0, columnspan=2, sticky="ew")

        # Configurar coluna 0 para centralizar horizontalmente
        root.columnconfigure(0, weight=1)

        # Labels centralizados
        ttk.Label(fluxo_frame, text="Via Principal ⇄").grid(column=0, row=1, columnspan=2, sticky="n")
        ttk.Label(fluxo_frame, text="Média:").grid(column=0, row=2, sticky="e")
        ttk.Label(fluxo_frame, textvariable=self.fluxo_via_principal_media).grid(column=1, row=2, sticky="w")
        ttk.Label(fluxo_frame, text="↠ :").grid(column=0, row=3, sticky="e")
        ttk.Label(fluxo_frame, textvariable=self.fluxo_via_principal_dir).grid(column=1, row=3, sticky="w")
        ttk.Label(fluxo_frame, text="↞ :").grid(column=0, row=4, sticky="e")
        ttk.Label(fluxo_frame, textvariable=self.fluxo_via_principal_esq).grid(column=1, row=4, sticky="w")

        # Adicione uma linha divisória horizontal após a etiqueta "Via Auxiliar ⇅"
        ttk.Separator(fluxo_frame, orient="horizontal").grid(column=0, row=5, columnspan=2, sticky="ew")

        # Configurar centralização dos itens na coluna 0 e 1
        fluxo_frame.columnconfigure(0, weight=1)  # Centraliza a coluna 0
        fluxo_frame.columnconfigure(1, weight=1)  # Centraliza a coluna 1

        # Labels centralizados
        ttk.Label(fluxo_frame, text="Via Auxiliar ⇅").grid(column=0, row=6, columnspan=2, sticky="n")
        ttk.Label(fluxo_frame, text="Média:").grid(column=0, row=7, sticky="e")
        ttk.Label(fluxo_frame, textvariable=self.fluxo_via_auxiliar_media).grid(column=1, row=7, sticky="w")
        ttk.Label(fluxo_frame, text="↡ :").grid(column=0, row=8, sticky="e")
        ttk.Label(fluxo_frame, textvariable=self.fluxo_via_auxiliar_baixo).grid(column=1, row=8, sticky="w")
        ttk.Label(fluxo_frame, text="↟ :").grid(column=0, row=9, sticky="e")
        ttk.Label(fluxo_frame, textvariable=self.fluxo_via_auxiliar_cima).grid(column=1, row=9, sticky="w")

        # Dentro do quadrado Velocidade Média (km/h)
        velocidade_frame = ttk.LabelFrame(info_frame, text="Velocidade Média (km/h)")
        velocidade_frame.grid(column=1, row=0, padx=10, pady=5, sticky="w")

        # Adicione uma linha divisória horizontal após a etiqueta "Via Principal ⇄"
        ttk.Separator(velocidade_frame, orient="horizontal").grid(column=0, row=0, columnspan=2, sticky="ew")

        # Configurar centralização dos itens na coluna 0 e 1
        velocidade_frame.columnconfigure(0, weight=1)  # Centraliza a coluna 0
        velocidade_frame.columnconfigure(1, weight=1)  # Centraliza a coluna 1

        # Labels centralizados
        ttk.Label(velocidade_frame, text="Via Principal ⇄").grid(column=0, row=1, columnspan=2, sticky="n")
        ttk.Label(velocidade_frame, text="Média:").grid(column=0, row=2, sticky="e")
        ttk.Label(velocidade_frame, textvariable=self.velocidade_via_principal_media).grid(column=1, row=2, sticky="w")
        ttk.Label(velocidade_frame, text="↠ :").grid(column=0, row=3, sticky="e")
        ttk.Label(velocidade_frame, textvariable=self.velocidade_via_principal_dir).grid(column=1, row=3, sticky="w")
        ttk.Label(velocidade_frame, text="↞ :").grid(column=0, row=4, sticky="e")
        ttk.Label(velocidade_frame, textvariable=self.velocidade_via_principal_esq).grid(column=1, row=4, sticky="w")

        # Adicione uma linha divisória horizontal após a etiqueta "Via Auxiliar ⇅"
        ttk.Separator(velocidade_frame, orient="horizontal").grid(column=0, row=5, columnspan=2, sticky="ew")

        # Configurar centralização dos itens na coluna 0 e 1
        velocidade_frame.columnconfigure(0, weight=1)  # Centraliza a coluna 0
        velocidade_frame.columnconfigure(1, weight=1)  # Centraliza a coluna 1

        # Labels centralizados
        ttk.Label(velocidade_frame, text="Via Auxiliar ⇅").grid(column=0, row=6, columnspan=2, sticky="n")
        ttk.Label(velocidade_frame, text="Média:").grid(column=0, row=7, sticky="e")
        ttk.Label(velocidade_frame, textvariable=self.velocidade_via_auxiliar_media).grid(column=1, row=7, sticky="w")
        ttk.Label(velocidade_frame, text="↡ :").grid(column=0, row=8, sticky="e")
        ttk.Label(velocidade_frame, textvariable=self.velocidade_via_auxiliar_baixo).grid(column=1, row=8, sticky="w")
        ttk.Label(velocidade_frame, text="↟ :").grid(column=0, row=9, sticky="e")
        ttk.Label(velocidade_frame, textvariable=self.velocidade_via_auxiliar_cima).grid(column=1, row=9, sticky="w")

        # Quadrado Infrações
        infra_frame = ttk.LabelFrame(info_frame, text="Infrações")
        infra_frame.grid(column=2, row=0, padx=10, pady=5, sticky="w")

        # Adicione uma linha divisória horizontal após a etiqueta "Infrações"
        ttk.Separator(infra_frame, orient="horizontal").grid(column=0, row=1, columnspan=2, sticky="ew")

        # Configurar peso da coluna 0 para centralizar horizontalmente
        infra_frame.columnconfigure(0, weight=1)

        ttk.Label(infra_frame, text="Total:").grid(column=0, row=0, sticky="e")
        ttk.Label(infra_frame, textvariable=self.total_infracoes).grid(column=1, row=0, sticky="w")
        ttk.Label(infra_frame, text="Avanço de Sinal:").grid(column=0, row=2, sticky="e")
        ttk.Label(infra_frame, textvariable=self.avanco_sinal_infracoes).grid(column=1, row=2, sticky="w")
        ttk.Label(infra_frame, text="Velocidade Acima da Permitida:").grid(column=0, row=3, sticky="e")
        ttk.Label(infra_frame, textvariable=self.velocidade_infracoes).grid(column=1, row=3, sticky="w")

        # Quadrado de Controles
        self.modo_controle = tk.StringVar()
        #self.modo_controle.set("diurno")  #Caso queira começar o programa com um modo já estabelecido

        control_frame = ttk.LabelFrame(root, text="Controles")
        control_frame.grid(column=0, row=1, columnspan=2, padx=10, pady=5)

        # Botões de Modo de Controle
        ttk.Radiobutton(control_frame, text="Modo Diurno", variable=self.modo_controle, value="diurno", command=self.ativar_modo_diurno).grid(column=0, row=0, padx=10, pady=5, sticky="ew")
        ttk.Radiobutton(control_frame, text="Modo de Emergência", variable=self.modo_controle, value="emergencia", command=self.ativar_modo_emergencia).grid(column=1, row=0, padx=10, pady=5, sticky="ew")
        ttk.Radiobutton(control_frame, text="Modo Noturno", variable=self.modo_controle, value="noturno", command=self.ativar_modo_noturno).grid(column=2, row=0, padx=10, pady=5, sticky="ew")

        # Adicione descrições dos botões de controle quebrando a linha
        ttk.Label(control_frame, text="Realiza o funcionamento normal das vias.", wraplength=220,
                  anchor="w", justify="left").grid(column=0, row=2, padx=10, pady=5, sticky="w")
        ttk.Label(control_frame, text="Liberar o fluxo de trânsito em uma via (os dois cruzamentos com a via principal em verde).", wraplength=220,
                  anchor="w", justify="left").grid(column=1, row=2, padx=10, pady=5, sticky="w")
        ttk.Label(control_frame, text="Fazer o sinal amarelo piscar em todos os cruzamentos.", wraplength=220,
                  anchor="w", justify="left").grid(column=2, row=2, padx=10, pady=5, sticky="w")

        # Inicializar informações
        self.atualizar_informacoes(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)

        
        # Adicione uma barra de rolagem ao terminal
        scrollbar = ttk.Scrollbar(terminal_frame, orient="vertical", command=self.terminal_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Associe a barra de rolagem ao widget de texto
        self.terminal_text.config(yscrollcommand=scrollbar.set)

        # Botão para limpar as mensagens do terminal
        ttk.Button(terminal_frame, text="Limpar Terminal", command=self.limpar_terminal).grid(row=0, column=2, padx=10, pady=5)

    def atualizar_informacoes(self, fluxo_via_principal_media, fluxo_via_principal_dir, fluxo_via_principal_esq,
                             fluxo_via_auxiliar_media, fluxo_via_auxiliar_baixo, fluxo_via_auxiliar_cima,
                             velocidade_via_principal_media, velocidade_via_principal_dir, velocidade_via_principal_esq,
                             velocidade_via_auxiliar_media, velocidade_via_auxiliar_baixo, velocidade_via_auxiliar_cima,
                             total_infracoes, avanco_sinal_infracoes, velocidade_infracoes):
        self.fluxo_via_principal_media.set(f"{fluxo_via_principal_media:.2f}")
        self.fluxo_via_principal_dir.set(f"{fluxo_via_principal_dir:.2f}")
        self.fluxo_via_principal_esq.set(f"{fluxo_via_principal_esq:.2f}")
        self.fluxo_via_auxiliar_media.set(f"{fluxo_via_auxiliar_media:.2f}")
        self.fluxo_via_auxiliar_baixo.set(f"{fluxo_via_auxiliar_baixo:.2f}")
        self.fluxo_via_auxiliar_cima.set(f"{fluxo_via_auxiliar_cima:.2f}")
        self.velocidade_via_principal_media.set(f"{velocidade_via_principal_media:.2f}")
        self.velocidade_via_principal_dir.set(f"{velocidade_via_principal_dir:.2f}")
        self.velocidade_via_principal_esq.set(f"{velocidade_via_principal_esq:.2f}")
        self.velocidade_via_auxiliar_media.set(f"{velocidade_via_auxiliar_media:.2f}")
        self.velocidade_via_auxiliar_baixo.set(f"{velocidade_via_auxiliar_baixo:.2f}")
        self.velocidade_via_auxiliar_cima.set(f"{velocidade_via_auxiliar_cima:.2f}")
        self.total_infracoes.set(total_infracoes)
        self.avanco_sinal_infracoes.set(avanco_sinal_infracoes)
        self.velocidade_infracoes.set(velocidade_infracoes)

    def run_server(self):
        # Inicialize o servidor socket aqui
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('127.0.0.1', 57858))
        server_socket.listen(5)  # Aceita até 5 conexões em espera

        self.adicionar_mensagem_terminal("Servidor inicializado com sucesso...")

        # ... (código anterior do servidor)

    def run_server(self):
        # Inicialize o servidor socket aqui
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)  # Aceita até 5 conexões em espera

        self.adicionar_mensagem_terminal("Servidor inicializado com sucesso...")

        while True:
            if len(self.client_sockets) < 5:
                # Aguardando uma conexão do cliente
                self.adicionar_mensagem_terminal("Aguardando conexão do(s) cruzamento(s)...")
                client, addr = server_socket.accept()

                # Adiciona o socket do cliente à lista
                self.client_sockets.append((client, addr))
                self.adicionar_mensagem_terminal(f"Cliente conectado: {addr}")

                # Leia e exiba a mensagem enviada pelo cliente
                message = client.recv(1024).decode()
                self.adicionar_mensagem_terminal(f"{message}")

            # Verifique as conexões dos clientes
            disconnected_clients = []
            for client_socket, addr in self.client_sockets:
                try:
                    # Tente receber uma pequena quantidade de dados para verificar se o cliente ainda está conectado
                    data = client_socket.recv(1)
                    if not data:
                        disconnected_clients.append((client_socket, addr))
                except Exception as e:
                    disconnected_clients.append((client_socket, addr))

            # Remova os clientes desconectados da lista
            for client_socket, addr in disconnected_clients:
                self.client_sockets.remove((client_socket, addr))
                self.adicionar_mensagem_terminal(f"Cliente desconectado: {addr}\n")
                client_socket.close()

    def adicionar_mensagem_terminal(self, mensagem):
        # Certifique-se de que o widget Text exista antes de inserir a mensagem
        if hasattr(self, 'terminal_text'):
            # Agende a exibição da mensagem com um pequeno atraso
            self.root.after(1000, self._exibir_mensagem_terminal, mensagem)

    def _exibir_mensagem_terminal(self, mensagem):
        # Insira a mensagem no widget Text e role para a última linha
        self.terminal_text.insert(tk.END, mensagem + "\n")
        self.terminal_text.see(tk.END)

    def ativar_modo_diurno(self):
        mensagem = "Modo Diurno ativado."
        self.adicionar_mensagem_terminal(mensagem)
        if os.path.exists("modo_diurno.py"):
            exec(open("modo_diurno.py").read())

    def ativar_modo_emergencia(self):
        mensagem = "Modo de Emergência ativado."
        self.adicionar_mensagem_terminal(mensagem)
        if os.path.exists("modo_emergencia.py"):
            exec(open("modo_emergencia.py").read())

    def ativar_modo_noturno(self):
        mensagem = "Modo Noturno ativado."
        self.adicionar_mensagem_terminal(mensagem)
        if os.path.exists("modo_noturno.py"):
            exec(open("modo_noturno.py").read())

    def limpar_terminal(self):
        # Limpa o conteúdo existente no terminal
        self.terminal_text.delete("1.0", tk.END)

def start_server(app):
    app.run_server()

def main():
    root = tk.Tk()
    app = TrafficControlTerminal(root)

    # Crie uma thread para executar o servidor
    server_thread = threading.Thread(target=start_server, args=(app,))
    server_thread.daemon = True
    server_thread.start()

    root.mainloop()

if __name__ == "__main__":
    main()