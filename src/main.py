import uvicorn
from fastapi import FastAPI
from dao.waterlevel import select_cruuent_waterlevel


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello"}


@app.get("/data")
async def index():
    return select_cruuent_waterlevel()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1")
