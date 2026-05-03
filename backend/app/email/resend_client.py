"""
Resend API client for sending emails.
"""
import os
import logging
from typing import Optional

try:
    import resend
    RESEND_AVAILABLE = True
except ImportError:
    RESEND_AVAILABLE = False
    resend = None

logger = logging.getLogger(__name__)


class ResendClient:
    """Client for sending emails via Resend API."""

    def __init__(self):
        self.api_key = os.getenv("RESEND_API_KEY", "")
        self.from_email = os.getenv("RESEND_FROM_EMAIL", "onboarding@resend.dev")
        self.enabled = bool(self.api_key) and RESEND_AVAILABLE

        if not self.api_key:
            logger.warning("RESEND_API_KEY not set - email sending disabled")
        elif not RESEND_AVAILABLE:
            logger.warning("resend package not installed - email sending disabled")

    def _get_client(self):
        if not self.enabled:
            return None
        return resend.Resend(self.api_key)

    def send_email(self, to: str, subject: str, html: str, text: Optional[str] = None) -> dict:
        """
        Send a generic email.

        Args:
            to: Recipient email address
            subject: Email subject
            html: HTML body content
            text: Optional plain text version

        Returns:
            dict with 'success' and 'message_id' or 'error' keys
        """
        if not self.enabled:
            logger.info(f"[TEST MODE] Would send email to {to}: {subject}")
            return {"success": True, "message_id": "test_mode_no_send", "test_mode": True}

        try:
            client = self._get_client()
            params = {
                "from": self.from_email,
                "to": to,
                "subject": subject,
                "html": html,
            }
            if text:
                params["text"] = text

            result = client.email.send(params)
            logger.info(f"Email sent to {to}, message_id={result.get('id')}")
            return {"success": True, "message_id": result.get("id")}
        except Exception as e:
            logger.error(f"Failed to send email to {to}: {e}")
            return {"success": False, "error": str(e)}

    def send_welcome_email(self, user_email: str, name: str, establishment_name: str = "Establecimiento GPP") -> dict:
        """
        Send a welcome email to a new user.

        Args:
            user_email: Recipient email
            name: User's name
            establishment_name: Name of their establishment

        Returns:
            dict with success status and message_id or error
        """
        subject = f"Bienvenido a {establishment_name}"
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
                .button {{ display: inline-block; background: #667eea; color: white; padding: 12px 30px; border-radius: 6px; text-decoration: none; font-weight: 600; margin: 20px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>¡Bienvenido, {name}!</h1>
            </div>
            <div class="content">
                <p>Gracias por unirte a <strong>{establishment_name}</strong>. Estamos encantados de tenerte a bordo.</p>
                <p>Con nuestra herramienta podrás:</p>
                <ul>
                    <li>Evaluar tus procesos operativos</li>
                    <li>Crear planes de acción concretos</li>
                    <li>Comparar tu rendimiento con estándares de la industria</li>
                    <li>Generar informes profesionales en PDF</li>
                </ul>
                <p style="text-align: center;">
                    <a href="#" class="button">Comenzar primera evaluación</a>
                </p>
                <p>Si tienes alguna pregunta, no dudes en contactarnos.</p>
                <p>Saludos,<br>El equipo de {establishment_name}</p>
            </div>
            <div class="footer">
                Este email fue enviado porque te registraste en {establishment_name}.
            </div>
        </body>
        </html>
        """
        return self.send_email(user_email, subject, html)

    def send_action_plan_reminder(self, user_email: str, action_plans: list) -> dict:
        """
        Send an action plan reminder email.

        Args:
            user_email: Recipient email
            action_plans: List of dicts with 'title', 'due_date', 'status' keys

        Returns:
            dict with success status and message_id or error
        """
        if not action_plans:
            return {"success": True, "message_id": "no_plans", "skipped": True}

        subject = "Recordatorio: Planes de acción pendientes"
        plans_html = ""
        for plan in action_plans:
            due_date = plan.get("due_date", "Sin fecha")
            status = plan.get("status", "pending")
            status_color = "#ffc107" if status == "pending" else "#dc3545" if status == "overdue" else "#28a745"

            plans_html += f"""
            <tr>
                <td style="padding: 12px; border-bottom: 1px solid #eee;">{plan.get('title', 'Sin título')}</td>
                <td style="padding: 12px; border-bottom: 1px solid #eee;">{due_date}</td>
                <td style="padding: 12px; border-bottom: 1px solid #eee;">
                    <span style="background: {status_color}; color: white; padding: 4px 8px; border-radius: 4px; font-size: 12px;">
                        {status.upper()}
                    </span>
                </td>
            </tr>
            """

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
                table {{ width: 100%; border-collapse: collapse; margin: 20px 0; }}
                th {{ background: #333; color: white; padding: 12px; text-align: left; }}
                .button {{ display: inline-block; background: #f5576c; color: white; padding: 12px 30px; border-radius: 6px; text-decoration: none; font-weight: 600; margin: 20px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📋 Recordatorio de Planes de Acción</h1>
                <p>Tienes {len(action_plans)} plan(es) que requieren atención</p>
            </div>
            <div class="content">
                <table>
                    <thead>
                        <tr>
                            <th>Plan</th>
                            <th>Fecha Límite</th>
                            <th>Estado</th>
                        </tr>
                    </thead>
                    <tbody>
                        {plans_html}
                    </tbody>
                </table>
                <p style="text-align: center;">
                    <a href="#" class="button">Ver todos los planes</a>
                </p>
                <p>No dejes que tus tareas se acumulen. Revisa y actualiza el estado de tus planes de acción.</p>
            </div>
            <div class="footer">
                Este es un email automático. No respondas a este mensaje.
            </div>
        </body>
        </html>
        """
        return self.send_email(user_email, subject, html)

    def send_weekly_summary(self, user_email: str, stats: dict) -> dict:
        """
        Send a weekly summary email.

        Args:
            user_email: Recipient email
            stats: dict with 'evaluations_completed', 'pending_action_plans', 'overdue_action_plans' keys

        Returns:
            dict with success status and message_id or error
        """
        evaluations = stats.get("evaluations_completed", 0)
        pending = stats.get("pending_action_plans", 0)
        overdue = stats.get("overdue_action_plans", 0)

        subject = "Resumen Semanal - Tu actividad en GPP"
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <style>
                body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); color: white; padding: 30px; border-radius: 8px 8px 0 0; text-align: center; }}
                .content {{ background: #f8f9fa; padding: 30px; border-radius: 0 0 8px 8px; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; text-align: center; }}
                .stat {{ flex: 1; }}
                .stat-number {{ font-size: 2em; font-weight: bold; color: #4facfe; }}
                .stat-label {{ color: #666; font-size: 14px; }}
                .button {{ display: inline-block; background: #4facfe; color: white; padding: 12px 30px; border-radius: 6px; text-decoration: none; font-weight: 600; margin: 20px 0; }}
                .footer {{ text-align: center; color: #666; font-size: 12px; margin-top: 20px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Tu Resumen Semanal</h1>
                <p>Así fue tu actividad esta semana</p>
            </div>
            <div class="content">
                <div class="stats">
                    <div class="stat">
                        <div class="stat-number">{evaluations}</div>
                        <div class="stat-label">Evaluaciones completadas</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number">{pending}</div>
                        <div class="stat-label">Planes pendientes</div>
                    </div>
                    <div class="stat">
                        <div class="stat-number" style="color: #dc3545;">{overdue}</div>
                        <div class="stat-label">Planes vencidos</div>
                    </div>
                </div>
                <p style="text-align: center;">
                    <a href="#" class="button">Ver dashboard</a>
                </p>
                <p>¡Sigue así! La evaluación constante de tus procesos es clave para la mejora continua.</p>
            </div>
            <div class="footer">
                Para dejar de recibir estos emails, actualiza tu configuración de notificaciones.
            </div>
        </body>
        </html>
        """
        return self.send_email(user_email, subject, html)


# Singleton instance
resend_client = ResendClient()