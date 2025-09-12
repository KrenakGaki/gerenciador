import subprocess
import threading
import ctypes
from tkinter import messagebox
from apagar_postmaster import datas_postgres


permissoes = [
    ("S-1-5-20", "(OI)(CI)F"),                  # Serviço de rede
    (r"NT AUTHORITY\SYSTEM", "(OI)(CI)F"),     # Sistema
    ("*S-1-5-32-544", "(OI)(CI)F"),            # Administradores
    (r"NT SERVICE\TrustedInstaller", "(OI)(CI)F"),  # TrustedInstaller
    ("*S-1-5-19", "(OI)(CI)F")                 # Usuários de serviço
]


def adicionar_permissoes(root):
    def tarefa():
        relatorio = []
        try:
            for pasta in datas_postgres:
                for usuario, permissao in permissoes:
                    cmd = f'icacls "{pasta}" /grant:r {usuario}:{permissao} /t /q'
                    subprocess.run(cmd, shell=True, check=True)
                    relatorio.append(f"Permissão {permissao} concedida para {usuario} em {pasta} para {usuario} em {pasta} aplicada com sucesso.")
        except subprocess.ChildProcessError as e:
            relatorio.append(f"Erro ao aplicar permissão {permissao} para {usuario} em {pasta}: {e}")
                
        messagebox.showinfo("Relatório de Permissões", "\n".join(relatorio))

        if not ctypes.windll.shell32.IsUserAnAdmin():
            messagebox.showwarning("Permissão Negada", "É necessário executar como administrador para alterar permissões do PostgreSQL.")
            return
    
        threading.Thread(target=tarefa, daemon=True).start()