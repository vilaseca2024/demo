# import secrets
# import string
# import pandas as pd

# def generar_contraseña(longitud=12):
#     caracteres = string.ascii_letters + string.digits + string.punctuation
#     contraseña = ''.join(secrets.choice(caracteres) for _ in range(longitud))
#     return contraseña

# def generar_contraseñas(num_contraseñas, longitud=12):
#     contraseñas = []
#     for _ in range(num_contraseñas):
#         contraseñas.append(generar_contraseña(longitud))
#     return contraseñas

# if __name__ == "__main__":
#     num_contraseñas = int(input("¿Cuántas contraseñas deseas generar? "))
#     longitud = int(input("¿Cuántos caracteres debe tener cada contraseña? "))
#     contraseñas = generar_contraseñas(num_contraseñas, longitud)
#     df = pd.DataFrame(contraseñas, columns=["Contraseñas"])
#     archivo_excel = "contrasenas_generadas.xlsx"
#     df.to_excel(archivo_excel, index=False)

#     print(f"Se han generado {num_contraseñas} contraseñas y se han guardado en '{archivo_excel}'")

#################################################

# import secrets
# import string
# import pandas as pd

# def generar_contraseña(longitud=12):
#     caracteres = string.ascii_letters + string.digits + string.punctuation
#     contraseña = ''.join(secrets.choice(caracteres) for _ in range(longitud - 2))  
#     primera_letra = secrets.choice(string.ascii_uppercase)
#     signos_puntuacion = secrets.choice(string.punctuation)
#     contraseña = primera_letra + contraseña + signos_puntuacion
#     return contraseña

# def generar_contraseñas(num_contraseñas, longitud=12):
#     contraseñas = []
#     for _ in range(num_contraseñas):
#         contraseñas.append(generar_contraseña(longitud))
#     return contraseñas

# if __name__ == "__main__":
#     num_contraseñas = int(input("¿Cuántas contraseñas deseas generar? "))
#     longitud = int(input("¿Cuántos caracteres debe tener cada contraseña? "))
#     contraseñas = generar_contraseñas(num_contraseñas, longitud)
#     df = pd.DataFrame(contraseñas, columns=["Contraseñas"])
#     archivo_excel = "contrasenas_generadas.xlsx"
#     df.to_excel(archivo_excel, index=False)
#     print(f"Se han generado {num_contraseñas} contraseñas y se han guardado en '{archivo_excel}'")


#############################################
import secrets
import string
import pandas as pd

def generar_contraseña(longitud=12, palabra="Palabra"):
    caracteres = string.ascii_letters + string.punctuation
    if longitud <= len(palabra) + 2:
        raise ValueError("La longitud de la contraseña debe ser mayor que la longitud de la palabra + 2 para que funcione correctamente.")
    parte_aleatoria = ''.join(secrets.choice(caracteres) for _ in range(longitud - len(palabra) - 2))
    primera_letra = secrets.choice(string.ascii_uppercase)
    numeros = ''.join(secrets.choice(string.digits) for _ in range(2))  # Generamos 2 números, puedes cambiar esto
    signos_puntuacion = secrets.choice(string.punctuation)
    posicion_palabra = secrets.randbelow(len(parte_aleatoria))  # Usar randbelow para obtener un número aleatorio
    contraseña = (
        primera_letra +
        parte_aleatoria[:posicion_palabra] +
        palabra +
        parte_aleatoria[posicion_palabra:] +
        numeros +
        signos_puntuacion
    )

    return contraseña

def generar_contraseñas(num_contraseñas, longitud=12, palabra="Palabra"):
    contraseñas = []
    for _ in range(num_contraseñas):
        contraseñas.append(generar_contraseña(longitud, palabra))
    return contraseñas

if __name__ == "__main__":
    num_contraseñas = int(input("¿Cuántas contraseñas deseas generar? "))
    longitud = int(input("¿Cuántos caracteres debe tener cada contraseña? "))
    palabra = input("Introduce la palabra que quieres que aparezca en la contraseña: ")
    contraseñas = generar_contraseñas(num_contraseñas, longitud, palabra)
    df = pd.DataFrame(contraseñas, columns=["Contraseñas"])
    archivo_excel = "contrasenas_generadas.xlsx"
    df.to_excel(archivo_excel, index=False)

    print(f"Se han generado {num_contraseñas} contraseñas y se han guardado en '{archivo_excel}'")
20