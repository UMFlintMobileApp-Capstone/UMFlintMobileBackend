from fastapi import FastAPI
from app.routers import test

app = FastAPI()

app.include_router(test.router)

@app.get("/")
def read_root():
    return {"status": "success", "message": "Hello world!"}