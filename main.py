from datetime import datetime
from flask import Flask, render_template, send_file
from src.dao import get_recently_data, DistTable_1, DistTable_2, DistTable_3, DistTable_4

app = Flask(__name__)


@app.route('/', methods=['GET'])
def index():
    r_list = get_recently_data()
    return render_template('home.html', r=r_list)

@app.route('/plan', methods=['GET'])
def plan():
    return render_template('plan.html')

@app.route('/history', methods=['GET'])
def history():
    return render_template('history.html')

@app.get('/table/1')
def get_table_1():
    dist = DistTable_1()
    dist.dist()
    dist_path: str = dist.path.dist
    return send_file(dist_path, download_name=f'{datetime.now().strftime('%Y年%m月%d日-水位表')}.xlsx')


@app.get('/table/2')
def get_table_2():
    dist = DistTable_2()
    dist.dist()
    dist_path: str = dist.path.dist
    return send_file(dist_path, download_name=f'{datetime.now().strftime('%Y年%m月%d日-水位表')}.xlsx')


@app.get('/table/3')
def get_table_3():
    dist = DistTable_3()
    dist.dist()
    dist_path: str = dist.path.dist
    return send_file(dist_path, download_name=f'{datetime.now().strftime('%Y年%m月%d日-水位表')}.xlsx')


@app.get('/table/4')
def get_table_4():
    dist = DistTable_4()
    dist.dist()
    dist_path: str = dist.path.dist
    return send_file(dist_path, download_name=f'{datetime.now().strftime('%Y年%m月%d日-水位表')}.xlsx')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5023)