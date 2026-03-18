from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from app.config import settings

conf = ConnectionConfig(
    MAIL_USERNAME   = settings.MAIL_USERNAME,
    MAIL_PASSWORD   = settings.MAIL_PASSWORD,
    MAIL_FROM       = settings.MAIL_FROM,
    MAIL_PORT       = settings.MAIL_PORT,
    MAIL_SERVER     = settings.MAIL_SERVER,
    MAIL_STARTTLS   = True,
    MAIL_SSL_TLS    = False,
    USE_CREDENTIALS = True,
)
 
async def send_verification_email(email: str, full_name: str, token: str):
    verify_url = f"http://localhost:8000/auth/verify-email?token={token}"
 
    html = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px;">
        <div style="text-align: center; margin-bottom: 30px;">
            <h1 style="color: #7a8c6e;"><FiberNest</h1>
            <img>src="/frontend/assets/img/logo.png" alt="FiberNest Logo" style="width: 80px; height: 80px;">
        </div>
        <h2 style="color: #2a2a2a;">Hi {full_name}, verify your email!</h2>
        <p style="color: #6b6b6b; line-height: 1.6;">
            Thank you for registering at FiberNest. Please click the button below to verify your email address and activate your account.
        </p>
        <div style="text-align: center; margin: 30px 0;">
            <a href="{verify_url}"
               style="background-color: #7a8c6e; color: white; padding: 14px 32px;
                      text-decoration: none; border-radius: 8px; font-weight: bold;
                      font-size: 16px; display: inline-block;">
                Verify Email Address
            </a>
        </div>
        <p style="color: #6b6b6b; font-size: 13px;">
            Or copy and paste this link into your browser:<br>
            <a href="{verify_url}" style="color: #7a8c6e;">{verify_url}</a>
        </p>
        <p style="color: #6b6b6b; font-size: 13px;">
            This link will expire in 24 hours. If you did not create an account, you can safely ignore this email.
        </p>
        <hr style="border: none; border-top: 1px solid #e5e1da; margin: 30px 0;">
        <p style="color: #b0aba3; font-size: 11px; text-align: center;">
            © 2025 FiberNest. For educational purposes only, and no copyright infringement is intended.
        </p>
    </div>"""
    
 
    message = MessageSchema(
        subject="Verify your FiberNest account",
        recipients=[email],
        body=html,
        subtype=MessageType.html,
    )
 
    fm = FastMail(conf)
    await fm.send_message(message)