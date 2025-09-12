from tkinter import messagebox
import win32serviceutil
import win32api, win32con
import psutil
import threading
from servicos import servicos, processes_to_kill

def taskkill_processo(proc_name):
    for proc in psutil.process_iter(attrs=["pid","name"]):
        if proc.info["name"].lower() == proc_name.lower():
            try:
                handle = win32api.OpenProcess(win32con.PROCESS_TERMINATE, False, proc.info["pid"])
                win32api.TerminateProcess(handle, -1)
                win32api.CloseHandle(handle)
            except Exception as e:
                print(f"Erro ao finalizar {proc_name}: {e}")