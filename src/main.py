import uvicorn
from fastapi import FastAPI
from dao.waterlevel import select_cruuent_waterlevel, select_threeline_waterlevel


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "hello"}


@app.get("/current")
async def current():
    return await select_cruuent_waterlevel()


@app.get("/threeline")
async def threeline():
    return await select_threeline_waterlevel()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="127.0.0.1")
