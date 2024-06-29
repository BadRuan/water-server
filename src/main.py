import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from core.service import filePath, get_waterlevel_mode1, save_xlsx
from datetime import datetime

app = FastAPI()


@app.get("/api/table1")
async def table():
    stations = await get_waterlevel_mode1()
    filepath = filePath("table1", "dist1")
    talbe_loc = [
        "D5:D14",
        "E5:E14",
        "F5:F14",
        "G5:G14",
    ]
    await save_xlsx(filepath[0], filepath[1], talbe_loc, stations)
    return FileResponse(
        filepath[1],
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime("%Y年%m月%d日_鸠江区三线水位测站记录表")}.xlsx""",
    )


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8080)
