import subprocess
import threading
import ctypes
from tkinter import messagebox
from customtkinter import CTkToplevel, CTkProgressBar
from apagar_postmaster import datas_postgres

permissoes = [
    (r"NT AUTHORITY\SYSTEM", "(OI)(CI)F"),
    ("*S-1-5-32-544", "(OI)(CI)F"),
    (r"NT SERVICE\TrustedInstaller", "(OI)(CI)F"),
    ("*S-1-5-19", "(OI)(CI)F")
]


def adicionar_permissoes(root):
    if not ctypes.windll.shell32.IsUserAnAdmin():
        messagebox.showwarning("Permissão Negada", "É necessário executar como administrador para alterar permissões do PostgreSQL.")
        return

    janela = CTkToplevel(root)
    janela.title("Progresso das Permissões")
    janela.geometry("320x100+810+835")
    barra = CTkProgressBar(janela, width=250)
    barra.pack(pady=30)
    barra.set(0)

    def tarefa():
        total = len(datas_postgres) * len(permissoes)
        progresso = 0
        relatorio = []
        erro = False

        for pasta in datas_postgres:
            for usuario, permissao in permissoes:
                usuario_formatado = f'"{usuario}"' if " " in usuario else usuario
                cmd = f'icacls "{pasta}" /grant:r {usuario_formatado}:{permissao} /t /q'
                try:
                    subprocess.run(cmd, shell=True, check=True)
                    relatorio.append(f"Permissão {permissao} concedida para {usuario} em {pasta} aplicada com sucesso.")
                except subprocess.CalledProcessError as e:
                    relatorio.append(f"Erro ao aplicar permissão {permissao} para {usuario} em {pasta}: {e}")
                    erro = True
                progresso += 1
                janela.after(0, lambda p=progresso: barra.set(p / total))

        def finalizar():
            janela.destroy()
            messagebox.showinfo("Relatório de Permissões", "\n".join(relatorio))
            if erro:
                messagebox.showwarning("Atenção", "Nem todas as permissões foram aplicadas com sucesso.")
            else:
                messagebox.showinfo("Confirmação", "Permissões aplicadas com sucesso!")

        janela.after(0, finalizar)

    threading.Thread(target=tarefa, daemon=True).start()