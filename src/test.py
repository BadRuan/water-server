from asyncio import run
from core.service import get_table2



async def test_table():
    s = await get_table2()
    print(s)


async def main():
    await test_table()


if __name__ == "__main__":
    print("----测试开始----")
    run(main())
    print("----测试结束----")
