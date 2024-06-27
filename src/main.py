import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from core.service import get_waterlevel, save_xlsx
from pathlib import Path
from datetime import datetime

app = FastAPI()


@app.get("/api/table")
async def table():
    # 获取当前文件路径
    current_file_path = Path(__file__).resolve()
    # 获取当前文件的所在目录
    current_dir = current_file_path.parent
    file_path = current_dir / "基础表格.xlsx"
    # 基础表格的完整路径
    source_filename = str(file_path)
    save_path = current_dir / "dist.xlsx"
    # 生成表格的完整路径
    dist_filename = str(save_path)
    # 获取水位数据
    stations = await get_waterlevel()
    # 将水位数据填入表格中
    await save_xlsx(source_filename, dist_filename, stations)
    return FileResponse(
        dist_filename,
        media_type="application/octet-stream",
        filename=f"""{datetime.now().strftime("%Y年%m月%d日_鸠江区三线水位测站记录表")}.xlsx""",
    )


app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=80)
