from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.deps import get_db, get_current_seller
from app.models.storefront import StorefrontConfig
from app.schemas.storefront import StorefrontIn, StorefrontOut
import json

router = APIRouter(prefix="/storefront", tags=["Storefront"])

@router.get("", response_model=StorefrontOut)
def get_storefront(db: Session = Depends(get_db)):
    rows = db.query(StorefrontConfig).all()
    result = {}
    for row in rows:
        result[row.key] = json.loads(row.value)
    return result

@router.put("", response_model=StorefrontOut)
def update_storefront(payload: StorefrontIn, db: Session = Depends(get_db), _=Depends(get_current_seller)):
    data = payload.model_dump()
    for key, value in data.items():
        row = db.query(StorefrontConfig).filter(StorefrontConfig.key == key).first()
        if row:
            row.value = json.dumps(value)
        else:
            db.add(StorefrontConfig(key=key, value=json.dumps(value)))
    db.commit()
    return data