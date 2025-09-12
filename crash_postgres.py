import subprocess
import threading
import ctypes
import tkinter as tk 
from tkinter import messagebox

SERVICOS_POSTGRES = [
    "postgresql-x64-12",
    "postgresql-x64-9.2",
    "postgresql-9.2"
]

def parar_postgres_thread():
    """
    Para os serviços do PostgreSQL em thread separada.
    Necessita privilégios de administrador.
    """
    def tarefa():
            for servico in SERVICOS_POSTGRES:
                subprocess.run(
                    ["sc", "stop", servico],
                    check=True,
                    shell=True
                )
            messagebox.showinfo("Sucesso", "Processo concluído.")
    

    # Verifica se é admin
    if not ctypes.windll.shell32.IsUserAnAdmin():
        raise PermissionError("É necessário executar como administrador para parar o PostgreSQL.")

    threading.Thread(target=tarefa, daemon=True).start()
