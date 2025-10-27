# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: test_main.py
# Descripción: Archivo de pruebas unitarias para validar el comportamiento de funciones del proyecto
# ============================================================
import sys
import unittest
from vars import *

sys.path.insert(0, BASE_DIR)

import main

class TestCryptography(unittest.TestCase):

    def test_cryptography(self):
        # Recuperar objetos desde main
        key = main.key
        fernet = main.f
        token = main.token

        # Validaciones didácticas
        self.assertIsInstance(key, bytes, "La clave debe ser de tipo bytes")
        self.assertIsInstance(token, bytes, "El token debe ser de tipo bytes")
        self.assertTrue(len(token) > 0, "El token no debe estar vacío")

        # Desencriptar y validar
        decrypted = fernet.decrypt(token)
        expected = b"A really secret message. Not for prying eyes."
        self.assertEqual(decrypted, expected, "El mensaje desencriptado debe coincidir con el original")
        
        print("Everything fine with cryptography.")
        
if __name__ == '__main__':
    unittest.main()