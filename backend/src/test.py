import asyncio
from httpx import AsyncClient
from app import app

async def test():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        files = {'gst': ('sample_gst.csv', open('data/sample_gst.csv', 'rb'), 'text/csv')}
        response = await ac.post("/api/analyze", files=files)
        print(response.status_code)
        print(response.json())

if __name__ == "__main__":
    asyncio.run(test())
