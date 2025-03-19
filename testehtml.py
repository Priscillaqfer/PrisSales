import tkinter as tk
from tkinterhtml import HtmlFrame

root = tk.Tk()
root.title("Exibindo HTML no Tkinter")

frame = HtmlFrame(root)
frame.pack(fill="both", expand=True)

# Exibindo HTML básico
frame.set_content("<h1>Olá, Mundo!</h1><p>Isso é um texto em <b>HTML</b> no tkinter.</p>")

root.mainloop()
