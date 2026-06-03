from datetime import datetime
from quart import Quart, render_template, send_file
from uvicorn import run
from src.settings import nav_list
from src.dao import get_recently_data, DistTable_1, DistTable_2, DistTable_3, DistTable_4
from src.utils import init_db_pool, close_db_pool


app = Quart(__name__)


@app.after_request
async def add_no_cache_headers(response):
    """禁止浏览器缓存，确保每次请求都获取最新数据。"""
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

# 水位表映射
TABLE_MAP = {
    1: DistTable_1,
    2: DistTable_2,
    3: DistTable_3,
    4: DistTable_4,
}


@app.before_serving
async def startup():
    """应用启动时初始化数据库连接池。"""
    await init_db_pool()


@app.after_serving
async def shutdown():
    """应用关闭时释放数据库连接池。"""
    await close_db_pool()


@app.route('/', methods=['GET'])
async def index():
    r_list = await get_recently_data()
    return await render_template('home.html', r=r_list, nav=nav_list)


@app.route('/plan', methods=['GET'])
async def plan():
    return await render_template('plan.html', nav=nav_list)


@app.route('/history', methods=['GET'])
async def history():
    return await render_template('history.html', nav=nav_list)


@app.get('/table/<int:table_id>')
async def get_table(table_id: int):
    table_cls = TABLE_MAP.get(table_id)
    if table_cls is None:
        return "水位表不存在", 404

    now: datetime = datetime.now()
    dist = table_cls()
    await dist.dist()
    dist_path: str = dist.path.dist
    return await send_file(
        dist_path,
        as_attachment=True,
        attachment_filename=f"{now.strftime('%Y年%m月%d日-水位表')}.xlsx",
    )


if __name__ == '__main__':
    run(app="main:app", host="0.0.0.0", port=80)
