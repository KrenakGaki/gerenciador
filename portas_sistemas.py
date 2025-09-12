import subprocess
import threading

# Lista de regras de Firewall
REGRAS_FIREWALL = [
    {"sistema": "GESTORES", "porta": 5432, "protocolo": ["TCP", "UDP"]},
    {"sistema": "SINCDATA", "porta": 8082, "protocolo": ["TCP", "UDP"]},
    {"sistema": "GESTOR FOOD", "porta": 8090, "protocolo": ["TCP", "UDP"]},
    {"sistema": "FORCA DE VENDA", "porta": 9191, "protocolo": ["TCP", "UDP"]},
    {"sistema": "BALCAO MOBILE", "porta": 8081, "protocolo": ["TCP", "UDP"]},
    {"sistema": "GESTORES UTILITARIOS", "porta": 9000, "protocolo": ["TCP", "UDP"]},
]

def criar_regras_firewall():
    def worker():
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
                    except subprocess.CalledProcessError:
                        pass

    threading.Thread(target=worker, daemon=True).start()

if __name__ == "__main__":
    criar_regras_firewall()
