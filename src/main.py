import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
from core.service import TableService, Table3_Service


app = FastAPI()
download_name: str = "%Y年%m月%d日_鸠江区三线水位测站记录表"


@app.get("/source/table3")
async def table3():
    service: TableService = Table3_Service()
    file_path = await service.get_table()
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime(download_name)}.xlsx""",
    )


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8080)
