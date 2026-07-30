# polindromo 2
def longitud_texto(texto):
    # calcular la longitud del texto ingresado sin funcion len()
    contador = 0
    for i in texto:
        contador += 1
    return contador
def es_palindromo(texto):
    inicio = 0
    fin = longitud_texto(texto) - 1
   
    while inicio < fin:
        if texto[inicio] != texto[fin]:
            return False #se encontró una diferencia, no es palíndromo
        inicio += 1
        fin -= 1
    
    
    return True
