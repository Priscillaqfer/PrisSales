import tkinter as tk
import os
from tkinter import messagebox
from supabase import create_client, Client
from dotenv import load_dotenv

# Configurações do Supabase
load_dotenv('python.env')

# Obter a URL e a chave do Supabase
url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

# Criar cliente do Supabase
supabase: Client = create_client(url, key)

# Função para cadastrar usuário
def cadastrar_usuario():
    cpf_cnpj = entry_cpf_cnpj.get()
    nome = entry_nome.get()
    email = entry_email.get()

    if nome and email and cpf_cnpj:
        try:
            # Insere os dados no Supabase
            response = supabase.table('Clientes').insert({
                "cpf_cnpj": cpf_cnpj,
                "nome": nome,
                "email": email,
            }).execute()

            if response.data:
                messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
                # Limpa os campos após o cadastro
                entry_cpf_cnpj.delete(0, tk.END)
                entry_nome.delete(0, tk.END)
                entry_email.delete(0, tk.END)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao cadastrar: {str(e)}")
    else:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")

# Interface gráfica
janela = tk.Tk()
janela.title("Cadastro de Usuários")

# Campos de entrada

tk.Label(janela, text="CPF/CNPJ:").grid(row=2, column=0, padx=10, pady=10)
entry_cpf_cnpj = tk.Entry(janela)  # Campo CPF/CNPJ
entry_cpf_cnpj.grid(row=2, column=1, padx=10, pady=10)

tk.Label(janela, text="Nome:").grid(row=0, column=0, padx=10, pady=10)
entry_nome = tk.Entry(janela)
entry_nome.grid(row=0, column=1, padx=10, pady=10)

tk.Label(janela, text="E-mail:").grid(row=1, column=0, padx=10, pady=10)
entry_email = tk.Entry(janela)
entry_email.grid(row=1, column=1, padx=10, pady=10)


# Botão de cadastro
btn_cadastrar = tk.Button(janela, text="Cadastrar", command=cadastrar_usuario)
btn_cadastrar.grid(row=3, column=0, columnspan=2, pady=10)

# Inicia a interface
janela.mainloop()