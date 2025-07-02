from fastapi import FastAPI     # type: ignore
from pydantic import BaseModel  # type: ignore
import sqlite3
import json

# universal key for json objects
keys = ['id','sensor','value','time']

# The definition of UpdateData
class UpdateData(BaseModel):
        name:str
        value:str
        time:str

dbConnection = sqlite3.connect('test1.db')
cursor = dbConnection.cursor()

# ensure table exists
cursor.execute(''' 
    CREATE TABLE IF NOT EXISTS readings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        sensor_name TEXT NOT NULL,
        sensor_value TEXT NOT NULL,
        sensor_time TEXT NOT NULL
    )
'''
)
dbConnection.commit()
dbConnection.close()


app = FastAPI()

@app.get("/")
def root():
        return {"message": "System Online"}

@app.post("/update")
def add_reading(data:UpdateData):
        
        print(F"sensor:{data.name} value:{data.value} time:{data.time}")
        dbConnection = sqlite3.connect('test1.db')
        cursor = dbConnection.cursor()
        cursor.execute(''' 
        INSERT INTO readings (sensor_name,sensor_value,sensor_time)
        values (?,?,?)
        ''',(data.name,data.value,data.time))
        dbConnection.commit()
        dbConnection.close()
        return{"message":"reading accepted"}

@app.get("/getall")
def getAll():    
    dbConnection = sqlite3.connect('test1.db')
    cursor = dbConnection.cursor()
    cursor.execute('SELECT * FROM readings')
    rows = cursor.fetchall()
    jsonData = [dict(zip(keys,item)) for item in rows] # convert tuples to list of dictionaries
    print(jsonData)

    # we can convert it to json here, keep in mind fastAPI will escape the quotes ...
    jsonStr  = json.dumps(jsonData) # convert to json
    print(jsonStr)
    
    # so we just return the dictionaries and fastAPI will serialize them into json for us
    return (jsonData)



