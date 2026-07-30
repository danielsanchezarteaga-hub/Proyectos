#CLOUDE
"""
logica_recursiva.py
--------------------
Peluqueria Canina y Veterinaria 'Huellitas'

Nucleo de logica de negocio. TODA consulta, filtro o acumulacion de datos
sobre la lista de citas del dia se resuelve con funciones RECURSIVAS.

Esta prohibido usar ciclos 'for' o 'while' en este modulo: cada funcion
avanza sobre la lista mediante llamadas recursivas a si misma, usando un
indice que se incrementa en cada llamada (caso base -> caso recursivo).

Estructura de una cita (dict):
    {
        "nombre":   str   -> nombre de la mascota
        "especie":  str   -> "Perro" o "Gato"
        "servicio": str   -> servicio contratado (Baño, Corte, Revision, etc.)
        "tarifa":   float -> valor del servicio
        "especial": bool  -> True si requiere manejo especial / sedacion
    }
"""


# ---------------------------------------------------------------------------
# 1) Funcion recursiva requerida: ingresos totales del dia
# ---------------------------------------------------------------------------
def calcular_ingresos_totales(lista_citas, indice=0):
    """
    Suma recursivamente la tarifa de todas las citas de la lista.

    Caso base: cuando el indice llega al final de la lista, no hay mas
    valor que sumar y se retorna 0.
    Caso recursivo: se suma la tarifa de la cita actual con el resultado
    de procesar el resto de la lista (indice + 1).
    """
    if indice >= len(lista_citas):
        return 0.0
    return lista_citas[indice]["tarifa"] + calcular_ingresos_totales(lista_citas, indice + 1)


# ---------------------------------------------------------------------------
# 2) Funcion recursiva requerida: conteo de citas por especie
# ---------------------------------------------------------------------------
def contar_por_especie(lista_citas, especie_buscada, indice=0):
    """
    Cuenta recursivamente cuantas citas corresponden a una especie dada
    ("Perro" o "Gato"), ignorando mayusculas/minusculas.

    Caso base: fin de la lista -> 0.
    Caso recursivo: 1 (si coincide la especie) + el conteo del resto,
    o 0 (si no coincide) + el conteo del resto.
    """
    if indice >= len(lista_citas):
        return 0

    coincide = 1 if lista_citas[indice]["especie"].strip().lower() == especie_buscada.strip().lower() else 0
    return coincide + contar_por_especie(lista_citas, especie_buscada, indice + 1)


# ---------------------------------------------------------------------------
# 3) Funcion recursiva requerida: filtrar cuidados especiales
# ---------------------------------------------------------------------------
def filtrar_cuidados_especiales(lista_citas, indice=0):
    """
    Retorna, de forma recursiva, una nueva lista solo con las citas que
    requieren manejo especial / sedacion.

    Caso base: fin de la lista -> lista vacia.
    Caso recursivo: si la cita actual requiere cuidado especial se agrega
    al resultado del resto de la lista; si no, se retorna solo el
    resultado del resto.
    """
    if indice >= len(lista_citas):
        return []

    resto = filtrar_cuidados_especiales(lista_citas, indice + 1)

    if lista_citas[indice]["especial"]:
        return [lista_citas[indice]] + resto
    return resto


# ---------------------------------------------------------------------------
# Funciones recursivas de apoyo (estadisticas y construccion de vistas)
# ---------------------------------------------------------------------------
def contar_por_servicio(lista_citas, servicio_buscado, indice=0):
    """Cuenta recursivamente cuantas citas corresponden a un servicio dado."""
    if indice >= len(lista_citas):
        return 0

    coincide = 1 if lista_citas[indice]["servicio"].strip().lower() == servicio_buscado.strip().lower() else 0
    return coincide + contar_por_servicio(lista_citas, servicio_buscado, indice + 1)


def obtener_servicios_unicos(lista_citas, indice=0):
    """
    Recorre recursivamente la lista y devuelve los nombres de servicio
    unicos (sin duplicados), preservando el orden de aparicion.
    """
    if indice >= len(lista_citas):
        return []

    resto = obtener_servicios_unicos(lista_citas, indice + 1)
    servicio_actual = lista_citas[indice]["servicio"]

    if servicio_actual in resto:
        return resto
    return [servicio_actual] + resto


def cita_mas_costosa(lista_citas, indice=0):
    """
    Encuentra recursivamente la cita con la tarifa mas alta.

    Caso base: si solo queda una cita (o ninguna), esa es el resultado.
    Caso recursivo: se compara la cita actual contra el mejor resultado
    del resto de la lista.
    """
    if indice >= len(lista_citas):
        return None
    if indice == len(lista_citas) - 1:
        return lista_citas[indice]

    mejor_del_resto = cita_mas_costosa(lista_citas, indice + 1)

    if mejor_del_resto is None or lista_citas[indice]["tarifa"] >= mejor_del_resto["tarifa"]:
        return lista_citas[indice]
    return mejor_del_resto


def contar_citas(lista_citas, indice=0):
    """Cuenta recursivamente el numero total de citas agendadas."""
    if indice >= len(lista_citas):
        return 0
    return 1 + contar_citas(lista_citas, indice + 1)


def calcular_promedio_tarifa(lista_citas):
    """
    Calcula el promedio de tarifas usando exclusivamente las funciones
    recursivas ya definidas (suma recursiva / conteo recursivo).
    """
    total_citas = contar_citas(lista_citas)
    if total_citas == 0:
        return 0.0
    return calcular_ingresos_totales(lista_citas) / total_citas


def construir_texto_agenda(lista_citas, indice=0):
    """
    Construye recursivamente el texto (linea a linea) que se muestra en
    la consola/lista grafica de la agenda del dia.
    """
    if indice >= len(lista_citas):
        return ""

    cita = lista_citas[indice]
    marca_especial = " [MANEJO ESPECIAL/SEDACION]" if cita["especial"] else ""
    linea = (
        f"{indice + 1:>2}. {cita['nombre']} ({cita['especie']}) - "
        f"{cita['servicio']} - ${cita['tarifa']:.2f}{marca_especial}"
    )

    resto = construir_texto_agenda(lista_citas, indice + 1)
    if resto == "":
        return linea
    return linea + "\n" + resto