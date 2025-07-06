# week-10-assignment

API based home automation server

We have decided to create an small automation server suitable as the core for a home automation system, to keep things simple we will only be using the system to record temperature measurements, the Automation server (from here on referred to as just the server) will accept new temperature readings via the API and record them in a database.

The server needs to be lightweight so it can be run on a single board computer running a headless debian based Linux distribution.

We will be researching two programming languages to use on the server, Python and Java.

The server will provide an API to post new and fetch past temperature readings from a local database running on the same SBC allowing for a simple self contained solution. the SBC is expected to be running on a private network.

This repository covers the Python solution, you can find the Java solution <a href="https://github.com/lukeplechaty/week10project">Here</a>

---

#### Set up the environment on a target SBC like the Raspberry Pi

Check you have python installed, any version above 3.10

```
        $ python --version
        Python 3.12.3
```

If you get the following:

```
        zsh: command not found python
```

You will need to Google installing python for your system, before continuing.

1.  Create a directory to hold your python server and cd into it

```
        $ mkdir server
        $ cd server
```

2.  Create a python environment, This will create and environment where any packages you install will be kept local to this project. the .venv is a hidden directory, note it can be given any other name.

```
        $ python -m venv .venv
```

3.  You need to activate the environment before you can use it, note the command line prompt will change to show it is active. (you can type 'deactivate' to leave the environment later.)

```
        Linux $ source .venv/bin/activate

        Windows CMD $  .venv\Scripts\activate.bat

        PowerShell  $   .venv\Scripts\activate.ps1
```

4.  Now you are in the environment you can use pip to install packages ...

```
        $ pip install fastapi uvicorn json
```

5.  build a simple test server, use a text editor to create a file server.py containing the following:

```python

        from fastapi import FastAPI

        app = FastAPI()

        @app.get("/")
        def root():
                return {"message": "Hello World"}
```

6.  run the server using uvicorn

```

        $ uvicorn server:app --host 0.0.0.0 --port 8000

```

Now visit localhost:8000 to see the server is working.

FastAPI has a neat trick, it documents its routes and provides interactive access for testing in the browser, if you visit localhost:8000/docs, later when you add post routes you will be able to test them using the docs.

Below we have a post route to accept sensor name, temperature value and time, these are all defined as string to allow flexibility in the format so '33C', '33' and '33 centigrade' can all be used and the date can be in any short or long form format.

```python
        from fastapi import FastAPI
        from pydantic import BaseModel

        # UpdateData
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
```

---

### Writing to the database

I chose to use mySql3 but there are other more complex and sophisticated packages.

```python

        from fastapi import FastAPI
        from pydantic import BaseModel
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
            # fastAPI will escape the quotes so we don't use this, its here as an example.
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
```

Note that the database connections need to be created within the scope of each route function, this is because the fastAPI package runs each of these in a different thread

---

### Testing

To test the system you can use the fastAPI created docs at localhost:8000/docs but I added a test sensor written in javascript that can be used if you have node.js installed, this will send a randomised temperature reading every five seconds.

```javascript
function getRand(min, max, dp) {
  const factor = Math.pow(10, dp);
  const random = Math.random() * (max - min) + min;
  return Math.round(random * factor) / factor;
}

function sendUpdate() {
  const data = {
    name: "sensor1",
    value: `${getRand(22.01, 23.01, 2)}`,
    time: new Date().toLocaleTimeString("en-GB", { hour12: false }),
  };

  console.log(`sending: ${JSON.stringify(data)} `);

  fetch("http://localhost:8000/add", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Success:", data);
    })
    .catch((error) => {
      console.error("Error:", error);
    });
}

// Send update every 5 seconds
setInterval(sendUpdate, 5000);

// Send first update immediately
sendUpdate();
```

---

---

Resources used for this project  
https://www.tutorialspoint.com/fastapi/fastapi_introduction.htm  
https://www.tutorialspoint.com/sqlite/sqlite_python.htm

Other resources explored  
https://code.visualstudio.com/docs/python/tutorial-fastapi  
https://supabase.com/docs/reference/python/introduction  
https://neon.com/docs/guides/python
