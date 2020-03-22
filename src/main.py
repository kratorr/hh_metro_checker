from aiohttp import web, ClientSession
import aiohttp
import asyncio
import json


API_URL = 'https://api.hh.ru/metro/1'


def get_stations_set(api_stations):
    stations = set()
    for line in api_stations['lines']:
        for station in line['stations']:
            stations.add(station['name'])
    return stations


def verificate_stations(input_stations,api_stations):
    result = {	
        'unchanged': [],
        'update': [],
        'deleted': list(api_stations.difference(input_stations))
    }

    for station in input_stations:
        if station in api_stations:
            result['unchanged'].append(station)
        else:
            result['update'].append(station)
    return result


async def get_api_stations():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(API_URL) as resp:
                response = await resp.json()
        return response
    except aiohttp.ClientError:
        raise web.HTTPNotFound(text='api metro error')


async def api(request):
    data_bytes = await request.read()
    try:
        input_stations = set(json.loads(data_bytes.decode('utf-8')))
    except json.decoder.JSONDecodeError as e:
        raise web.HTTPNotFound(text=str(e))
    api_data = await get_api_stations()
    api_stations = get_stations_set(api_data)
    result = verificate_stations(input_stations, api_stations)
    return web.json_response(result)


if __name__ == '__main__':
    app = web.Application() 
    app.router.add_post('/api/v1/metro/verificate', api)
    web.run_app(app, host='localhost', port=8000)