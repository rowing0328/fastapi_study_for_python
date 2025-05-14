from fastapi import FastAPI
from routes import todos

# FastAPI (웹) 인스턴스를 생성
app = FastAPI()
app.include_router(todos.todo_router)

# 라우트 정의
@app.get("/")
async def welcome() -> dict:
    return {"mess age": "Hello World"}
