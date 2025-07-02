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

        $ python --version
        Python 3.12.3

If you get the following:

        zsh: command not found python

Google installing python for your system, before continuing.

1.  Create a directory to hold your python server and cd into it

        $ mkdir server
        $ cd server

2.  Create a python environment, This will create and environment where any packages you install will be kept local to this project. the .venv is a hidden directory, note it can be given any other name.

        $ python -m venv .venv

3.  You need to activate the environment before you can use it, note the command line prompt will change to show it is active. (you can type 'deactivate' to leave the environment later.)

        Linux $ source .venv/bin/activate

        Windows CMD $  .venv\Scripts\activate.bat

        PowerShell  $   .venv\Scripts\activate.ps1

4.  Now you are in the environment you can use pip to install packages ...

        $ pip install fastapi uvicorn

5.  build a simple test server, use a text editor to create a file server.py containing the following:

        from fastapi import FastAPI

        app = FastAPI()

        @app.get("/")
        def root():
                return {"message": "Hello World"}

6.  run the server using uvicorn

        $ uvicorn server:app --host 0.0.0.0 --port 8000

Now visit localhost:8000 to see the server is working.

fastAPI has a neat trick, it documents its routes and provides interactive access for testing in the browser, if you visit localhost:8000/docs, later when you add post routes you will be able to test them using the docs.

Below we have a post route to accept sensor name, temperature value and time, these are all defined as string to allow flexibility in the format so '33C', '33' and '33 centigrade' can all be used and the date can be in any short or long form format.

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

---

#### Writing to the database

TBD note to self: test sensor code created and tested, just this to write up

---

---

https://supabase.com/docs/reference/python/introduction  
https://code.visualstudio.com/docs/python/tutorial-fastapi  
https://www.tutorialspoint.com/sqlite/sqlite_python.htm
