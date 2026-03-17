from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.utils.deps import get_db, get_current_user
from app.utils.auth import verify_password, hash_password
from app.models.user import User
from app.schemas.user import UserOut, UserUpdate, ChangePassword

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=UserOut)
def update_me(
    payload: UserUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if payload.full_name is not None:
        current_user.full_name = payload.full_name
    if payload.address is not None:
        current_user.address = payload.address
    if payload.mobile is not None:
        current_user.mobile = payload.mobile
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/me/change-password")
def change_password(
    payload: ChangePassword,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(payload.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    current_user.password = hash_password(payload.new_password)
    db.commit()
    return {"message": "Password updated successfully"}