import asyncio
from aiohttp import ClientSession


async def get_posts():
    async with ClientSession() as session:
        async with session.get("http://127.0.0.1:8080/posts") as resp:
            return await resp.json()

async def get_post(post_id):
    async with ClientSession() as session:
        async with session.get(f"http://127.0.0.1:8080/post/{post_id}") as resp:
            return await resp.json()

async def post_posts():
    async with ClientSession() as session:
        async with session.post(f"http://127.0.0.1:8080/post", json={
            "title": "test post",
            "text": "test text",
            "user_id": 1
        }) as resp:
            return await resp.json()

async def delete_post(post_id):
    async with ClientSession() as session:
        async with session.delete(f"http://127.0.0.1:8080/post/{post_id}") as resp:
            return await resp.json()



async def main():
    response1 = await get_posts()
    print(response1)
    response2 = await get_post(8)
    print(response2)
    response3 = await post_posts()
    print(response3)
    response4 = await delete_post(10)
    print(response4)

asyncio.run(main())