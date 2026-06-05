import httpx, asyncio, json

async def test():
    async with httpx.AsyncClient(timeout=30) as client:
        query = "SELECT answer FROM mindsdb.articles_model WHERE question = 'test'"
        res = await client.post('http://mindsdb:47334/api/sql/query', json={'query': query})
        print(json.dumps(res.json(), indent=2))

asyncio.run(test())
