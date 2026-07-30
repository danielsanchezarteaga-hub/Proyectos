import tkinter as tk
from tkinter import messagebox

PRECIO_SERVICIOS = {"Peluquería": 30000, "Veterinario": 50000}
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

def al_marcar_perro():
    if var_perro.get():
        var_gato.set(False)

def al_marcar_gato():
    if var_gato.get():
        var_perro.set(False)

def insertar_filas(lista_citas, indice=0):
    if indice >= len(lista_citas):
        return
    cita = lista_citas[indice]
    servicio_texto = " + ".join(cita["servicios"])
    cuidados_texto = " + ".join(cita["cuidados"]) if cita["cuidados"] else "Ninguno"
    linea = f"{cita['nombre']} - {cita['especie']} - {servicio_texto} - {cuidados_texto} - {texto_dinero(cita['tarifa'])}"
    lista_agenda.insert(tk.END, linea)
    insertar_filas(lista_citas, indice + 1)

def refrescar_lista():
    lista_agenda.delete(0, tk.END)
    insertar_filas(citas)

def limpiar_formulario():
    entrada_nombre.delete(0, tk.END)
    var_perro.set(False)
    var_gato.set(False)
    var_peluqueria.set(False)
    var_veterinario.set(False)
    var_sedacion.set(False)
    var_piel_sensible.set(False)
    entrada_nombre.focus()

def agendar_mascota():
    nombre = entrada_nombre.get().strip()
    if not nombre:
        messagebox.showwarning("Falta información", "Ingresa el nombre de la mascota.")
        return

    if not var_perro.get() and not var_gato.get():
        messagebox.showwarning("Falta información", "Selecciona la especie (Perro o Gato).")
        return
    especie = "Perro" if var_perro.get() else "Gato"

    servicios = []
    if var_peluqueria.get():
        servicios.append("Peluquería")
    if var_veterinario.get():
        servicios.append("Veterinario")

    if not servicios:
        messagebox.showwarning("Falta información", "Selecciona al menos un servicio requerido.")
        return

    cuidados = []
    if var_sedacion.get():
        cuidados.append("Sedación")
    if var_piel_sensible.get():
        cuidados.append("Piel Sensible")

    total = 0
    if var_peluqueria.get():
        total += PRECIO_SERVICIOS["Peluquería"]
    if var_veterinario.get():
        total += PRECIO_SERVICIOS["Veterinario"]
    if var_sedacion.get():
        total += PRECIO_CUIDADOS["Sedación"]
    if var_piel_sensible.get():
        total += PRECIO_CUIDADOS["Piel Sensible"]

    nueva_cita = {
        "nombre": nombre,
        "especie": especie,
        "servicios": servicios,
        "cuidados": cuidados,
        "especial": len(cuidados) > 0,
        "tarifa": total,
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
        f"Con cuidados especiales / sedación: {len(especiales)}\n\n"
        f"Ingresos totales: {texto_dinero(total)}\n"
        f"Tarifa promedio por mascota: {texto_dinero(promedio)}"
    )
    messagebox.showinfo("Estadísticas del día", mensaje)

ventana = tk.Tk()
ventana.title("Peluquería y veterinaria Huellitas")

tk.Label(ventana, text="Bienvenido a la Peluquería y veterinaria Huellitas",
         font=("Arial", 14, "bold")).pack(pady=10)

marco_nombre = tk.Frame(ventana)
marco_nombre.pack(pady=4)
tk.Label(marco_nombre, text="Nombre de la mascota:").pack(side="left")
entrada_nombre = tk.Entry(marco_nombre, width=30)
entrada_nombre.pack(side="left")

marco_especie = tk.Frame(ventana)
marco_especie.pack(pady=4)
tk.Label(marco_especie, text="Especie del animal:").pack(side="left")
var_perro = tk.BooleanVar()
var_gato = tk.BooleanVar()
tk.Checkbutton(marco_especie, text="Perro", variable=var_perro, command=al_marcar_perro).pack(side="left")
tk.Checkbutton(marco_especie, text="Gato", variable=var_gato, command=al_marcar_gato).pack(side="left")

marco_servicio = tk.Frame(ventana)
marco_servicio.pack(pady=4)
tk.Label(marco_servicio, text="Servicio Requerido:").pack(side="left")
var_peluqueria = tk.BooleanVar()
var_veterinario = tk.BooleanVar()
tk.Checkbutton(marco_servicio, text="Peluquería (30k)", variable=var_peluqueria).pack(side="left")
tk.Checkbutton(marco_servicio, text="Veterinario (50k)", variable=var_veterinario).pack(side="left")

marco_cuidados = tk.Frame(ventana)
marco_cuidados.pack(pady=4)
tk.Label(marco_cuidados, text="Cuidados especiales:").pack(side="left")
var_sedacion = tk.BooleanVar()
var_piel_sensible = tk.BooleanVar()
tk.Checkbutton(marco_cuidados, text="Sedación (15k)", variable=var_sedacion).pack(side="left")
tk.Checkbutton(marco_cuidados, text="Piel Sensible (15k)", variable=var_piel_sensible).pack(side="left")

tk.Button(ventana, text="Agendar Mascota", command=agendar_mascota).pack(pady=8)

tk.Label(ventana, text="Agenda:").pack(anchor="w", padx=10)
lista_agenda = tk.Listbox(ventana, width=90, height=10)
lista_agenda.pack(padx=10, pady=4)

marco_botones = tk.Frame(ventana)
marco_botones.pack(pady=10)
tk.Button(marco_botones, text="Calcular Caja Diaria", command=calcular_caja_diaria).pack(side="left", padx=5)
tk.Button(marco_botones, text="Ver Estadísticas", command=ver_estadisticas).pack(side="left", padx=5)

ventana.mainloop()
