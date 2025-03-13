import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_google_drive():
    """Autentica el acceso y obtiene el token de acceso a Google Drive"""
    creds = None

    # Si existe el archivo token.pickle, cargar las credenciales guardadas
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # Si las credenciales no son válidas o no existen, obtener nuevas credenciales
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refrescar las credenciales si han expirado
        else:
            # La ruta del archivo credentials.json
            credentials_path = os.path.join(os.path.dirname(__file__), 'credentials', 'credentials.json')
            # Iniciar el flujo de autenticación
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            # Usar el flujo de consola (sin navegador) para autenticar
            creds = flow.run_console()

        # Guardar las credenciales en un archivo token.pickle para futuras ejecuciones
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    # Crear el servicio de Google Drive con las credenciales obtenidas
    service = build('drive', 'v3', credentials=creds)
    return service
