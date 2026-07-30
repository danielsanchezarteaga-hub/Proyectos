import tkinter as tk
from tkinter import messagebox


PRECIO_SENCILLA = 50_000
PRECIO_DOBLE = 80_000
PRECIO_SUITE = 150_000

PRECIO_DESAYUNO = 15_000
PRECIO_PARQUEADERO = 10_000

huespedes = []


# Funciones de lógica 
def precio_habitacion(tipo_habitacion):
    """Devuelve el precio por noche según el tipo de habitación."""
    if tipo_habitacion == "Sencilla":
        return PRECIO_SENCILLA
    elif tipo_habitacion == "Doble":
        return PRECIO_DOBLE
    elif tipo_habitacion == "Suite":
        return PRECIO_SUITE
    else:
        return 0


def calcular_total(tipo_habitacion, dias, incluye_desayuno, incluye_parqueadero):
    """Calcula el valor total a pagar según habitación, días y servicios."""
    total = precio_habitacion(tipo_habitacion) * dias

    if incluye_desayuno:
        total = total + (PRECIO_DESAYUNO * dias)

    if incluye_parqueadero:
        total = total + (PRECIO_PARQUEADERO * dias)

    return total


def validar_datos(nombre, documento, dias_texto):

    if nombre.strip() == "":
        return False, 0, "El nombre completo es obligatorio."

    if documento.strip() == "":
        return False, 0, "El documento ID es obligatorio."

    if not dias_texto.isdigit():
        return False, 0, "Los días de estadía deben ser un número entero."

    dias_numero = int(dias_texto)
    if dias_numero <= 0:
        return False, 0, "Los días de estadía deben ser mayores a 0."

    return True, dias_numero, ""


def formatear_pesos(valor):
    texto = f"${valor:,.0f}"
    texto = texto.replace(",", ".")
    return texto


def formatear_fila(nombre, documento, habitacion, dias, servicios, total_texto):
    
    return (
        f"{nombre:<18}"
        f"{documento:<14}"
        f"{habitacion:<11}"
        f"{str(dias):<6}"
        f"{servicios:<22}"
        f"{total_texto:<12}"
    )

# Funciones que interactúan con la interfaz 
def limpiar_formulario():
    entrada_nombre.delete(0, tk.END)
    entrada_documento.delete(0, tk.END)
    entrada_dias.delete(0, tk.END)
    variable_habitacion.set("Sencilla")
    variable_desayuno.set(False)
    variable_parqueadero.set(False)


def guardar_registro():
    nombre = entrada_nombre.get()
    documento = entrada_documento.get()
    dias_texto = entrada_dias.get()
    tipo_habitacion = variable_habitacion.get()
    incluye_desayuno = variable_desayuno.get()
    incluye_parqueadero = variable_parqueadero.get()

    es_valido, dias, mensaje_error = validar_datos(nombre, documento, dias_texto)

    if not es_valido:
        messagebox.showerror("Datos inválidos", mensaje_error)
        return

    total = calcular_total(tipo_habitacion, dias, incluye_desayuno, incluye_parqueadero)

    # Construir el texto de servicios adicionales
    lista_servicios = []
    if incluye_desayuno:
        lista_servicios.append("Desayuno")
    if incluye_parqueadero:
        lista_servicios.append("Parqueadero")

    if len(lista_servicios) == 0:
        servicios_texto = "Ninguno"
    else:
        servicios_texto = ", ".join(lista_servicios)

    # Guardar en la lista global de huéspedes
    registro = (nombre.strip(), documento.strip(), tipo_habitacion, dias, servicios_texto, total)
    huespedes.append(registro)

    # Agregar la fila 
    fila_texto = formatear_fila(
        nombre.strip(), documento.strip(), tipo_habitacion, dias, servicios_texto, formatear_pesos(total)
    )
    lista_huespedes.insert(tk.END, fila_texto)

    limpiar_formulario()

    messagebox.showinfo(
        "Registro guardado",
        f"Huésped registrado correctamente.\nTotal a pagar: {formatear_pesos(total)}",
    )

# Construcción de la ventana principal 
ventana = tk.Tk()
ventana.title("                                                                                                 Hotel Blue Label         ")
ventana.geometry("780x620") 
ventana.resizable(False,False)
ventana.config(bg="darkblue")

