"""
huellitas.py
-------------
Peluqueria Canina y Veterinaria 'Huellitas'
Gestion de Turnos, Servicios de Estetica y Cuidados Especiales

Programa unico: nucleo de logica recursiva + interfaz Tkinter.

NUCLEO DE LOGICA RECURSIVA (obligatorio, sin ciclos for/while):
    - calcular_ingresos_totales(lista_citas)
    - contar_por_especie(lista_citas, especie_buscada)
    - filtrar_cuidados_especiales(lista_citas)

Para ejecutar (necesitas Python 3 con soporte de Tkinter instalado):
    python3 huellitas.py
"""

import tkinter as tk
from tkinter import ttk, messagebox


# ===========================================================================
# NUCLEO DE LOGICA RECURSIVA
# ===========================================================================
# Unicamente estas tres funciones. Ninguna usa ciclos for/while: cada una
# avanza sobre la lista de citas mediante un indice que se incrementa en
# cada llamada recursiva (caso base -> caso recursivo).
#
# Estructura esperada de cada cita (dict):
#   {
#       "nombre":    str   -> nombre de la mascota
#       "especie":   str   -> "Perro" o "Gato"
#       "servicios": list  -> servicios contratados (ej. ["Peluqueria"])
#       "cuidados":  list  -> cuidados especiales contratados (puede ser [])
#       "especial":  bool  -> True si requiere manejo especial / sedacion
#       "tarifa":    float -> valor total de la cita (servicios + cuidados)
#   }

def calcular_ingresos_totales(lista_citas, indice=0):
    """
    Suma recursivamente la tarifa de todas las citas de la lista.

    Caso base: el indice llego al final de la lista -> no hay mas valor
    que sumar, se retorna 0.
    Caso recursivo: tarifa de la cita actual + ingresos del resto de la
    lista (indice + 1).
    """
    if indice >= len(lista_citas):
        return 0
    return lista_citas[indice]["tarifa"] + calcular_ingresos_totales(lista_citas, indice + 1)


def contar_por_especie(lista_citas, especie_buscada, indice=0):
    """
    Cuenta recursivamente cuantas citas corresponden a una especie dada
    ("Perro" o "Gato"), sin distinguir mayusculas/minusculas.

    Caso base: fin de la lista -> 0.
    Caso recursivo: 1 (si coincide la especie) + el conteo del resto,
    o 0 (si no coincide) + el conteo del resto.
    """
    if indice >= len(lista_citas):
        return 0

    coincide = 1 if lista_citas[indice]["especie"].strip().lower() == especie_buscada.strip().lower() else 0
    return coincide + contar_por_especie(lista_citas, especie_buscada, indice + 1)


def filtrar_cuidados_especiales(lista_citas, indice=0):
    """
    Retorna, de forma recursiva, una nueva lista con unicamente las
    citas que requieren manejo especial / sedacion.

    Caso base: fin de la lista -> lista vacia.
    Caso recursivo: si la cita actual requiere cuidado especial, se
    antepone al resultado de procesar el resto de la lista; si no, se
    retorna solo el resultado del resto.
    """
    if indice >= len(lista_citas):
        return []

    resto = filtrar_cuidados_especiales(lista_citas, indice + 1)

    if lista_citas[indice]["especial"]:
        return [lista_citas[indice]] + resto
    return resto


# ===========================================================================
# INTERFAZ GRAFICA (TKINTER)
# ===========================================================================

# Tarifas fijas por servicio y por cuidado especial (en pesos; "k" = miles)
PRECIO_SERVICIOS = {"Peluquería": 30000, "Veterinario": 50000}
PRECIO_CUIDADOS = {"Sedación": 15000, "Piel Sensible": 15000}

COLOR_FONDO = "#fdf6ec"
COLOR_PANEL = "#ffffff"
COLOR_ACENTO = "#6b8f71"
COLOR_ACENTO_OSCURO = "#4f6b54"
COLOR_TEXTO = "#3a3a3a"


class HuellitasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🐾 Peluquería y veterinaria Huellitas")
        self.root.geometry("840x700")
        self.root.configure(bg=COLOR_FONDO)
        self.root.minsize(780, 620)

        # Lista de citas del dia: unica fuente de datos para el motor recursivo
        self.citas = []

        self._configurar_estilos()
        self._construir_interfaz()

    # ------------------------------------------------------------------
    # Estilos
    # ------------------------------------------------------------------
    def _configurar_estilos(self):
        estilo = ttk.Style()
        try:
            estilo.theme_use("clam")
        except tk.TclError:
            pass

        estilo.configure("TFrame", background=COLOR_FONDO)
        estilo.configure("Panel.TFrame", background=COLOR_PANEL)
        estilo.configure("TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO, font=("Segoe UI", 10))
        estilo.configure("Panel.TLabel", background=COLOR_PANEL, foreground=COLOR_TEXTO, font=("Segoe UI", 10))
        estilo.configure("Titulo.TLabel", background=COLOR_FONDO, foreground=COLOR_ACENTO_OSCURO,
                         font=("Segoe UI", 17, "bold"))
        estilo.configure("Subtitulo.TLabel", background=COLOR_FONDO, foreground=COLOR_TEXTO,
                         font=("Segoe UI", 10, "italic"))
        estilo.configure("Seccion.TLabel", background=COLOR_FONDO, foreground=COLOR_ACENTO_OSCURO,
                         font=("Segoe UI", 12, "bold"))
        estilo.configure("TCheckbutton", background=COLOR_PANEL, foreground=COLOR_TEXTO, font=("Segoe UI", 10))
        estilo.configure("TEntry", font=("Segoe UI", 10))
        estilo.configure(
            "Accento.TButton",
            background=COLOR_ACENTO,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            padding=8,
        )
        estilo.map("Accento.TButton", background=[("active", COLOR_ACENTO_OSCURO)])

        estilo.configure("Treeview", background="#fbfbf8", fieldbackground="#fbfbf8",
                         foreground=COLOR_TEXTO, rowheight=26, font=("Segoe UI", 9))
        estilo.configure("Treeview.Heading", background=COLOR_ACENTO, foreground="white",
                         font=("Segoe UI", 9, "bold"))
        estilo.map("Treeview.Heading", background=[("active", COLOR_ACENTO_OSCURO)])

    # ------------------------------------------------------------------
    # Construccion de la interfaz (sigue el orden del boceto)
    # ------------------------------------------------------------------
    def _construir_interfaz(self):
        contenedor = ttk.Frame(self.root, padding=20, style="TFrame")
        contenedor.pack(fill="both", expand=True)

        self._construir_encabezado(contenedor)
        self._construir_formulario(contenedor)
        self._construir_seccion_lista(contenedor)
        self._construir_tabla(contenedor)
        self._construir_botones_inferiores(contenedor)

    def _construir_encabezado(self, padre):
        ttk.Label(
            padre,
            text="Bienvenido a la Peluquería y veterinaria Huellitas",
            style="Titulo.TLabel",
            anchor="center",
            justify="center",
        ).pack(fill="x", pady=(0, 4))
        ttk.Label(
            padre,
            text="🐾 Gestión de turnos, estética y cuidados especiales",
            style="Subtitulo.TLabel",
            anchor="center",
            justify="center",
        ).pack(fill="x", pady=(0, 16))

    def _construir_formulario(self, padre):
        panel = ttk.Frame(padre, style="Panel.TFrame", padding=18)
        panel.pack(fill="x", pady=(0, 14))
        panel.columnconfigure(1, weight=1)

        # Nombre de la mascota
        ttk.Label(panel, text="Nombre de la mascota:", style="Panel.TLabel").grid(
            row=0, column=0, sticky="w", pady=6)
        self.entrada_nombre = ttk.Entry(panel, width=32)
        self.entrada_nombre.grid(row=0, column=1, sticky="w", pady=6)

        # Especie (mutuamente excluyente: una mascota es Perro o Gato)
        ttk.Label(panel, text="Especie:", style="Panel.TLabel").grid(row=1, column=0, sticky="w", pady=6)
        marco_especie = ttk.Frame(panel, style="Panel.TFrame")
        marco_especie.grid(row=1, column=1, sticky="w", pady=6)
        self.var_perro = tk.BooleanVar(value=False)
        self.var_gato = tk.BooleanVar(value=False)
        ttk.Checkbutton(marco_especie, text="Perro", variable=self.var_perro,
                        command=self._al_marcar_perro).pack(side="left", padx=(0, 20))
        ttk.Checkbutton(marco_especie, text="Gato", variable=self.var_gato,
                        command=self._al_marcar_gato).pack(side="left")

        # Servicio requerido (tarifa fija, se puede elegir uno o ambos)
        ttk.Label(panel, text="Servicio Requerido:", style="Panel.TLabel").grid(
            row=2, column=0, sticky="w", pady=6)
        marco_servicio = ttk.Frame(panel, style="Panel.TFrame")
        marco_servicio.grid(row=2, column=1, sticky="w", pady=6)
        self.var_peluqueria = tk.BooleanVar(value=False)
        self.var_veterinario = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            marco_servicio,
            text=f"Peluquería ({self._texto_precio(PRECIO_SERVICIOS['Peluquería'])})",
            variable=self.var_peluqueria,
        ).pack(side="left", padx=(0, 20))
        ttk.Checkbutton(
            marco_servicio,
            text=f"Veterinario ({self._texto_precio(PRECIO_SERVICIOS['Veterinario'])})",
            variable=self.var_veterinario,
        ).pack(side="left")

        # Cuidados especiales (tarifa fija, se puede elegir uno, ambos o ninguno)
        ttk.Label(panel, text="Cuidados especiales:", style="Panel.TLabel").grid(
            row=3, column=0, sticky="w", pady=6)
        marco_cuidados = ttk.Frame(panel, style="Panel.TFrame")
        marco_cuidados.grid(row=3, column=1, sticky="w", pady=6)
        self.var_sedacion = tk.BooleanVar(value=False)
        self.var_piel_sensible = tk.BooleanVar(value=False)
        ttk.Checkbutton(
            marco_cuidados,
            text=f"Sedación ({self._texto_precio(PRECIO_CUIDADOS['Sedación'])})",
            variable=self.var_sedacion,
        ).pack(side="left", padx=(0, 20))
        ttk.Checkbutton(
            marco_cuidados,
            text=f"Piel Sensible ({self._texto_precio(PRECIO_CUIDADOS['Piel Sensible'])})",
            variable=self.var_piel_sensible,
        ).pack(side="left")

        ttk.Button(panel, text="➕ Agendar Mascota", style="Accento.TButton",
                   command=self.agendar_mascota).grid(row=4, column=0, columnspan=2, sticky="ew", pady=(16, 0))

    def _construir_seccion_lista(self, padre):
        marco = ttk.Frame(padre, style="TFrame")
        marco.pack(fill="x", pady=(4, 8))
        ttk.Label(marco, text="Lista:", style="Seccion.TLabel").pack(side="left")
        ttk.Separator(marco, orient="horizontal").pack(side="left", fill="x", expand=True, padx=(10, 0))

    def _construir_tabla(self, padre):
        marco = ttk.Frame(padre, style="Panel.TFrame", padding=4)
        marco.pack(fill="both", expand=True)
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)

        self.tabla = ttk.Treeview(
            marco,
            columns=("nombre", "especie", "servicio", "cuidados", "total"),
            show="headings",
            height=9,
        )
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("especie", text="Especie")
        self.tabla.heading("servicio", text="Servicio")
        self.tabla.heading("cuidados", text="Cuidados")
        self.tabla.heading("total", text="Total")
        self.tabla.column("nombre", width=130, anchor="w")
        self.tabla.column("especie", width=80, anchor="center")
        self.tabla.column("servicio", width=180, anchor="w")
        self.tabla.column("cuidados", width=180, anchor="w")
        self.tabla.column("total", width=100, anchor="e")
        self.tabla.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(marco, orient="vertical", command=self.tabla.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tabla.configure(yscrollcommand=scrollbar.set)

    def _construir_botones_inferiores(self, padre):
        marco = ttk.Frame(padre, style="TFrame")
        marco.pack(fill="x", pady=(14, 0))
        ttk.Button(marco, text="💰 Calcular Caja Diaria", style="Accento.TButton",
                   command=self.calcular_caja_diaria).pack(side="left", expand=True, fill="x", padx=(0, 8))
        ttk.Button(marco, text="📊 Ver Estadísticas", style="Accento.TButton",
                   command=self.ver_estadisticas).pack(side="left", expand=True, fill="x", padx=(8, 0))

    # ------------------------------------------------------------------
    # Especie mutuamente excluyente (una mascota es Perro o Gato, no ambos)
    # ------------------------------------------------------------------
    def _al_marcar_perro(self):
        if self.var_perro.get():
            self.var_gato.set(False)

    def _al_marcar_gato(self):
        if self.var_gato.get():
            self.var_perro.set(False)

    # ------------------------------------------------------------------
    # Acciones de los botones
    # ------------------------------------------------------------------
    def agendar_mascota(self):
        nombre = self.entrada_nombre.get().strip()
        if not nombre:
            messagebox.showwarning("Falta información", "Ingresa el nombre de la mascota.")
            return

        if not self.var_perro.get() and not self.var_gato.get():
            messagebox.showwarning("Falta información", "Selecciona la especie (Perro o Gato).")
            return
        especie = "Perro" if self.var_perro.get() else "Gato"

        servicios = []
        if self.var_peluqueria.get():
            servicios.append("Peluquería")
        if self.var_veterinario.get():
            servicios.append("Veterinario")

        if not servicios:
            messagebox.showwarning("Falta información", "Selecciona al menos un servicio requerido.")
            return

        cuidados = []
        if self.var_sedacion.get():
            cuidados.append("Sedación")
        if self.var_piel_sensible.get():
            cuidados.append("Piel Sensible")

        total = 0
        if self.var_peluqueria.get():
            total += PRECIO_SERVICIOS["Peluquería"]
        if self.var_veterinario.get():
            total += PRECIO_SERVICIOS["Veterinario"]
        if self.var_sedacion.get():
            total += PRECIO_CUIDADOS["Sedación"]
        if self.var_piel_sensible.get():
            total += PRECIO_CUIDADOS["Piel Sensible"]

        nueva_cita = {
            "nombre": nombre,
            "especie": especie,
            "servicios": servicios,
            "cuidados": cuidados,
            "especial": len(cuidados) > 0,
            "tarifa": total,
        }
        self.citas.append(nueva_cita)

        self._refrescar_tabla()
        self._limpiar_formulario()

    def calcular_caja_diaria(self):
        if not self.citas:
            messagebox.showinfo("Caja Diaria", "Aún no hay citas agendadas.")
            return

        total = calcular_ingresos_totales(self.citas)
        messagebox.showinfo(
            "Caja Diaria",
            f"Total de citas del día: {len(self.citas)}\nIngresos totales: {self._texto_dinero(total)}",
        )

    def ver_estadisticas(self):
        if not self.citas:
            messagebox.showinfo("Estadísticas", "Aún no hay citas agendadas.")
            return

        perros = contar_por_especie(self.citas, "Perro")
        gatos = contar_por_especie(self.citas, "Gato")
        especiales = filtrar_cuidados_especiales(self.citas)
        total = calcular_ingresos_totales(self.citas)
        promedio = total / len(self.citas)

        mensaje = (
            f"Total de mascotas atendidas: {len(self.citas)}\n"
            f"Perros: {perros}\n"
            f"Gatos: {gatos}\n"
            f"Con cuidados especiales / sedación: {len(especiales)}\n\n"
            f"Ingresos totales: {self._texto_dinero(total)}\n"
            f"Tarifa promedio por mascota: {self._texto_dinero(promedio)}"
        )
        messagebox.showinfo("Estadísticas del día", mensaje)

    # ------------------------------------------------------------------
    # Utilidades internas para la tabla (recursivas, sin for/while)
    # ------------------------------------------------------------------
    def _refrescar_tabla(self):
        self._eliminar_filas(self.tabla.get_children())
        self._insertar_filas(self.citas)

    def _eliminar_filas(self, items, indice=0):
        if indice >= len(items):
            return
        self.tabla.delete(items[indice])
        self._eliminar_filas(items, indice + 1)

    def _insertar_filas(self, lista_citas, indice=0):
        if indice >= len(lista_citas):
            return
        cita = lista_citas[indice]
        servicio_texto = " + ".join(cita["servicios"])
        cuidados_texto = " + ".join(cita["cuidados"]) if cita["cuidados"] else "Ninguno"
        self.tabla.insert(
            "", tk.END,
            values=(cita["nombre"], cita["especie"], servicio_texto, cuidados_texto,
                    self._texto_dinero(cita["tarifa"])),
        )
        self._insertar_filas(lista_citas, indice + 1)

    def _limpiar_formulario(self):
        self.entrada_nombre.delete(0, tk.END)
        self.var_perro.set(False)
        self.var_gato.set(False)
        self.var_peluqueria.set(False)
        self.var_veterinario.set(False)
        self.var_sedacion.set(False)
        self.var_piel_sensible.set(False)
        self.entrada_nombre.focus()

    @staticmethod
    def _texto_precio(valor):
        return f"{int(valor / 1000)}k"

    @staticmethod
    def _texto_dinero(valor):
        return "$" + f"{valor:,.0f}".replace(",", ".")


def main():
    root = tk.Tk()
    HuellitasApp(root)
    root.mainloop()



main()