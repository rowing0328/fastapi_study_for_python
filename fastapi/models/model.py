from pydantic import BaseModel
from typing import List

class Todo(BaseModel):
    id: int
    item: str

class TodoItem(BaseModel):
    item: str

class TodoItems(BaseModel):
    items: List[TodoItem]

class IdItem(BaseModel):
    iditem: str

class IdItems(BaseModel):
    iditems: List[IdItem]
