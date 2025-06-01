from fastapi import APIRouter, HTTPException
from src.schemas.response import SuccessResponse
from src.exceptions.api_exception import NotFoundException
from src.service.api_service import ApiService


api_router = APIRouter(tags=["apis"])


@api_router.get("/count", response_model=SuccessResponse, status_code=200)
async def get_water_count():
    try:
        service = ApiService()
        return SuccessResponse(data=service.getCountInfo())
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.json())


@api_router.get("/recently", response_model=SuccessResponse, status_code=200)
async def get_recently():
    try:
        service = ApiService()
        return SuccessResponse(data=service.get_recently())
    except NotFoundException as e:
        raise HTTPException(status_code=404, detail=e.json())
