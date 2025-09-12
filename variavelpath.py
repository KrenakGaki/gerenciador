import os
import tkinter as tk
from tkinter import messagebox
import subprocess

def adicionar_ao_path():

    try:
        postgres_path = [r"C:\Program Files\PostgreSQL\12\data",
                            r"C:\Program Files\PostgreSQL\12\bin",
                            r"C:\Program Files\PostgreSQL\12",
                            r"C:\Program Files\PostgreSQL\9.2\data",
                            r"C:\Program Files\PostgreSQL\9.2\bin",
                            r"C:\Program Files\PostgreSQL\9.2",
                            r"C:\Program Files (x86)\PostgreSQL\9.2\data",
                            r"C:\Program Files (x86)\PostgreSQL\9.2\bin",
                            r"C:\Program Files (x86)\PostgreSQL\9.2"]
        
        #Path atual do sistema
        current_path = os.environ.get('PATH', '')

        # Adiciona os caminhos do PostgreSQL ao PATH se não estiverem presentes
        novo_path = ";".join(postgres_path) + ";" + current_path

        #Define o novo PATH
        subprocess.run(["setx", "PATH", novo_path], shell=True)

        os.environ['PATH'] = novo_path

        messagebox.showinfo("Sucesso", "Caminhos do PostgreSQL adicionados ao PATH do sistema.")   

    except subprocess.CalledProcessError as e:
        messagebox.showerror("Erro", f"Falha ao adicionar ao PATH.\n\n{e}")