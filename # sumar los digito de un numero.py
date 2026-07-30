# sumar los digito de un numero
def sumarDigito(n):
    if n <= 1: #Caso base
        return 1
    else:
        return n % 10 + sumarDigito(n // 10) #(o lo necesario)

print(sumarDigito(142))