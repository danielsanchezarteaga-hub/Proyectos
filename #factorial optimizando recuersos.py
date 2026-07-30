#factorial optimizando recuersos 

def factorial(numero):
    if numero == 1:
        return 1
    else: 
        resultado = numero * factorial (numero -1)
        return resultado
re = factorial(5)
print(re)