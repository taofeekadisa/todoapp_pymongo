from fastapi import APIRouter
from crud.user import user_crud
from schemas import user as user_schema

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(user: user_schema.UserCreate):
    return user_crud.create_user(user)
