# 鸠江防汛水位小助手

鸠江区防汛水位数据查询与报表生成工具。直连安徽水信息网站数据库，一键获取指定时间的水位表，自动标注设防、警戒、保证三线水位。

## 功能简介

- **首页水位概览**：实时展示各测站最新水位及涨落情况
- **一键生成报表**：点击即可下载 Excel 格式水位表，自动填充数据并按三线水位着色
- **多种报表模板**：支持 4 种不同维度的水位对比表（今日/昨日/上周/去年同期等）

## 技术栈

| 层级 | 技术 |
|------|------|
| Web 框架 | [Quart](https://quart.palletsprojects.com/)（异步 Flask） |
| ASGI 服务器 | Uvicorn |
| 数据库 | PostgreSQL（asyncpg 异步驱动） |
| Excel 处理 | openpyxl |
| 配置管理 | pydantic-settings |
| 前端样式 | Tailwind CSS |
| Python 版本 | >= 3.12 |

## 项目结构

```
water-server/
├── main.py                 # 应用入口、路由定义
├── src/
│   ├── settings.py         # 配置项、站点列表、三线水位定义
│   ├── model.py            # 数据模型（Station、WaterItem）
│   ├── dao/
│   │   ├── table.py        # Excel 水位表生成（DistTable_1~4）
│   │   └── recently.py     # 首页最新水位查询
│   ├── utils/
│   │   ├── storage.py      # 数据库连接池、查询封装
│   │   └── logger.py       # 日志配置（控制台 + 文件轮转）
│   └── routes/
├── templates/              # Jinja2 页面模板
│   ├── base.html           # 基础布局
│   ├── home.html           # 首页
│   ├── plan.html           # 未来计划
│   └── history.html        # 开发历程
├── static/                 # 静态资源（CSS、图标、图片）
├── file/                   # Excel 报表模板（table1~4.xlsx）
├── dist/                   # 生成的报表输出目录
├── logs/                   # 运行日志（按天轮转，保留 7 天）
├── test/                   # 测试用例
├── requirements.txt        # Python 依赖
├── pyproject.toml          # 项目元数据（uv 管理）
├── Dockerfile              # Docker 构建文件
└── .env                    # 环境变量（数据库连接等）
```

## 快速开始

### 1. 环境准备

```bash
# 克隆项目
git clone <repo-url>
cd water-server

# 创建虚拟环境（推荐使用 uv）
uv venv
source .venv/bin/activate

# 安装依赖
uv pip install -r requirements.txt
```

### 2. 配置环境变量

复制并编辑 `.env` 文件：

```env
DATABASE_URL=postgresql://user:password@host:port/dbname
TIMEZONE=Asia/Shanghai
```

### 3. 数据库建表

参考以下 SQL 在 PostgreSQL 中创建站点表：

```sql
-- 站点基表
CREATE TABLE IF NOT EXISTS station (
    ts    TIMESTAMP PRIMARY KEY UNIQUE NOT NULL WITHOUT TIME ZONE,
    height NUMERIC(5, 2) NOT NULL
);

-- 各测站子表（继承基表结构）
CREATE TABLE IF NOT EXISTS station_60115400 (LIKE station INCLUDING ALL);
CREATE TABLE IF NOT EXISTS station_62904400 (LIKE station INCLUDING ALL);
CREATE TABLE IF NOT EXISTS station_62904500 (LIKE station INCLUDING ALL);
CREATE TABLE IF NOT EXISTS station_62900700 (LIKE station INCLUDING ALL);
CREATE TABLE IF NOT EXISTS station_62900600 (LIKE station INCLUDING ALL);
CREATE TABLE IF NOT EXISTS station_62906500 (LIKE station INCLUDING ALL);
CREATE TABLE IF NOT EXISTS station_62905100 (LIKE station INCLUDING ALL);
```

### 4. 启动服务

```bash
python main.py
```

服务默认监听 `0.0.0.0:80`，访问 `http://localhost` 即可使用。

### 5. Docker 部署

```bash
docker build -t water-server .
docker run -d -p 80:80 --env-file .env water-server
```

## 路由说明

| 路径 | 方法 | 说明 |
|------|------|------|
| `/` | GET | 首页，展示各测站最新水位及涨落 |
| `/plan` | GET | 未来计划页面 |
| `/history` | GET | 开发历程页面 |
| `/table/1` | GET | 下载水位表 1（今日/昨日/上周/去年同期 8 时） |
| `/table/2` | GET | 下载水位表 2（当前/4小时前/8小时前） |
| `/table/3` | GET | 下载水位表 3（今日/3日前/去年同期 8 时） |
| `/table/4` | GET | 下载水位表 4（今日/昨日/去年同期 8 时） |

## 测站列表

| 站点编码 | 测站名称 | 所属堤段 |
|----------|----------|----------|
| 60115400 | 弋矶山 | 城北圩 |
| 62904400 | 凤凰颈新站闸上 | — |
| 62904500 | 凤凰颈新站闸下 | 无为大堤 / 惠生连圩堤 / 永定大圩堤 / 黑沙洲天然洲圩 |
| 62900700 | 裕溪闸下 | 江北（沈巷）长江堤 / 裕溪口江堤 |
| 62900600 | 裕溪闸上 | 裕溪河堤 |
| 62906500 | 清水 | 万春圈堤 |
| 62905100 | 新桥闸上 | 牛屯河堤 |

## 运行测试

```bash
pytest test/ -v
```

## 联系方式

- 邮箱：ruanfm@qq.com
- QQ：645187410

Copyright © 2024-2026 鸠江水位小助手 | 阮福民 版权所有
