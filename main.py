from datetime import datetime
from quart import Quart, render_template, send_file
from uvicorn import run
from src.settings import nav_list
from src.dao import get_recently_data, DistTable_1, DistTable_2, DistTable_3, DistTable_4


app = Quart(__name__)


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

@app.get('/table/1')
async def get_table_1():
    dist = DistTable_1()
    await dist.dist()
    dist_path: str = dist.path.dist
    return await send_file(dist_path,as_attachment=True, attachment_filename=f'{datetime.now().strftime('%Y年%m月%d日-水位表')}.xlsx')

@app.get('/table/2')
async def get_table_2():
    dist = DistTable_2()
    await dist.dist()
    dist_path: str = dist.path.dist
    return await send_file(dist_path,as_attachment=True, attachment_filename=f'{datetime.now().strftime('%Y年%m月%d日-水位表')}.xlsx')


@app.get('/table/3')
async def get_table_3():
    dist = DistTable_3()
    await dist.dist()
    dist_path: str = dist.path.dist
    return await send_file(dist_path,as_attachment=True, attachment_filename=f'{datetime.now().strftime('%Y年%m月%d日-水位表')}.xlsx')


@app.get('/table/4')
async def get_table_4():
    dist = DistTable_4()
    await dist.dist()
    dist_path: str = dist.path.dist
    return await send_file(dist_path,as_attachment=True, attachment_filename=f'{datetime.now().strftime('%Y年%m月%d日-水位表')}.xlsx')

if __name__ == '__main__':
    run(app="main:app", host="0.0.0.0", port=80)
    # app.run(debug=True, host='0.0.0.0', port=50231)