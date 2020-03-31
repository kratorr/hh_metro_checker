import json

from datetime import datetime, timedelta
from functools import wraps

from aiohttp import web, ClientSession



API_URL = 'https://api.hh.ru/metro/1'


def cache(ttl):
    cache_dict = {}
    def decorator(func):
        async def wrapper():
            if 'response' in cache_dict:
                delta = (datetime.now() - cache_dict['response']['time']).total_seconds()
                if delta > ttl:
                    result = await func()
                    cache_dict['response'] = {'data': result , 'time': datetime.now()}
            else:
                result = await func()
                cache_dict['response'] = {'data': result , 'time': datetime.now()}
            return cache_dict['response']['data']
        return wrapper
    return decorator


def get_stations_set(api_stations):
    stations = set()
    for line in api_stations['lines']:
        for station in line['stations']:
            stations.add(station['name'])
    return stations


def verificate_stations(input_stations,api_stations):
    result = {	
        'unchanged': list(input_stations.intersection(api_stations)),
        'update': list(input_stations.difference(api_stations)),
        'deleted': list(api_stations.difference(input_stations))
    }
    return result


@cache(ttl=600)
async def get_api_stations():
    try:
        async with ClientSession() as session:
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