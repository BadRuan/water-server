import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
from core.service import get_table1, get_table2, get_table3, get_table4


app = FastAPI()
download_name: str = "%Y年%m月%d日_鸠江区三线水位测站记录表"


@app.get("/api/table1")
async def table1():
    file_path = await get_table1()
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime(download_name)}.xlsx""",
    )


@app.get("/api/table2")
async def table1():
    file_path = await get_table2()
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime(download_name)}.xlsx""",
    )


@app.get("/api/table3")
async def table3():
    file_path = await get_table3()
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime(download_name)}.xlsx""",
    )


@app.get("/api/table4")
async def table4():
    file_path = await get_table4()
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime(download_name)}.xlsx""",
    )

app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8080)
