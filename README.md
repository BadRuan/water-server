# 鸠江防汛水位小助手 后端部分

Python + Flask + PostgreSQL
  
## 功能简介

> 一键获取指定时间水位表；

## 相关数据库SQL备忘

```sql
--- 建表语句
create table if not exists station (
 ts timestamp  primary key unique not null without time zone ,
 height numeric(5, 2) not null
);

create table if not exists station_60115400 (
 like station including all
) inherits (station);
create table if not exists station_62904400 (
 like station including all
) inherits (station);
create table if not exists station_62904500 (
 like station including all
) inherits (station);
create table if not exists station_62900700 (
 like station including all
) inherits (station);
create table if not exists station_62900600 (
 like station including all
) inherits (station);
create table if not exists station_62906500 (
 like station including all
) inherits (station);
create table if not exists station_62905100 (
 like station including all
) inherits (station);

insert into station_60115400 (ts, height) 
values 
('2023-01-01 08:00:00', 3.44);

insert into station_60115400 (ts, height) 
values 
('2023-01-01 08:10:00', 3.43);

select count(*) from station_60115400;
select count(*) from station_62900600;
select count(*) from station;

select (height) 
from station_60115400 
where ts='2023-01-01 08:10:00.000';

select *
from station_62904400  
where ts between '2026-03-01 00:00:00' and '2026-03-31 23:59:59';


--    (60115400,"芜湖"),
--    (62904400,"凤凰颈新站闸上"),
--    (62904500,"凤凰颈新站闸下"),
--    (62900700,"裕溪闸下"),
--    (62900600,"裕溪闸上"),
--    (62906500,"清水"),
--    (62905100,"新桥闸上")

select ts, height
from station_62900600
ORDER BY ts desc  LIMIT 1;

select *  from station_60115400 where ts = (SELECT MAX(ts) FROM station_60115400);

CREATE USER liyan WITH PASSWORD 'Zb4$28_YnjHCO?';

GRANT CONNECT ON DATABASE water TO liyan;

GRANT SELECT ON ALL TABLES IN SCHEMA public TO liyan;

GRANT USAGE ON SCHEMA public TO liyan;
```
