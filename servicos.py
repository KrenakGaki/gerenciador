import subprocess
import threading
import tkinter as tk
from tkinter import messagebox

# Lista fixa dos Serviços Gestores (nomes internos)
servicos = [
    "RestDWsrv","RestDWsrvBIServiceGestores", "_GestoresFood_Service", "_SrvGestoresScanntech",
    "_SrvApiCatalogoDigital", "_SrvGestoresPilar", "_SrvGestoresDominioSistemas",
    "_SrvGestoresMegaLista", "BrGestoresApi", "_Gestores_Smart_POS_RELEASE",
    "_SrvPdvGestoresService", "postgresql-x64-12"
]

# Processos que devem ser finalizados ao parar todos
processes_to_kill = [
    "AutoFood.exe", "backup.exe", "BuscaPreco.exe", "Coletor.exe",
    "ConfiguraGestorPDV.exe", "GestorBalcao.exe", "Gestores.exe",
    "GestorPDV.exe", "ManifestacaoDocumentos.exe", "Migrador.exe", "Migrador_filial.exe",
    "MonitorPosto.exe", "MonitorPrinter.exe", "PedidoZap.exe", "pg_dump.exe",
    "pg_restore.exe", "PgMaestro.exe", "Restaurador.exe", "Servidor.exe",
    "SincData.exe", "Sintegra.exe", "Sped_Contribuicoes.exe", "Sped_Fiscal.exe",
    "StartMDe2.exe", "StartSincData.exe", "SvrPedidoMob.exe", "WhatsAppMSG.exe",
    "MonitorEasyInner.exe"
]

def executar_servico(nome_servico, acao):
    try:
        subprocess.run(["net", acao, nome_servico], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass

def taskkill_processo(proc):
    subprocess.run(["taskkill", "/F", "/IM", proc], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def iniciar_todos():
    # Executa todos os serviços em threads separadas
    for nome_servico in servicos:
        threading.Thread(target=executar_servico, args=(nome_servico, "start")).start()
    messagebox.showinfo("Sucesso", "Processo concluído.")

def parar_todos():
    # Para todos exceto PostgreSQL
    for nome_servico in servicos:
        if nome_servico != "postgresql-x64-12":
            threading.Thread(target=executar_servico, args=(nome_servico, "stop")).start()

    # Reinicia PostgreSQL
    threading.Thread(target=executar_servico, args=("postgresql-x64-12", "stop")).start()
    threading.Thread(target=executar_servico, args=("postgresql-x64-12", "start")).start()

    # Finaliza processos relacionados em threads
    for proc in processes_to_kill:
        threading.Thread(target=taskkill_processo, args=(proc,)).start()

    messagebox.showinfo("Sucesso", "Processo concluído.")