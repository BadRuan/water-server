from asyncio import run
from core.service import TableService, Table4_Service


async def main():
    service: TableService = Table4_Service()
    s:str = await service.get_table()
    print(s)


if __name__ == "__main__":
    run(main())
