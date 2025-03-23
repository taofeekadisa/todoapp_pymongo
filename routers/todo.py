from fastapi import APIRouter, HTTPException
from crud.todo import todo_crud
from schemas import todo as todo_schema

router = APIRouter(prefix="/todos", tags=["Todos"])


@router.post("/", response_model=todo_schema.Todo)
async def create_todo(todo: todo_schema.TodoCreate):
    return todo_crud.create_todo(todo)


@router.get("/", response_model=list[todo_schema.TodoResponse])
async def get_todos():
    result = todo_crud.get_todos()
    return result

@router.get("/{todo_id}", response_model=dict)
async def get_todo(todo_id: str):
    result = todo_crud.get_todo(todo_id)
    if "error" in result:
        raise HTTPException(status_code=400 if "Invalid ObjectId" in result["error"] else 404, detail=result["error"])
    return result

@router.put("/{todo_id}", response_model=dict)
async def update_todo_endpoint(todo_id: str, todo_data: todo_schema.TodoUpdate):
    result = todo_crud.update_todo(todo_id, todo_data.dict(exclude_unset=True))
    if "error" in result:
        raise HTTPException(status_code=400 if "Invalid ObjectId" in result["error"] else 404, detail=result["error"])
    return result

@router.delete("/{todo_id}", response_model=dict)
async def delete_todo_endpoint(todo_id: str):
    result = todo_crud.delete_todo(todo_id)
    if "error" in result:
        raise HTTPException(status_code=400 if "Invalid ObjectId" in result["error"] else 404, detail=result["error"])
    return result