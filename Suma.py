import tkinter as tk 

def sumar(n):
    if n <= 1 : return 1
    return n + sumar(n-1)

def ejecutar():
    numero = int(entrada.get())
    resultado = sumar(numero)
    resp.config(text=f"El resultado es:{resultado}")

ventana = tk.Tk()
ventana.title("Aplicacion de Suma")
ventana.geometry("340x240")
ventana.minsize(320,220)
ventana.maxsize(500,350)



texto = tk.Label(ventana, text="Ingrese un numero N:")
texto.pack()
entrada = tk.Entry(ventana)
entrada.pack()

tk.Button(ventana, text="calcular", command=ejecutar).pack()

resp= tk.Label(ventana, text="resultado = 0:")
resp.pack()

ventana.mainloop()

# crear entorno virtual
# py -m venv venv

# windows
# .\vemc\Scripts\activate.bat
# 
# #crear el ejecutable
# #pyistaller --noconsole --onefile Suma.py

