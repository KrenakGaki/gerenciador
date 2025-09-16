import customtkinter as ctk
from servicos import iniciar_todos, parar_todos
from reiniciar_postgres import reiniciar_postgres
from variavelpath import adicionar_ao_path
from crash_postgres import parar_postgres_thread
from apagar_postmaster import apagar_postmaster
from permissoes_postgres import adicionar_permissoes
from portas_sistemas import liberacao_portas
import psutil
import ctypes

# Verifica se é admin
if not ctypes.windll.shell32.IsUserAnAdmin():
    import sys
    import os
    # Reexecuta o script como administrador
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, " ".join(sys.argv), None, 1
    )
    sys.exit()

# --- Configuração do tema ---
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# --- Janela principal ---
root = ctk.CTk()
root.title("Gerenciador de Serviços 2.9")
root.geometry("340x500+800+300")
root.resizable(False, False)
root.bind("<Escape>", lambda e: root.destroy())

# --- Função para criar botões padronizados ---
def criar_botao(frame, texto, comando):
    return ctk.CTkButton(frame,
                        text=texto,
                        command=comando,
                        width=150,
                        height=40,
                        corner_radius=12,
                        font=("Arial", 12, "bold"),
                        fg_color="#3A7CA5",
                        hover_color="#569CD6",
                        text_color="white")

# --- Função para criar frames com grid interno ---
def criar_frame_grid(nome):
    frame = ctk.CTkFrame(root, corner_radius=10)
    frame.pack(padx=10, pady=10, fill="x")

    titulo = ctk.CTkLabel(frame, text=nome, anchor="w", font=("Arial", 13, "bold"))
    titulo.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    # Padroniza as colunas para expandirem igualmente
    frame.grid_columnconfigure(0, weight=1)
    frame.grid_columnconfigure(1, weight=1)
    return frame

# --- Frames ---
frame_servicos = criar_frame_grid("Serviços Gerais")
frame_postgres = criar_frame_grid("PostgreSQL")
frame_portas = criar_frame_grid("Sistema de Portas")

# --- Botões Serviços Gerais ---
btn_iniciar = criar_botao(frame_servicos, "Iniciar Todos", iniciar_todos)
btn_iniciar.grid(row=1, column=0, padx=5, pady=3, sticky="ew")

btn_parar = criar_botao(frame_servicos, "Parar Todos", parar_todos)
btn_parar.grid(row=1, column=1, padx=5, pady=3, sticky="ew")

# --- Botões PostgreSQL ---
btn_parar_pg = criar_botao(frame_postgres, "Parar PostgreSQL", parar_postgres_thread)
btn_parar_pg.grid(row=1, column=0, padx=5, pady=3, sticky="ew")

btn_reiniciar_pg = criar_botao(frame_postgres, "Reiniciar PostgreSQL", reiniciar_postgres)
btn_reiniciar_pg.grid(row=1, column=1, padx=5, pady=5, sticky="ew")

btn_manutencao = criar_botao(frame_postgres, "Manutenção", lambda: abrir_opcoes_extras())
btn_manutencao.grid(row=2, column=0, columnspan=2, padx=3, pady=15, sticky="ew")


# --- Janela de manutenção ---
def abrir_opcoes_extras():
    janela = ctk.CTkToplevel(root)
    janela.title("Manutenção do PostgreSQL")
    janela.geometry("220x230+575+545")
    janela.resizable(False, False)
    janela.transient(root)
    janela.grab_set()
    janela.focus_set()
    janela.bind("<Escape>", lambda e: janela.destroy())  # <-- Fecha com Esc

    janela.grid_columnconfigure(0, weight=1)

    btn_path = criar_botao(janela, "Adicionar ao PATH", adicionar_ao_path)
    btn_path.grid(row=0, column=0, padx=20, pady=5, sticky="ew")

    btn_permissoes = criar_botao(janela, "Permissões do PostgreSQL", lambda: adicionar_permissoes(root))
    btn_permissoes.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

    btn_postmaster = criar_botao(janela, "Apagar Postmaster", apagar_postmaster)
    btn_postmaster.grid(row=2, column=0, padx=20, pady=5, sticky="ew")

    btn_fechar = criar_botao(janela, "Fechar", janela.destroy)
    btn_fechar.grid(row=3, column=0, padx=20, pady=15, sticky="ew")

def janela_verificar_porta():
    def checar(event=None):
        porta = entry_porta.get()
        try:
            porta_int = int(porta)
        except ValueError:
            resultado_label.configure(text="Porta inválida!", text_color="red")
            return

        for conn in psutil.net_connections():
            if conn.laddr and conn.laddr.port == porta_int:
                pid = conn.pid
                if pid:
                    try:
                        proc = psutil.Process(pid)
                        nome = proc.name()
                        resultado_label.configure(
                            text=f"Porta {porta} usada por: {nome} (PID: {pid})",
                            text_color="#FFD700"
                        )
                    except Exception:
                        resultado_label.configure(
                            text=f"Porta {porta} usada por PID {pid}, nome não disponível.",
                            text_color="#FFD700"
                        )
                else:
                    resultado_label.configure(
                        text=f"Porta {porta} em uso, processo não identificado.",
                        text_color="#FFD700"
                    )
                return
        resultado_label.configure(text=f"Porta {porta} está livre.", text_color="#00FF00")

    janela = ctk.CTkToplevel(master=root)
    janela.title("Verificar Porta")
    janela.geometry("340x200+455+300")
    janela.resizable(False, False)
    janela.transient(root)
    janela.grab_set()
    janela.focus_set()
    janela.bind("<Escape>", lambda e: janela.destroy())  # <-- Fecha com Esc

    frame_interno = ctk.CTkFrame(janela, corner_radius=10)
    frame_interno.pack(expand=True, fill="both", padx=15, pady=15)

    ctk.CTkLabel(frame_interno, text="Digite a porta:", font=("Arial", 13, "bold")).pack(pady=(10, 5))

    entry_porta = ctk.CTkEntry(frame_interno, width=120, font=("Arial", 12))
    entry_porta.pack(pady=5)
    entry_porta.bind("<Return>", checar)
    janela.after(100, entry_porta.focus_set)

    btn_checar = ctk.CTkButton(
        frame_interno,
        text="Verificar",
        command=checar,
        width=120,
        height=36,
        corner_radius=10,
        font=("Arial", 12, "bold"),
        fg_color="#3A7CA5",
        hover_color="#569CD6",
        text_color="white"
    )
    btn_checar.pack(pady=10)

    resultado_label = ctk.CTkLabel(frame_interno, text="", font=("Arial", 12))
    resultado_label.pack(pady=10)

# Exemplo de botão para criar regras de firewall
btn_verificar_porta = criar_botao(frame_portas, "Verificar Porta", janela_verificar_porta)
btn_verificar_porta.grid(row=4, column=0, padx=5, pady=5, sticky="ew")

btn_liberar_porta = criar_botao(frame_portas, "Não Funciona", None)
btn_liberar_porta.grid(row=4, column=1, padx=5, pady=5, sticky="ew") 

btn_firewall = criar_botao(frame_portas, "Liberação de Portas", lambda: liberacao_portas(root))
btn_firewall.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="ew") 


# --- Botão sair ---
btn_sair = criar_botao(root, "Sair", root.quit)
btn_sair.pack(pady=10)

root.mainloop()