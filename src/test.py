import asyncio
from dao.waterlevel import select_threeline_waterlevel


async def main():
    result = await select_threeline_waterlevel()
    for i in result:
        print(i)


if __name__ == "__main__":
    asyncio.run(main())
