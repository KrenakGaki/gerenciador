import threading
import time
import tkinter as tk
from tkinter import messagebox
import win32serviceutil
import win32api, win32con
import psutil

# Serviços
servicos = [
    "RestDWsrv","RestDWsrvBIServiceGestores", "_GestoresFood_Service", "_SrvGestoresScanntech",
    "_SrvApiCatalogoDigital", "_SrvGestoresPilar", "_SrvGestoresDominioSistemas", "_Gestores_Auth_HOMOLOGATION",
    "_SrvGestoresMegaLista", "BrGestoresApi", "_Gestores_Smart_POS_RELEASE","_Gestores_Auth_RELEASE",
    "_SrvPdvGestoresService", "postgresql-x64-12", "postgresql-x64-9.2", "postgresql-x86-9.2"
]

# Processos
processes_to_kill = [
    "AutoFood.exe","backup.exe","BuscaPreco.exe","Coletor.exe",
    "ConfiguraGestorPDV.exe","GestorBalcao.exe","Gestores.exe", "pg_admin.exe",
    "GestorPDV.exe","ManifestacaoDocumentos.exe","Migrador.exe","Migrador_filial.exe",
    "MonitorPosto.exe","MonitorPrinter.exe","PedidoZap.exe","pg_dump.exe",
    "pg_restore.exe","PgMaestro.exe","Restaurador.exe","Servidor.exe",
    "SincData.exe","Sintegra.exe","Sped_Contribuicoes.exe","Sped_Fiscal.exe",
    "StartMDe2.exe","StartSincData.exe","SvrPedidoMob.exe","WhatsAppMSG.exe",
    "MonitorEasyInner.exe", "ServerNFCe.exe"
    ]

# Inicia/para serviços
def executar_servico(nome_servico, acao): 
    try:
        if acao == "start":
            win32serviceutil.StartService(nome_servico)
        elif acao == "stop":
            win32serviceutil.StopService(nome_servico)
    except Exception as e:
        print(f"Erro ao {acao} serviço {nome_servico}: {e}")

# Mata processos
def taskkill_processo(proc_name):
    for proc in psutil.process_iter(attrs=["pid","name"]):
        if proc.info["name"].lower() == proc_name.lower():
            try:
                handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, proc.info["pid"])
                win32api.TerminateProcess(handle, -1)
                win32api.CloseHandle(handle)
            except Exception as e:
                print(f"Erro ao finalizar {proc_name}: {e}")

# Iniciar todos
def iniciar_todos():
    for nome_servico in servicos:
        threading.Thread(target=executar_servico, args=(nome_servico, "start")).start()
    messagebox.showinfo("Sucesso", "Processo concluído.")

# Parar todos
def parar_todos():
    # Para todos os serviços exceto PostgreSQL
    for nome_servico in servicos:
        if "postgresql" not in nome_servico.lower():
            threading.Thread(target=executar_servico, args=(nome_servico, "stop")).start()

    # Reinicia PostgreSQL de forma controlada
    def reiniciar_postgres():
        try:
            # Para o PostgreSQL
            executar_servico("postgresql-x64-12", "stop")

            # Aguarda até o serviço realmente parar
            while True:
                status = win32serviceutil.QueryServiceStatus("postgresql-x64-12")[1]
                # 1 = parado, 4 = rodando
                if status == 1:
                    break
                time.sleep(0.5)

            # Inicia o PostgreSQL
            executar_servico("postgresql-x64-12", "start")
        except Exception as e:
            print(f"Erro ao reiniciar PostgreSQL: {e}")

    threading.Thread(target=reiniciar_postgres).start()

    # Finaliza processos em paralelo
    for proc in processes_to_kill:
        threading.Thread(target=taskkill_processo, args=(proc,)).start()

    messagebox.showinfo("Sucesso", "Processo concluído.")