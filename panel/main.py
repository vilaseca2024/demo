import importlib
import pkg_resources
import sys

librerias = {
    'asgiref': '3.8.1', 
    'bcrypt': '4.2.1',
    'cachetools': '5.5.1',
    'certifi': '2025.1.31',
    'cffi': '1.17.1',
    'chardet': '5.2.0',
    'charset-normalizer': '3.4.1',
    'colorama': '0.4.6',
    'cryptography': '44.0.1',
    'Django': '5.1.6',
    'google-api-core': '2.24.1',
    'google-api-python-client': '2.161.0',
    'google-auth': '2.38.0',
    'google-auth-httplib2': '0.2.0',
    'google-auth-oauthlib': '1.2.1',
    'googleapis-common-protos': '1.67.0',
    'httplib2': '0.22.0',
    'idna': '3.10',
    'numpy': '2.2.3',
    'oauthlib': '3.2.2',
    'pandas': '2.2.3',
    'pillow': '11.1.0',
    'proto-plus': '1.26.0',
    'protobuf': '5.29.3',
    'pyasn1': '0.6.1',
    'pyasn1-modules': '0.4.1',
    'pycparser': '2.22',
    'pyparsing': '3.2.1',
    'python-dateutil': '2.9.0.post0',
    'pytz': '2025.1',
    'qrcode': '8.0',
    'reportlab': '4.3.1',
    'requests': '2.32.3',
    'requests-oauthlib': '2.0.0',
    'rsa': '4.9',
    'six': '1.17.0',
    'sqlparse': '0.5.3',
    'typing-extensions': '4.12.2',
    'tzdata': '2025.1',
    'uritemplate': '4.1.1',
    'urllib3': '2.3.0'
}


def verificar_librerias():
    librerias_faltantes = []
    librerias_desactualizadas = []

    for libreria, version_requerida in librerias.items():
        try:
            importlib.import_module(libreria)
            version_instalada = pkg_resources.get_distribution(libreria).version
            if pkg_resources.parse_version(version_instalada) < pkg_resources.parse_version(version_requerida):
                librerias_desactualizadas.append(f"{libreria} (Instalada: {version_instalada}, Requerida: {version_requerida})")
            else:
                print(f"{libreria} está instalada (Versión: {version_instalada})")
        except ImportError:
            print(f"{libreria} NO está instalada.")
            librerias_faltantes.append(libreria)

    if librerias_faltantes:
        print("\nFaltan las siguientes librerías:")
        for libreria in librerias_faltantes:
            print(f"- {libreria}")

    if librerias_desactualizadas:
        print("\nLas siguientes librerías están desactualizadas:")
        for libreria in librerias_desactualizadas:
            print(f"- {libreria}")

    if not librerias_faltantes and not librerias_desactualizadas:
        print("\nTodas las librerías están instaladas y actualizadas.")

    input("presiona ENTER para cerrar..............")


if __name__ == "__main__":
    verificar_librerias()
