import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from datetime import datetime
from schemas.response import SuccessResponse
from exceptions.api_exception import NotFoundException
from service.table_service import TableService, Table1_Service, Table2_Service
from service.api_service import ApiService


app = FastAPI()
download_name: str = "%Y年%m月%d日_鸠江区三线水位测站记录表"

# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/table/1")
async def table1():
    service: TableService = Table1_Service()
    file_path = service.dist_table()
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime(download_name)}.xlsx""",
    )


@app.get("/table/2")
async def table2():
    service: TableService = Table2_Service()
    file_path = service.dist_table()
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime(download_name)}.xlsx""",
    )


@app.get("/water", response_model=SuccessResponse, status_code=200)
async def get_water_count():
    try:
        service = ApiService()
        return SuccessResponse(data=service.getCountInfo())
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.json())


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8080)
