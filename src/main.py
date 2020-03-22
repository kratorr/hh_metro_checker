from aiohttp import web, ClientSession
import aiohttp
import time
import asyncio


API_URL = 'https://api.hh.ru/metro/'

async def get_stations():
    async with aiohttp.ClientSession() as session:
        async with session.get(API_URL) as resp:
            response = await resp.json()
    return response


async def api(request):
    data = await request.post()
    print(data)
    #for i in data[0]:
    #    print(i)
    response = await get_stations()
    return web.json_response(response)

app = web.Application() 

app.router.add_post('/api/v1/metro', api)
app.router.add_get('/api/v1/metro', api) 
web.run_app(app, host='172.30.30.52', port=9999)