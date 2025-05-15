import uvicorn
from fastapi import FastAPI
from routes import todos, idtodos

# FastAPI (웹) 인스턴스를 생성
app = FastAPI()
app.include_router(todos.todo_router)
app.include_router(idtodos.idtodo_router)

# 라우트 정의
@app.get("/")
async def welcome() -> dict:
    return {"mess age": "Hello World"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
