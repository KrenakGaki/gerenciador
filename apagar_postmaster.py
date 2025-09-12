import ctypes
import threading
from pathlib import Path
from tkinter import messagebox, Tk

datas_postgres = [
    r"C:\Program Files\PostgreSQL\12\data",
    r"C:\Program Files\PostgreSQL\9.2\data",
    r"C:\Program Files (x86)\PostgreSQL\9.2\data"
]

def apagar_postmaster():
    def tarefa():
        relatorio = []
        for data in datas_postgres:
            for arquivo in ["postmaster.opts", "postmaster.pid"]:
                caminho = Path(data) / arquivo
                try:
                    if caminho.exists():
                        caminho.unlink()
                        relatorio.append(f"Arquivo {arquivo} removido de {data}")
                    else:
                        relatorio.append(f"Arquivo {arquivo} não encontrado em {data}")
                except Exception as e:
                    relatorio.append(f"Erro ao remover {arquivo} em {data}: {e}")
        
        # Chama a messagebox na thread principal
        root.after(0, lambda: messagebox.showinfo("Limpeza PostgreSQL", "\n".join(relatorio) + "\n\nProcesso finalizado com sucesso!"))

    if not ctypes.windll.shell32.IsUserAnAdmin():
        messagebox.showwarning("Permissão Negada", "É necessário executar como administrador para apagar arquivos do PostgreSQL.")
        return

    # Cria uma janela oculta apenas para permitir o uso de after()
    root = Tk()
    root.withdraw()
    threading.Thread(target=tarefa, daemon=True).start()
