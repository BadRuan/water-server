import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from core.service import get_waterlevel_1, get_waterlevel_2
from core.util import filePath, save_xlsx1, save_xlsx2
from datetime import datetime

app = FastAPI()


@app.get("/api/table1")
async def table1():
    stations = await get_waterlevel_1()
    filepath = filePath("table1", "dist1")

    await save_xlsx1(filepath[0], filepath[1], stations)
    return FileResponse(
        filepath[1],
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime("%Y年%m月%d日_鸠江区三线水位测站记录表")}.xlsx""",
    )


@app.get("/api/table2")
async def table2():
    stations = await get_waterlevel_2()
    filepath = filePath("table2", "dist2")

    await save_xlsx2(filepath[0], filepath[1], stations)
    return FileResponse(
        filepath[1],
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime("%Y年%m月%d日%H时_鸠江区三线水位测站记录表")}.xlsx""",
    )


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=80)
