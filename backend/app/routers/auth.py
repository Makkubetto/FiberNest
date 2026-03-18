import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.utils.deps import get_db
from app.utils.auth import hash_password, verify_password, create_access_token
from app.utils.email import send_verification_email
from app.models.user import User
from app.models.verification import EmailVerification
from app.schemas.user import UserRegister, UserOut

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserOut, status_code=201)
async def register(
    payload: UserRegister,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    try:
        existing = db.query(User).filter(User.email == payload.email).first()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered")

        user = User(
            email       = payload.email,
            password    = hash_password(payload.password),
            full_name   = payload.full_name,
            address     = payload.address,
            mobile      = payload.mobile,
            role        = payload.role if payload.role in ("buyer", "seller") else "buyer",
            is_verified = False,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

        token = secrets.token_urlsafe(32)
        verification = EmailVerification(user_id=user.id, token=token)
        db.add(verification)
        db.commit()

        background_tasks.add_task(
            send_verification_email,
            email     = user.email,
            full_name = user.full_name,
            token     = token,
        )

        return user
    except HTTPException:
        raise
    except Exception as e:
        print(f"REGISTER ERROR: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail=f"{type(e).__name__}: {str(e)}")


@router.get("/verify-email", response_class=HTMLResponse)
def verify_email(token: str, db: Session = Depends(get_db)):
    verification = db.query(EmailVerification).filter(
        EmailVerification.token == token,
        EmailVerification.is_used == False,
    ).first()

    if not verification:
        return HTMLResponse(content=_page(
            "❌ Invalid or Expired Link",
            "This verification link is invalid or has already been used.",
            success=False
        ))

    age = datetime.utcnow() - verification.created_at
    if age > timedelta(hours=24):
        return HTMLResponse(content=_page(
            "⏰ Link Expired",
            "This verification link has expired. Please register again.",
            success=False
        ))

    user = db.query(User).filter(User.id == verification.user_id).first()
    if not user:
        return HTMLResponse(content=_page(
            "❌ User Not Found",
            "Something went wrong. Please contact support.",
            success=False
        ))

    user.is_verified = True
    verification.is_used = True
    db.commit()

    return HTMLResponse(content=_page(
        "✅ Email Verified!",
        f"Hi {user.full_name}, your FiberNest account is now active. You can now log in.",
        success=True
    ))


@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form.username).first()

    if not user or not verify_password(form.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    if not user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Please verify your email address before logging in. Check your inbox.",
        )

    token = create_access_token({"sub": str(user.id), "role": user.role})
    return {"access_token": token, "token_type": "bearer"}


@router.post("/resend-verification")
async def resend_verification(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Email not found")
    if user.is_verified:
        raise HTTPException(status_code=400, detail="Account is already verified")

    db.query(EmailVerification).filter(
        EmailVerification.user_id == user.id,
        EmailVerification.is_used == False,
    ).update({"is_used": True})
    db.commit()

    token = secrets.token_urlsafe(32)
    verification = EmailVerification(user_id=user.id, token=token)
    db.add(verification)
    db.commit()

    background_tasks.add_task(
        send_verification_email,
        email     = user.email,
        full_name = user.full_name,
        token     = token,
    )

    return {"message": "Verification email resent. Please check your inbox."}


def _page(title: str, message: str, success: bool = True) -> str:
    color = "#7a8c6e" if success else "#c0392b"
    btn_href = "http://127.0.0.1:5500/frontend/buyer/login.html"
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title} - FiberNest</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ font-family: Arial, sans-serif; background: #f8f5f0; display: flex; align-items: center; justify-content: center; min-height: 100vh; }}
            .card {{ background: white; border-radius: 16px; padding: 48px; max-width: 480px; width: 90%; text-align: center; box-shadow: 0 4px 24px rgba(0,0,0,0.08); }}
            h1 {{ font-size: 28px; color: #2a2a2a; margin-bottom: 16px; }}
            p {{ color: #6b6b6b; line-height: 1.6; margin-bottom: 24px; }}
            a {{ display: inline-block; background: {color}; color: white; padding: 12px 28px; border-radius: 8px; text-decoration: none; font-weight: bold; }}
            .logo {{ font-size: 48px; margin-bottom: 16px; }}
            small {{ color: #b0aba3; font-size: 11px; display: block; margin-top: 24px; }}
        </style>
    </head>
    <body>
        <div class="card">
            <div class="logo">🌿</div>
            <h1>{title}</h1>
            <p>{message}</p>
            <a href="{btn_href}">{"Go to Login" if success else "Back to Home"}</a>
            <small>© 2025 FiberNest. For educational purposes only, and no copyright infringement is intended.</small>
        </div>
    </body>
    </html>
    """