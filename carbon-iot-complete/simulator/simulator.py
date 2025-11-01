import asyncio
import aiohttp
import os
import random
import time

API = os.getenv('SIM_API', 'http://api:8000')
TOKEN = os.getenv('SIM_TOKEN', '')

HEADERS = {'Content-Type': 'application/json'}
if TOKEN:
    HEADERS['Authorization'] = f'Bearer {TOKEN}'

async def register(session, i):
    payload = {'name': f'sim-sensor-{i}', 'type': random.choice(['temp','humidity','motion']), 'location': 'sim-lab'}
    async with session.post(f'{API}/devices/register_bulk', json=[payload], headers=HEADERS) as resp:
        text = await resp.text()
        print('register', resp.status, text)

async def run(n=10, concurrency=5):
    async with aiohttp.ClientSession() as s:
        sem = asyncio.Semaphore(concurrency)
        async def worker(i):
            async with sem:
                await register(s, i)
        tasks = [worker(i) for i in range(n)]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    n = int(os.getenv('SIM_COUNT','20'))
    c = int(os.getenv('SIM_CONCURRENCY','10'))
    asyncio.run(run(n,c))
