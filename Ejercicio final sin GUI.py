lista_citas = []


def agregar_cita():
    print("--- NUEVA CITA ---")

    nombre = input("Nombre de la mascota: ")
    especie = input("Especie (Perro/Gato): ")
    servicio = input("Servicio (Baño/Corte/Revisión): ")
    valor = int(input("Valor del servicio: "))

    respuesta = input("¿Requiere cuidados especiales? (S/N): ")

    if respuesta.upper() == "S":
        cuidados = True
    else:
        cuidados = False

    cita = {
        "nombre": nombre,
        "especie": especie,
        "servicio": servicio,
        "valor": valor,
        "cuidados": cuidados
    }

    lista_citas.append(cita)

    print("Cita agregada correctamente.")   


def calcular_ingresos_totales(lista, indice=0):
    if indice == len(lista):
        return 0

    return lista[indice]["valor"] + calcular_ingresos_totales(lista, indice + 1)


def contar_por_especie(lista, especie, indice=0):
    if indice == len(lista):
        return 0

    if lista[indice]["especie"].lower() == especie.lower():
        return 1 + contar_por_especie(lista, especie, indice + 1)

    return contar_por_especie(lista, especie, indice + 1)


def filtrar_cuidados_especiales(lista, indice=0):
    if indice == len(lista):
        return []

    resto = filtrar_cuidados_especiales(lista, indice + 1)

    if lista[indice]["cuidados"]:
        return [lista[indice]] + resto

    return resto


def mostrar_especiales(lista, indice=0):
    if indice == len(lista):
        return

    if lista[indice]["cuidados"]:
        print("----------------------")
        print("Nombre:", lista[indice]["nombre"])
        print("Especie:", lista[indice]["especie"])
        print("Servicio:", lista[indice]["servicio"])
        print("Valor:", lista[indice]["valor"])

    mostrar_especiales(lista, indice + 1)


def menu():
    print("====== CENTRO VETERINARIO HUELLITAS ======")
    print("1. Agregar cita")
    print("2. Calcular ingresos")
    print("3. Contar por especie")
    print("4. Mostrar cuidados especiales")
    print("5. Salir")

    opcion = int(input("Seleccione una opción: "))

    if opcion == 1:
        agregar_cita()
        menu()

    elif opcion == 2:
        print("Ingresos totales: $", calcular_ingresos_totales(lista_citas))
        menu()

    elif opcion == 3:
        especie = input("Ingrese la especie: ")
        cantidad = contar_por_especie(lista_citas, especie)
        print("Cantidad:", cantidad)
        menu()

    elif opcion == 4:
        especiales = filtrar_cuidados_especiales(lista_citas)

        if len(especiales) == 0:
            print("No existen mascotas con cuidados especiales.")
        else:
            mostrar_especiales(especiales)

        menu()

    elif opcion == 5:
        print("Programa finalizado.")

    else:
        print("Opción inválida.")
        menu()


menu()