from fastapi import FastAPI
from app.routers import test, auth

app = FastAPI()

app.include_router(test.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"status": "success", "message": "Hello world!"}