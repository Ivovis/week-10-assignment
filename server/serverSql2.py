from fastapi import FastAPI,Depends     # type: ignore
from pydantic import BaseModel  # type: ignore
from sqlmodel import SQLModel,Field,create_engine,Session #type:ignore

class Reading(SQLModel, table=True): #type:ignore
    id: int = Field(default=None, primary_key=True)
    name: str
    value: str
    time: str

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# The definition of UpdateData
class UpdateData(BaseModel):
        name:str
        value:str
        time:str

    
engine = create_engine("sqlite:///./test.db")
def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()

@app.on_event("startup") 
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
        return {"message": "Hello World"}

@app.post("/update")
def add_reading(data: UpdateData, session: Session = Depends(get_session)):
    print(f"sensor:{data.name} value:{data.value} time:{data.time}")
    reading = Reading(name=data.name, value=data.value, time=data.time)
    session.add(reading)
    session.commit()
    session.refresh(reading)
    return {"message": "reading accepted"}


