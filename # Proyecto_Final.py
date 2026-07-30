# Trabajo final ultima edicion 
import tkinter as tk
from tkinter import messagebox

PRECIO_SERVICIOS = {"Baño": 25000, "Corte De Pelo": 20000, "Revisión Médica": 40000}
PRECIO_CUIDADOS = {"Sedación": 15000, "Piel Sensible": 15000}

citas = []

def calcular_ingresos_totales(lista_citas, indice=0):
    if indice >= len(lista_citas):
        return 0
    return lista_citas[indice]["tarifa"] + calcular_ingresos_totales(lista_citas, indice + 1)


def contar_por_especie(lista_citas, especie_buscada, indice=0):
    if indice >= len(lista_citas):
        return 0
    coincide = 1 if lista_citas[indice]["especie"].strip().lower() == especie_buscada.strip().lower() else 0
    return coincide + contar_por_especie(lista_citas, especie_buscada, indice + 1)


def filtrar_cuidados_especiales(lista_citas, indice=0):
    if indice >= len(lista_citas):
        return []
    resto = filtrar_cuidados_especiales(lista_citas, indice + 1)
    if lista_citas[indice]["especial"]:
        return [lista_citas[indice]] + resto
    return resto

def texto_dinero(valor):
    return f"${valor:.0f}"


def insertar_filas(lista_citas, indice=0):
    if indice >= len(lista_citas):
        return
    cita = lista_citas[indice]
    numero = indice + 1
    servicio_texto = " + ".join(cita["servicio"]) if cita["servicio"] else "Ninguno"
    cuidados_texto = " + ".join(cita["cuidados"]) if cita["cuidados"] else "Ninguno"
    linea = f"{numero}.  {cita['nombre']} - {cita['especie']} - {servicio_texto} - {cuidados_texto} - {texto_dinero(cita['tarifa'])}"
    lista_agenda.insert(tk.END, linea)
    insertar_filas(lista_citas, indice + 1)

def refrescar_lista():
    lista_agenda.delete(0, tk.END)
    insertar_filas(citas)

def limpiar_formulario():
    entrada_nombre.delete(0, tk.END)
    entrada_especie.delete(0, tk.END)
    var_bano.set(False)
    var_corte.set(False)
    var_revision.set(False)
    entrada_tarifa.delete(0, tk.END)
    var_sedacion.set(False)
    var_piel_sensible.set(False)
    entrada_nombre.focus()

def recalcular_tarifa():
    total_base = 0
    if var_bano.get():
        total_base += PRECIO_SERVICIOS["Baño"]
    if var_corte.get():
        total_base += PRECIO_SERVICIOS["Corte De Pelo"]
    if var_revision.get():
        total_base += PRECIO_SERVICIOS["Revisión Médica"]
    entrada_tarifa.delete(0, tk.END)
    entrada_tarifa.insert(0, str(total_base))
    

def agendar_mascota():
    nombre = entrada_nombre.get().strip()
    if not nombre:
        messagebox.showwarning("Falta información", "Ingresa el nombre de la mascota.")
        return
    if not nombre.replace(" ", "").isalpha():
        messagebox.showwarning("Dato inválido", "El nombre solo debe contener letras.")
        return


    especie = entrada_especie.get().strip().capitalize()
    if especie not in ("Perro", "Gato"):
        messagebox.showwarning("Dato inválido", "La especie debe ser 'Perro' o 'Gato'.")
        return

    servicios_lista = []
    if var_bano.get():
        servicios_lista.append("Baño")
    if var_corte.get():
        servicios_lista.append("Corte De Pelo")
    if var_revision.get():
        servicios_lista.append("Revisión Médica")

    if not servicios_lista:
        messagebox.showwarning("Falta información", "Selecciona al menos un servicio.")
        return

    try:
        tarifa = float(entrada_tarifa.get().strip())
        if tarifa <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Dato inválido", "La tarifa debe ser un número mayor a 0.")
        return
    cuidados_lista = []
    extra_cuidados = 0
    if var_sedacion.get():
        cuidados_lista.append("Sedación")
        extra_cuidados += PRECIO_CUIDADOS["Sedación"]
    if var_piel_sensible.get():
        cuidados_lista.append("Piel Sensible")
        extra_cuidados += PRECIO_CUIDADOS["Piel Sensible"]

    tarifa_total = tarifa + extra_cuidados



    nueva_cita = {
        "nombre": nombre,
        "especie": especie,
        "servicio": servicios_lista,
        "cuidados": cuidados_lista,
        "especial": len(cuidados_lista)>0,
        "tarifa": tarifa_total,
    }
    citas.append(nueva_cita)

    refrescar_lista()
    limpiar_formulario()


