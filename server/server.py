'''
        server.py
        simple server to test "/" route
'''
from fastapi import FastAPI     # type: ignore
from pydantic import BaseModel  # type: ignore

# The definition of UpdateData
class UpdateData(BaseModel):
        name:str
        value:str
        time:str

app = FastAPI()

@app.get("/")
def root():
        return {"message": "Hello World"}

@app.post("/update")
def add_reading(data:UpdateData):
        print(F"sensor:{data.name} value:{data.value} time:{data.time}")
        return{"message":"reading accepted"}

