# dummy_binary_with_message.py
import os

# Mensaje secreto legible (puede incluir tu firma, fecha, etc.)
mensaje = b"Mensaje secreto: firmado por Rafael, 12/11/2025\n"

# Tamaño total del archivo en bytes
tamano_total = 1024  # 1 KB

# Relleno binario aleatorio para completar el archivo
relleno = os.urandom(tamano_total - len(mensaje))

# Combina el mensaje con el relleno
contenido = mensaje + relleno

# Guarda el archivo
with open("dummy_firmable.bin", "wb") as f:
    f.write(contenido)

print("Archivo binario con mensaje secreto generado: dummy_firmable.bin")