from datetime import datetime
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse
from src.service.table_service import (
    TableService,
    Table1_Service,
    Table2_Service,
    Table3_Service,
    Table4_Service,
)
from src.service.api_service import ApiService


table_router = APIRouter(tags=["tables"])

download_name: str = f"%Y年%m月%d日_鸠江区三线水位测站记录表"


def common(request: Request, service: TableService):
    file_path: str = service().dist_table()
    api = ApiService()
    ip_address: str = request.client.host
    api.add_download(ip_address)
    return FileResponse(
        file_path,
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime(download_name)}.xlsx""",
    )


@table_router.get("/1")
async def table1(request: Request):
    return common(request, Table1_Service)


@table_router.get("/2")
async def table2(request: Request):
    return common(request, Table2_Service)


@table_router.get("/3")
async def table3(request: Request):
    return common(request, Table3_Service)


@table_router.get("/4")
async def table4(request: Request):
    return common(request, Table4_Service)
