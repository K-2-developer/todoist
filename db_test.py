import asyncio
from src.Boards_service.Infrastructure.Database.database import engine
from sqlalchemy import text


async def test_connection():
    try:
        async with engine.begin() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("DB OK:", result.scalar())
    except Exception as e:
        print("DB ERROR:", e)

asyncio.run(test_connection())
