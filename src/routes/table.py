from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from service.table_service import TableService, Table1_Service, Table2_Service
from service.api_service import ApiService


table_router = APIRouter(tags=["tables"])

download_name: str = f"%Y年%m月%d日_鸠江区三线水位测站记录表"


@table_router.get("/1")
async def table1(request: Request):
    service: TableService = Table1_Service()
    file_path = service.dist_table()
    api = ApiService()
    ip_address: str = request.client.host
    api.add_download(ip_address)
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime(download_name)}.xlsx""",
    )


@table_router.get("/2")
async def table2(request: Request):
    service: TableService = Table2_Service()
    file_path = service.dist_table()
    api = ApiService()
    ip_address: str = request.client.host
    api.add_download(ip_address)
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime(download_name)}.xlsx""",
    )
