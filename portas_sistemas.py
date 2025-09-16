import subprocess
import threading
from tkinter import messagebox
from customtkinter import CTkToplevel, CTkTextbox

# Lista de regras de Firewall
REGRAS_FIREWALL = [
    {"sistema": "GESTORES", "porta": 5432, "protocolo": ["TCP", "UDP"]},
    {"sistema": "SINCDATA", "porta": 8082, "protocolo": ["TCP", "UDP"]},
    {"sistema": "GESTOR FOOD", "porta": 8090, "protocolo": ["TCP", "UDP"]},
    {"sistema": "FORCA DE VENDA", "porta": 9191, "protocolo": ["TCP", "UDP"]},
    {"sistema": "BALCAO MOBILE", "porta": 8081, "protocolo": ["TCP", "UDP"]},
    {"sistema": "GESTORES UTILITARIOS", "porta": 9000, "protocolo": ["TCP", "UDP"]},
]

def liberacao_portas(root):
    def worker():
        relatorio = []
        sucesso = True
        portas_adicionadas = []

        for regra in REGRAS_FIREWALL:
            nome_base = regra["sistema"]
            porta = regra["porta"]
            for protocolo in regra["protocolo"]:
                for direcao in ["in", "out"]:
                    nome = f"BRAJAN SISTEMAS {nome_base} {protocolo} {'ENTRADA' if direcao=='in' else 'SAIDA'}"
                    
                    # Verifica se a regra já existe
                    resultado = subprocess.run(
                        ["netsh", "advfirewall", "firewall", "show", "rule", f"name={nome}"],
                        capture_output=True, text=True
                    )
                    if "Não foram encontradas regras" not in resultado.stdout:
                        relatorio.append(f"Regra já existe: {nome}")
                        continue

                    # Cria a regra
                    comando = [
                        "netsh", "advfirewall", "firewall", "add", "rule",
                        f'name={nome}',
                        f"dir={direcao}",
                        "action=allow",
                        f"protocol={protocolo}",
                        f"localport={porta}"
                    ]
                    try:
                        subprocess.run(comando, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                        relatorio.append(f"Regra criada: {nome} - Porta {porta}/{protocolo} [{direcao}]")
                        portas_adicionadas.append(f"{nome} - Porta {porta}/{protocolo} [{direcao}]")
                    except subprocess.CalledProcessError as e:
                        relatorio.append(f"Erro ao criar regra {nome}: {e}")
                        sucesso = False

        def mostrar_resultado():
            # Mensagem de sucesso/erro
            if sucesso:
                messagebox.showinfo("Firewall", "Todas as regras foram aplicadas com sucesso!")
            else:
                messagebox.showwarning("Firewall", "Algumas regras não foram aplicadas corretamente.")

            # Janela com relatório das portas adicionadas
            janela = CTkToplevel(root)
            janela.title("Portas Adicionadas ao Firewall")
            janela.geometry("400x350")
            texto = CTkTextbox(janela, width=380, height=300)
            texto.pack(padx=10, pady=10)
            texto.insert("end", "\n".join(relatorio))
            texto.configure(state="disabled")

        root.after(0, mostrar_resultado)

    threading.Thread(target=worker, daemon=True).start()
