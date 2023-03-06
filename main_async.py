import asyncio
import json
import logging
import time

import aiohttp
import pandas as pd
import requests
from jsonmerge import Merger


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d',
    level=logging.INFO,
    filemode="a"
)
logger = logging.getLogger(__file__)


schema = {
    "properties": {
        "results": {
            "mergeStrategy": "append"
        }
    }
}

merger = Merger(schema)
result = {}

columns = [
    "agency",
    "basepay",
    "benefits",
    "employeename",
    "id",
    "jobtitle",
    "notes",
    "otherpay",
    "overtimepay",
    "status",
    "totalpay",
    "totalpaybenefits",
    "year"
]


def paging_stats(url):
    res = requests.get(url)
    data_json = json.loads(res.content)
    total_count = data_json['pagination']['count']
    pages = data_json['pagination']['pages']

    return total_count, pages


async def save_data(data):
    global result
    result = merger.merge(result, data)


async def scrape(url):
    async with aiohttp.ClientSession(trust_env=True) as session:
        async with session.get(url) as res:
            try:
                body = await res.read()
                body = body.decode('utf-8')
                data_json = json.loads(body)
                await save_data(data_json)

            except Exception as e:
                logger.error(e)


async def main(urls):
    tasks = []
    for url in urls:
        task = asyncio.create_task(scrape(url))
        tasks.append(task)

    await asyncio.gather(*tasks)
    df = pd.json_normalize(result, record_path=['results'])
    df.to_csv(f'output_async.csv', index=False, encoding='utf-8-sig')


if __name__ == '__main__':
    # Inicio del proceso
    start = time.time()

    # Obtenemos información de cuántas páginas tiene el conjunto de datos de la API
    per_page = 100
    base_url = "http://localhost:1337/salaries"
    first_req_url = f"{base_url}?per-page={per_page}"
    total_count, pages = paging_stats(first_req_url)

    # Generamos una lista con todas las URL a la que debemos hacer peticiones
    urls = [
        f'{base_url}?page={i}&per-page={per_page}' for i in range(1, pages + 1)]

    # Definimos una función asíncrona que irá ejecutando los request y al
    # final unirá todos los datos en un solo dataframe
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(urls))

    # Fin del proceso
    end = time.time()
    seconds = end - start
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    logger.info("Execution time: %d:%02d:%02d" % (hours, minutes, seconds))
