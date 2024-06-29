from asyncio import run
from core.service import get_waterlevel_mode2
from core.util import filePath, save_xlsx2


async def main():
    stations = await get_waterlevel_mode2()
    filepath = filePath("table2", "dist2")

    await save_xlsx2(filepath[0], filepath[1], stations)


if __name__ == "__main__":
    print("----测试开始----")
    run(main())
    print("----测试结束----")
