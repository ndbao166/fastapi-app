import uvicorn
from fastapi import FastAPI

from settings import settings

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


if __name__ == "__main__":
    uvicorn.run(app, host=settings.APP_HOST, port=settings.APP_PORT)
