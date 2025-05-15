from fastapi import APIRouter, Path, Query, HTTPException
from models.model import Todo, TodoItem, TodoItems, IdItems

todo_router = APIRouter()

# 할일 정보를 저장할 리스트 => 이후에 DB 연동으로 변경
todo_list = []

# -------------------------------
# 할일 데이터를 저장할 모델을 정의
from pydantic import BaseModel

class Todo(BaseModel):
    id: int
    item: str
# -------------------------------

# 할일 추가
# POST http://localhost:8000/todo
@todo_router.post("/todo", status_code=201)
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
# @todo_router.get("/todos")
# async def retrives_todos() -> dict:
#     return {"todos": todo_list}

# 할일 목록 조회
# GET http://localhost:8000/todos
@todo_router.get("/todos", response_model=TodoItems)
async def retrives_todos() -> dict:
    result = []
    for todo in todo_list:
        result.append({"item": todo.item})
    return {"items": result}



# # 할일 상세 조회
# # GET http://localhost:8000/todo/{todo_id}
# @todo_router.get("/todo/{todo_id}")
# async def retrive_todo(todo_id: int) -> dict:
#     for todo in todo_list:
#         if todo.id == todo_id:
#             return {"todo": todo}
        
#     return {"message": "일치하는 할 일이 없습니다."}

# 할일 상세 조회
# GET http://localhost:8000/todos/1  ==> id 항목의 값이 1인 할 일 정보를 반환
@todo_router.get("/todo/search/{todo_id}", status_code=200)
async def retrive_todo(todo_id: int = Path(..., title="조회할 할 일의 ID", ge=1)) -> dict:
    # todo_list 변수에는 아래와 같은 형식의 값이 저장
    # [{id: 1, item: "파이썬 공부"}, {id: 2, item: "FastAPI 공부"}]
    for todo in todo_list:
        if todo.id == todo_id:
            return {"todo": todo}
        
    # return {"message": "일치하는 할 일이 없습니다."}    
    raise HTTPException(status_code=404, detail=f"ID가 {todo_id}인 할 일을 찾을 수 없습니다.")


# 할일 검색
# # http://localhost:8000/todos/search?item=검색어
# @todo_router.get("/todo/search")
# async def search_todos(item: str) -> dict:
#     result = []
#     for todo in todo_list:
#         if item in todo.item:
#             result.append(todo)
#     return {"todos": result}

# 관련된 할일 검색
# 할일 검색 기능에 item 항목의 값을 필수 입력으로, 최소 2자리, 최대 10자리로 설정
@todo_router.get("/todos/search")
async def search_todos(item: str = Query(..., min_length=2, max_length=10, title="할 일 목록 검색어")) -> dict:
    result = []
    for todo in todo_list:
        if item in todo.item:
            result.append(todo)
    return {"todos": result}

# 할일 수정
# PUT http://localhost:8000/todo/1
# @todo_router.put("/todo/{todo_id}")
# async def update_todo(
#     todo_id: int = Path(..., title="수정할 할 일 ID", ge=1),
#     item: str = Query(..., min_length=1, max_length=100, title="수정할 할 일 내용")
# ) -> dict:
#     for todo in todo_list:
#         if todo.id == todo_id:
#             todo.item = item
#             return {"message": "할 일을 수정했습니다.", "todo": todo}
        
#     return {"message": "수정 할 일이 없습니다."}

# 할일 수정
# PUT http://localhost:8000/todo/1
@todo_router.put("/todo/{todo_id}")
async def update_todo(
    todo_id: int = Path(..., title="수정할 할 일 ID", ge=1),
    new_todo: TodoItem = None
) -> dict:
    for todo in todo_list:
        if todo.id == todo_id:
            todo.item = new_todo.item
            return {"message": "할 일을 수정했습니다.", "todo": todo}
        
    return {"message": "수정 할 일이 없습니다."}

# 할 일 삭제
# DELETE http://localhost:8000/todo/1
@todo_router.delete("/todo/{todo_id}")
async def delete_todo(
    todo_id: int = Path(..., title="삭제할 할 일 ID", ge=1)
) -> dict:
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            deleted_Todo = todo_list.pop(index)
            return {"message": "할 일을 삭제했습니다.", "todo": deleted_Todo}
    
    return {"message": "삭제 할 일이 없습니다."}
    raise HTTPException(status_code=404, detail="일치하는 할 일이 없습니다.")
