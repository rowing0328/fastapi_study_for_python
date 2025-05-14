from fastapi import APIRouter

todo_router = APIRouter()

# 할 일 정보를 저장할 리스트 => 이후에 DB 연동으로 변경
todo_list = []

# -------------------------------
# 할 일 데이터를 저장할 모델을 정의
from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    item: str
# -------------------------------

# 할일 추가
# POST http://localhost:8000/todo
@todo_router.post("/todo")
# async def add_todo(todo: dict) -> dict:
async def add_todo(todo: Todo) -> dict:
    # 중복 ID 검사
    for existing in todo_list:
        if existing.id == todo.id:
            return {"message": "중복된 ID입니다."}

    # todo_list 리스트에 todo 변수의 내용을 추가
    todo_list.append(todo)
    return {"message": "할 일을 추가했습니다.", "todo": todo}

# 할일 목록 조회
# GET http://localhost:8000/todos
@todo_router.get("/todos")
async def retrives_todos() -> dict:
    return {"todos": todo_list}

# 할일 상세 조회
# GET http://localhost:8000/todo/{todo_id}
@todo_router.get("/todo/{todo_id}")
async def retrive_todo(todo_id: int) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            return {"todo": todo}
        
    return {"message": "일치하는 할 일이 없습니다."}
        