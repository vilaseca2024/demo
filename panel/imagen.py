import mailbox

def leer_mbox(archivo_mbox):
    # Abrir el archivo MBOX
    mbox = mailbox.mbox(archivo_mbox)

    for mensaje in mbox:
        print("=" * 50)
        print(f"De: {mensaje['from']}")
        print(f"Asunto: {mensaje['subject']}")
        print("Cuerpo:")
        
        if mensaje.is_multipart():
            # Si el mensaje tiene múltiples partes, obtener el texto plano
            for parte in mensaje.walk():
                if parte.get_content_type() == "text/plain":
                    print(parte.get_payload(decode=True).decode('utf-8', errors='ignore'))
        else:
            print(mensaje.get_payload(decode=True).decode('utf-8', errors='ignore'))

        print("=" * 50)

# Llamar la función con el archivo MBOX
leer_mbox("respaldo.mbox")
