import tkinter as tk
from tkinter import messagebox
from servicos  import iniciar_todos, parar_todos 
from post import reinicio_postgres

root = tk.Tk()
root.title("Gerenciador de Serviços Gestores")
root.geometry("300x200")

tk.Button(root, text="Iniciar Todos", command=iniciar_todos, width=25).pack(pady=10)
tk.Button(root, text="Parar Todos", command=parar_todos, width=25).pack(pady=10)
tk.Button(root, text="Reiniciar PostgreSQL", command=reinicio_postgres, width=25).pack(pady=10)

root.mainloop() 