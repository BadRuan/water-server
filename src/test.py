from asyncio import run
from util.pathtool import filePath
from core.dao import StableCount
from core.service import get_table3


async def test_table():
    f = filePath('table3', 'dist3')
    s = await get_table3(f)
    print(s)

async def test_table_count():
    s_obj = StableCount()
    for i in s_obj.all_station_count():
        print(i)


async def main():
    await test_table_count()


if __name__ == "__main__":
    print("----测试开始----")
    run(main())
    print("----测试结束----")
