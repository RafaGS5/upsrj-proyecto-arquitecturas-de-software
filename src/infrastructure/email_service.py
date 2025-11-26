# ============================================================
# Servicio para enviar correos de aprobación de binarios
# ============================================================

from flask_mail import Message
from flask import url_for, current_app
import traceback


class EmailService:
    """
    Servicio encargado de enviar el correo con el enlace de aprobación.
    Usa la configuración de Flask-Mail definida en main.py.
    """

    def send_approval_email(self, recipient_email: str, file_id: str, filename: str) -> bool:
        """
        Envía un correo con el enlace de aprobación:
        GET /approve/<file_id>

        Retorna:
            True si se envió correctamente, False si hubo error.
        """
        try:
            # Genera el enlace absoluto (http://host:puerto/approve/<id>)
            approval_link = url_for("approve_file", file_id=file_id, _external=True)

            # Crear el mensaje
            msg = Message(
                subject=f"Requiere aprobación: {filename}",
                recipients=[recipient_email],
                body=f"""
SOLICITUD DE FIRMA PARA PRODUCCIÓN

El archivo '{filename}' ha sido subido y está en espera de aprobación.

Para aprobarlo y firmarlo digitalmente, haga clic aquí:
{approval_link}

Si usted no solicitó esto, puede ignorar este mensaje.
"""
            )

            print(f"[EmailService] Enviando correo a: {recipient_email}")
            print(f"[EmailService] Enlace de aprobación: {approval_link}")

            # Enviar usando la instancia de Flask-Mail (app.mail)
            current_app.mail.send(msg)

            print("[EmailService] Correo enviado correctamente.")
            return True

        except Exception as e:
            print("[EmailService] ERROR al enviar correo:")
            print(e)
            traceback.print_exc()
            return False
