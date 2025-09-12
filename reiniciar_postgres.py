import threading
import time
from pathlib import Path
import win32serviceutil
import win32service
from tkinter import messagebox

SERVICOS_POSTGRES = [
    "postgresql-x64-12",
    "postgresql-x64-9.2",
    "postgresql-9.2"
]

DATAS_POSTGRES = [
    r"C:\Program Files\PostgreSQL\12\data",
    r"C:\Program Files\PostgreSQL\9.2\data",
    r"C:\Program Files (x86)\PostgreSQL\9.2\data"
]

PASTA_LOGS = "log"

def reiniciar_postgres():
    def tarefa():
        relatorio = []

        for data in DATAS_POSTGRES:
            log_dir = Path(data) / PASTA_LOGS
            if log_dir.exists() and log_dir.is_dir():
                for log_file in log_dir.glob("*.log"):
                    try:
                        log_file.unlink()
                    except Exception as e:
                        relatorio.append(f"Erro ao apagar {log_file.name}: {e}")

        # Reinício/Início dos serviços
        for servico in SERVICOS_POSTGRES:
            try:
                status = win32serviceutil.QueryServiceStatus(servico)[1]
                if status == win32service.SERVICE_RUNNING:
                    win32serviceutil.StopService(servico)
                    time.sleep(1)
                    win32serviceutil.StartService(servico)
                    relatorio.append(f"{servico} reiniciado com sucesso.")
                elif status == win32service.SERVICE_STOPPED:
                    win32serviceutil.StartService(servico)
                    relatorio.append(f"{servico} iniciado com sucesso.")
                else:
                    relatorio.append(f"{servico} em estado {status}, não foi possível reiniciar/iniciar.")
            except Exception as e:
                relatorio.append(f"{servico} falhou: {e}")

        # Apaga arquivos de log

        messagebox.showinfo("Reinício PostgreSQL", "PostgreSQL reiniciado com sucesso!.")

    threading.Thread(target=tarefa, daemon=True).start()
