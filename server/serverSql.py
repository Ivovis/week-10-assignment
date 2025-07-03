''' 
        serverSql.py
        simple server that stores sensor readings into a sqLite3 database
        includes example get routes 

        note FastAPI functions will run in different threads, so database connections must be opened and closed for each
'''

from fastapi import FastAPI     # type: ignore
from pydantic import BaseModel  # type: ignore
import sqlite3
import json

database = "test.db"

# universal key for json objects
keys = ['id','sensor','value','time']

# The definition of UpdateData
class UpdateData(BaseModel):
        name:str
        value:str
        time:str

# ensure table exists
dbConnection = sqlite3.connect(database)
cursor = dbConnection.cursor()

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

@app.post("/add")
def add(data:UpdateData):
    print(F"sensor:{data.name} value:{data.value} time:{data.time}")
    dbConnection = sqlite3.connect(database)
    cursor = dbConnection.cursor()
    cursor.execute(''' 
    INSERT INTO readings (sensor_name,sensor_value,sensor_time)
    values (?,?,?)
    ''',(data.name,data.value,data.time))
    dbConnection.commit()
    dbConnection.close()
    return{"message":"reading accepted"}

@app.get("/all")
def all():    
    dbConnection = sqlite3.connect(database)
    cursor = dbConnection.cursor()
    cursor.execute('SELECT * FROM readings')
    rows = cursor.fetchall()
    dbConnection.close()
    jsonData = [dict(zip(keys,item)) for item in rows] # convert tuples to list of dictionaries
    print(jsonData)

    # the dictionaries are converted to json here, keep in mind 
    # fastAPI will escape the quotes so we dont use this, its here as an example.
    jsonStr  = json.dumps(jsonData) # convert to json
    print(jsonStr)
    
    # We return the dictionaries and fastAPI will serialize them into json for us
    return (jsonData)

# get last ten readings
@app.get("/lastten")
def last_ten():    
    dbConnection = sqlite3.connect(database)
    cursor = dbConnection.cursor()
    cursor.execute('SELECT * FROM readings ORDER BY id DESC LIMIT 10')
    rows = cursor.fetchall()
    jsonData = [dict(zip(keys,item)) for item in rows]
    dbConnection.close()
    return (jsonData)

# get last reading
@app.get("/last")
def last():
    dbConnection = sqlite3.connect(database)
    cursor = dbConnection.cursor()
    cursor.execute('SELECT * FROM readings ORDER BY id DESC LIMIT 1')
    rows = cursor.fetchall()
    jsonData = [dict(zip(keys,item)) for item in rows]
    dbConnection.close()
    return (jsonData)

