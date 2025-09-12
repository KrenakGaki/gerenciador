import psutil

def verificar_porta(porta):
    porta = int(porta)
    for conn in psutil.net_connections():
        if conn.laddr and conn.laddr.port == porta:
            pid = conn.pid
            if pid:
                try:
                    proc = psutil.Process(pid)
                    nome = proc.name()
                    print(f"Porta {porta} está sendo usada pelo processo: {nome} (PID: {pid})")
                except Exception as e:
                    print(f"Porta {porta} está sendo usada por PID {pid}, mas não foi possível obter o nome do processo.")
            else:
                print(f"Porta {porta} está em uso, mas não foi possível identificar o processo.")
            return
    print(f"Porta {porta} está livre.")

# Exemplo de uso:
if __name__ == "__main__":
    porta = input("Digite a porta para verificar: ")
    verificar_porta(porta)