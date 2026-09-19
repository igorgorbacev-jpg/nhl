
from pydantic import BaseModel,Field
from fastapi import FastAPI, Body,UploadFile
from typing import Optional
import cloudpickle
import io
import pandas as pd



with open("pipeline.pkl", "rb") as f:
   pipeline = cloudpickle.load(f)


app = FastAPI()
info = {'id': 1, 'name': '1', 'last_name': '1'}
class Our(BaseModel):
   a:int = Field(default=5,description="Это наш класс")
   b:int = Field(default=10,description="Это наш класс")
   c:int = Field(default=10,description="Это наш класс")

app = FastAPI()

@app.post("/model")
async def m(file:UploadFile):
   contents = await file.read()
   df = pd.read_csv(io.BytesIO(contents))
   pred = pipeline.predict(df)
   return {"predictions": pred.tolist()}



@app.get("/")
async def root(a:int, b:int):
   return {"its": a+b}
@app.get("/compyt")
async def compyt(a:int,b:int,c:int):
   return "right"
@app.post("/p")
async def p(a:int,b:int,c:int):
   return {"i am": a+b+c}
@app.post("/d")
async def d(our_class:Our):
   our_class_json = our_class.model_dump()
   return {"answer":(our_class.a + our_class.b + our_class.c)/3}

info = {'id': 1, 'name': '1', 'last_name': '1'}
users_db = {
    1: {"id": 1, "name": "Alice", "last_name": "Smith"},
    2: {"id": 2, "name": "Bob", "last_name": "Johnson"}
}

class UserUpdate(BaseModel):
    id: Optional[int] = None 
    name: Optional[str] = None
    last_name: Optional[str] = None

@app.put('/put')
async def update_user(user: UserUpdate):
    info['id'] = user.id
    info['name'] = user.name
    info['last_name'] = user.last_name
    return info 
@app.patch('/patch/{user_id}')
async def update_user_for_patch(user_id: int, user: UserUpdate):
    update_data = user.dict(exclude_unset=True)
    users_db[user_id].update(update_data)
    return users_db[user_id]

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
   users_db.pop(user_id)
   return 'its work'






