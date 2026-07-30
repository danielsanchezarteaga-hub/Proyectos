# lista = [1,3,4,6]

def sumarLista (numero):
    if len(numero) == 0: #Caso base
        return 0
    else:
        return numero[0] + sumarLista(numero[1:]) #(o lo necesario)
lista = [1,3,4,6,7]
r = sumarLista(lista)
print(r)

