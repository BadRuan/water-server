from fastapi import APIRouter, Request


table_router = APIRouter(tags=["tables"])

download_name: str = f"%Y年%m月%d日_鸠江区三线水位测站记录表"
