#vaina 2 dolares
#cocolate 3 dolares

def menu():
    print("----Bienvenido a la Heladería----")
    print("--Bienvenido al menú de opciones--")
    print("Seleccione una opción:")
    print("1. Vaina")
    print("2. Chocolate")
    print("3. Salir")

def pedido(totalActual):
    menu()
    opc = int(input("Digite su número de opción 1, 2, 3: "))

    if opc == 1:
        print("Ha seleccionado Vainilla. El precio es de 2 dólares.")
        return pedido(totalActual + 2)
    elif opc == 2:
        print("Ha seleccionado Chocolate. El precio es de 3 dólares.")
        return pedido(totalActual + 3)
    elif opc == 3:
        print("Gracias por su compra. ¡Hasta luego!")
        return totalActual
    else:
        print("Opción no válida. Por favor, seleccione una opción válida.")
        return pedido(totalActual)

def main():
    total = pedido(0)
    print("----------------")
    print(f"El total de su compra es: {total} dólares.")

main()
