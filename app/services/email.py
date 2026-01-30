import aiosmtplib
from email.message import EmailMessage

from app.core.config import settings
from app.core.logger import get_logger

logger = get_logger("email")


class EmailService:
    @staticmethod
    async def send_order_confirmation(email: str, order_id: str):
        logger.info(f"email_send_start order_id={order_id}")

        message = EmailMessage()
        message["From"] = settings.SMTP_FROM
        message["To"] = email
        message["Subject"] = "Order Confirmation"

        message.set_content(
            f"""
Hello,

Your order {order_id} has been successfully placed.

Thank you for shopping with us!

Best,
E-Commerce Team
"""
        )

        try:
            await aiosmtplib.send(
                message,
                hostname=settings.SMTP_HOST,
                port=settings.SMTP_PORT,
                username=settings.SMTP_USER,
                password=settings.SMTP_PASS,
                start_tls=True,
            )

            logger.info(
                f"email_sent order_id={order_id} to={email}"
            )

        except Exception as e:
            logger.error(
                f"email_failed order_id={order_id} error={str(e)}"
            )
            raise
