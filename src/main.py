import uvicorn
from fastapi import FastAPI
from core.dao import select_threeline_waterlevel


app = FastAPI()


@app.get("/")
async def index():
    return {"message": "run success"}


@app.get("/threeline")
async def threeline():
    return await select_threeline_waterlevel()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8080)
