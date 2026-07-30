
def invertir(n, acumulado):

    if n == 0:
        return acumulado

    nuevo_acumulado = acumulado * 10 + (n % 10)

    return invertir(n // 10, nuevo_acumulado)


def esPalindromo(numero):

    numero_invertido = invertir(numero, 0)

    if numero == numero_invertido:
        return True
    else:
        return False


def main():

    numero = int(input("Digite un numero: "))

    if esPalindromo(numero):
        print("El numero es palindromo.")
    else:
        print("El numero no es polindromo")


main()





