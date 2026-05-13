from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.services.auth_service import login_user, register_user
from app.schemas.user import UserRegister, UserLogin, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


# =========================
# LOGIN
# =========================
@router.post("/login")
def login(
    data: UserLogin,
    db: Session = Depends(get_db),
):
    return login_user(db, data)


# =========================
# REGISTER
# =========================
@router.post("/register", response_model=UserResponse)
def register(
    data: UserRegister,
    db: Session = Depends(get_db),
):
    return register_user(db, data)