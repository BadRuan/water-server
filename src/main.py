import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from routes.table import table_router
from routes.api import api_router
from service.api_service import ApiService


app = FastAPI()


# 跨域配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def handle_static_files(request: Request, call_next):
    api = ApiService()
    ip_address: str = request.client.host
    api.add_visit(ip_address)

    response = await call_next(request)
    return response


# 挂载路由
app.include_router(table_router, prefix="/table", tags=["tables"])
app.include_router(api_router, prefix="/api", tags=["apis"])

app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8080)
