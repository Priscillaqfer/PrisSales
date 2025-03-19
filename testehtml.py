import tkinter as tk
from tkhtmlview import HTMLLabel

# Criar janela principal
root = tk.Tk()
root.title("Exibindo HTML no Tkinter")
root.geometry("400x300")  # Define o tamanho da janela

# Criar um widget que suporta HTML
html_label = HTMLLabel(root, html="""
    <h1 style='color: blue;'>Olá, Mundo!</h1>
    <p>Isso é um texto em <b>HTML</b> dentro do Tkinter.</p>
    <p style='color: red;'>Suporta <i>CSS inline</i> e <b>negrito</b>.</p>
""")
html_label.pack(padx=10, pady=10, fill="both", expand=True)

# Iniciar a interface
root.mainloop()
