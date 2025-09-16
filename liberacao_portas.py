import os
import threading
import subprocess
from tkinter import messagebox
from customtkinter import CTkToplevel, CTkTextbox

REGRAS_FIREWALL = [
    {"sistema": "BRAJAN SISTEMAS GESTORES", "porta": 5432, "protocolo": ["TCP", "UDP"]},
    {"sistema": "BRAJAN SISTEMAS SINCDATA", "porta": 8082, "protocolo": ["TCP", "UDP"]},
    {"sistema": "BRAJAN SISTEMAS GESTOR FOOD", "porta": 8090, "protocolo": ["TCP", "UDP"]},
    {"sistema": "BRAJAN SISTEMAS FORCA DE VENDA", "porta": 9191, "protocolo": ["TCP", "UDP"]},
    {"sistema": "BRAJAN SISTEMAS BALCAO MOBILE", "porta": 8081, "protocolo": ["TCP", "UDP"]},
    {"sistema": "BRAJAN SISTEMAS GESTORES UTILITARIOS", "porta": 9000, "protocolo": ["TCP", "UDP"]},
]

# Variáveis globais de controle
relatorio = []
sucesso = True

def liberar_regra(sistema, porta, protocolo, direcao):
    global sucesso
    nome_regra = f"{sistema} - {direcao.upper()} - Porta {porta} ({protocolo})"

    check_cmd = f'netsh advfirewall firewall show rule name="{nome_regra}"'
    resultado = subprocess.run(check_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    comando = f'netsh advfirewall firewall add rule name="{nome_regra}" dir={direcao} action=allow protocol={protocolo} localport={porta}'
    resultado = subprocess.run(comando, shell=True)

    if resultado.returncode == 0:
        relatorio.append(f"[OK] {nome_regra}")
    else:
        relatorio.append(f"[ERRO] {nome_regra}")
        sucesso = False

def mostrar_resultado(root):
    janela = CTkToplevel(root)
    janela.title("Portas Adicionadas ao Firewall")
    janela.geometry("480x300+1145+300")
    janela.resizable(False, False)
    janela.focus_set()
    janela.bind("<Escape>", lambda e: janela.destroy())

    texto = CTkTextbox(janela, width=470, height=300)
    texto.pack(padx=5, pady=5)
    texto.insert("end", "\n".join(relatorio))
    texto.configure(state="disabled")

    if sucesso:
        messagebox.showinfo("Firewall", "Todas as regras foram aplicadas com sucesso!")
    else:
        messagebox.showwarning("Firewall", "Algumas regras não foram aplicadas corretamente.")

def criar_regras_firewall(root):
    global relatorio, sucesso
    relatorio = []   # resetar sempre que rodar
    sucesso = True

    def worker():
        threads = []
        for regra in REGRAS_FIREWALL:
            sistema = regra["sistema"]
            porta = regra["porta"]
            for protocolo in regra["protocolo"]:
                for direcao in ["in", "out"]:

                    t = threading.Thread(target=liberar_regra, args=(sistema, porta, protocolo, direcao))
                    threads.append(t)
                    t.start()

        for t in threads:
            t.join()

        # chama o resultado dentro do mainloop do Tkinter
        root.after(0, lambda: mostrar_resultado(root))

    # roda o processo em thread para não travar a UI
    threading.Thread(target=worker, daemon=True).start()