def calcular_caja_diaria():
    if not citas:
        messagebox.showinfo("Caja Diaria", "Aún no hay citas agendadas.")
        return
    total = calcular_ingresos_totales(citas)
    messagebox.showinfo(
        "Caja Diaria",
        f"Total de citas del día: {len(citas)}\nIngresos totales: {texto_dinero(total)}",
    )


def ver_estadisticas():
    if not citas:
        messagebox.showinfo("Estadísticas", "Aún no hay citas agendadas.")
        return

    perros = contar_por_especie(citas, "Perro")
    gatos = contar_por_especie(citas, "Gato")
    especiales = filtrar_cuidados_especiales(citas)
    total = calcular_ingresos_totales(citas)
    promedio = total / len(citas)

    mensaje = (
        f"Total de mascotas atendidas: {len(citas)}\n"
        f"Perros: {perros}\n"
        f"Gatos: {gatos}\n"
        f"Con cuidados especiales / sedación / piel_sencible: {len(especiales)}\n\n"
        f"Ingresos totales: {texto_dinero(total)}\n"
        f"Tarifa promedio por mascota: {texto_dinero(promedio)}"
    )
    messagebox.showinfo("Estadísticas del día", mensaje)

ventana = tk.Tk()
ventana.title("Peluquería y veterinaria Huellitas")
ventana.configure(bg="#B1D4E1")#color de ventana

tk.Label(ventana, text="Bienvenido a la Peluquería y veterinaria Huellitas",font=("Arial", 14, "bold")).pack(pady=10)

marco_nombre = tk.Frame(ventana)
marco_nombre.pack(pady=4)
tk.Label(marco_nombre, text="Nombre de la mascota:", bg="#B1D4E1").pack(side="left")
entrada_nombre = tk.Entry(marco_nombre, width=30)
entrada_nombre.pack(side="left")

marco_especie = tk.Frame(ventana)
marco_especie.pack(pady=4)
tk.Label(marco_especie, text="Especie del animal:", bg="#B1D4E1").pack(side="left")
entrada_especie = tk.Entry(marco_especie, width=30)
entrada_especie.pack(side="left")


var_bano = tk.BooleanVar()
var_corte = tk.BooleanVar()
var_revision = tk.BooleanVar()

marco_servicio = tk.Frame(ventana)
marco_servicio.pack(pady=4)
tk.Label(marco_servicio, text="Servicio(s) Requerido(s):", bg="#B1D4E1").pack(side="left")

boton_servicios = tk.Menubutton(marco_servicio, text="Seleccionar servicios", relief="raised")
menu_servicios = tk.Menu(boton_servicios, tearoff=0)
menu_servicios.add_checkbutton(label="Baño", variable=var_bano, command=recalcular_tarifa)
menu_servicios.add_checkbutton(label="Corte De Pelo", variable=var_corte, command=recalcular_tarifa)
menu_servicios.add_checkbutton(label="Revisión Médica", variable=var_revision, command=recalcular_tarifa)
boton_servicios["menu"] = menu_servicios
boton_servicios.pack(side="left")

marco_tarifa = tk.Frame(ventana)
marco_tarifa.pack(pady=4)
tk.Label(marco_tarifa, text="Tarifa base del servicio:", bg="#B1D4E1").pack(side="left")
entrada_tarifa = tk.Entry(marco_tarifa, width=30)
entrada_tarifa.pack(side="left")


marco_cuidados = tk.Frame(ventana)
marco_cuidados.pack(pady=4)
tk.Label(marco_cuidados, text="Cuidados especiales:", bg="#B1D4E1").pack(side="left")
var_sedacion = tk.BooleanVar()
var_piel_sensible = tk.BooleanVar()
tk.Checkbutton(marco_cuidados, text="Sedación (+15k)", variable=var_sedacion).pack(side="left")
tk.Checkbutton(marco_cuidados, text="Piel Sensible (+15k)", variable=var_piel_sensible).pack(side="left")

tk.Button(ventana, text="Agendar Mascota", command=agendar_mascota, bg="#17C1DF", width=20, height=1).pack(pady=10)

tk.Label(ventana, text="Agenda:").pack(anchor="w", padx=10)
lista_agenda = tk.Listbox(ventana, width=90, height=10)
lista_agenda.pack(padx=10, pady=4)

marco_botones = tk.Frame(ventana)
marco_botones.pack(pady=10)
tk.Button(marco_botones, text="Calcular Caja Diaria", command=calcular_caja_diaria, bg="#17C1DF").pack(side="left", padx=5)
tk.Button(marco_botones, text="Ver Estadísticas", command=ver_estadisticas,bg="#17C1DF").pack(side="left", padx=5)

ventana.mainloop()
