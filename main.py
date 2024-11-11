from fastapi import FastAPI
from app.routers import test, auth

app = FastAPI()

""" 
<main.py>

The main interface for the backend.
This is where routes are added to the FastAPI application.

You do that by including your route located in app/routers
to the import statement, and then doing below:
    app.include_router(EXAMPLE.router)

If you have a base slug, you can place it here. Though we
typically want to make a route for every feature (so for
instance messaging route, maps route, events route, etc)
for ease of understanding.
"""

app.include_router(test.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"status": "success", "message": "Hello world!"}
    