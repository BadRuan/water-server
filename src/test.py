from asyncio import run
from core.service import generate_time_description



async def test_table():
    s = generate_time_description(1)
    print(s)


async def main():
    await test_table()


if __name__ == "__main__":
    print("----测试开始----")
    run(main())
    print("----测试结束----")