# ----- Sección: Registrar Nuevo Huésped -----
marco_registro = tk.Frame(ventana, padx=10, pady=10, bd=0, highlightthickness=0)
marco_registro.pack(fill="x", padx=15, pady=15)
marco_registro.config(bg="darkblue")

# Nombre completo
tk.Label(marco_registro, text="Digite el nombre:").grid(row=0, column=0, sticky="w", pady=6)
entrada_nombre = tk.Entry(marco_registro, width=40)
entrada_nombre.grid(row=0, column=1, columnspan=3, sticky="w", pady=6)

# Documento ID
tk.Label(marco_registro, text="Digite la cedula:").grid(row=1, column=0, sticky="w", pady=6)
entrada_documento = tk.Entry(marco_registro, width=40)
entrada_documento.grid(row=1, column=1, columnspan=3, sticky="w", pady=6)

# Días de estadía
tk.Label(marco_registro, text="Digite los dias:").grid(row=2, column=0, sticky="w", pady=6)
entrada_dias = tk.Entry(marco_registro, width=8)
entrada_dias.grid(row=2, column=1, sticky="w", pady=6)

# Tipo de habitación (radio buttons)
tk.Label(marco_registro, text="Tipo de habitacion:").grid(row=3, column=0, sticky="w", pady=6)

variable_habitacion = tk.StringVar(value="Sencilla")

tk.Radiobutton(
    marco_registro, text=f"Sencilla (${PRECIO_SENCILLA // 1000}k)",
    variable=variable_habitacion, value="Sencilla",
).grid(row=3, column=2, sticky="w", pady=6)

tk.Radiobutton(
    marco_registro, text=f"Doble (${PRECIO_DOBLE // 1000}k)",
    variable=variable_habitacion, value="Doble",
).grid(row=3, column=3, sticky="w", pady=6)

tk.Radiobutton(
    marco_registro, text=f"Suite (${PRECIO_SUITE // 1000}k)",
    variable=variable_habitacion, value="Suite",
).grid(row=3, column=4, sticky="w", pady=6)

# Servicios adicionales 
tk.Label(marco_registro, text="Servicios Extra").grid(row=4, column=0, sticky="w", pady=6)

variable_desayuno = tk.BooleanVar(value=False)
variable_parqueadero = tk.BooleanVar(value=False)

tk.Checkbutton(
    marco_registro, text=f"Desayuno (+${PRECIO_DESAYUNO // 1000}k/día)",
    variable=variable_desayuno,
).grid(row=4, column=2, sticky="w", pady=6)

tk.Checkbutton(
    marco_registro, text=f"Parqueadero (+${PRECIO_PARQUEADERO // 1000}k/día)",
    variable=variable_parqueadero,
).grid(row=4, column=3, sticky="w", pady=6)

# Botón Guardar Registro
tk.Button(marco_registro, text="Guardar Registro", command=guardar_registro).grid(
    row=6, column=2, columnspan=6, pady=12
)

# ----- Sección: Huéspedes en Memoria -----

tk.Label(ventana, text="Datos", bg="darkblue", fg="white", font=("Arial", 11, "bold")).pack(anchor="w", padx=25)


marco_tabla = tk.Frame(ventana, padx=10, pady=10, bd=0, highlightthickness=0)
marco_tabla.pack(fill="both", expand=True, padx=15, pady=(0, 15))
marco_tabla.config(bg="darkblue")


fuente_tabla = ("Courier", 10)

encabezado_texto = formatear_fila("Nombre", "Documento", "Habitación", "Días", "Servicios", "Total Pagar")
tk.Label(marco_tabla, text=encabezado_texto, font=("Courier", 10, "bold"), anchor="w").pack(fill="x")

# Marco auxiliar 
marco_lista = tk.Frame(marco_tabla)
marco_lista.pack(fill="both", expand=True, pady=(6, 0))

barra_desplazamiento = tk.Scrollbar(marco_lista, orient="vertical")
barra_desplazamiento.pack(side="right", fill="y")

lista_huespedes = tk.Listbox(
    marco_lista,
    font=fuente_tabla,
    yscrollcommand=barra_desplazamiento.set,
)
lista_huespedes.pack(fill="both", expand=True, side="left")

barra_desplazamiento.config(command=lista_huespedes.yview)

ventana.mainloop()