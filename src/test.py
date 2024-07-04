from asyncio import run
from util.pathtool import filePath
from core.service import get_table4



async def test_table():
    f = filePath('table3', 'dist4')
    s = await get_table4(f)
    print(s)


async def main():
    await test_table()


if __name__ == "__main__":
    print("----测试开始----")
    run(main())
    print("----测试结束----")
