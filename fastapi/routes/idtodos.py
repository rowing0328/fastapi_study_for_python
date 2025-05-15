from fastapi import APIRouter
from .todos import todo_list
from models.model import IdItems

idtodo_router = APIRouter(prefix="/idtodos")

# id + item 형식으로 할일 목록 반환
# GET http://localhost:8000/idtodos
@idtodo_router.get("", response_model=IdItems)
async def retrive_idtodos() -> dict:
    result = []
    for todo in todo_list:
        result.append({"iditem": f"{todo.id} {todo.item}"})
    return {"iditems": result}
