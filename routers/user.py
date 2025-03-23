from fastapi import APIRouter, HTTPException
from crud.user import user_crud
from schemas import user as user_schema

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/")
def create_user(user: user_schema.UserCreate):
    return user_crud.create_user(user)

@router.get("/", response_model=list[user_schema.User])
def get_users():
    return user_crud.get_users()

@router.get("/{user_id}")
def get_user(user_id):
    user = user_crud.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=dict)
async def update_user(user_id: str, user_data: user_schema.UserUpdate):
    result = user_crud.update_user(user_id, user_data.dict(exclude_unset=True))

    if "error" in result:
        raise HTTPException(status_code=400 if "Invalid ObjectId" in result["error"] else 404, detail=result["error"])

    return result

@router.delete("/{user_id}", response_model=dict)
async def delete_user(user_id: str):
    result = user_crud.delete_user(user_id)

    if "error" in result:
        raise HTTPException(status_code=400 if "Invalid ObjectId" in result["error"] else 404, detail=result["error"])

    return result
