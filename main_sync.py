import json
import logging
import time

import pandas as pd
import requests

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    datefmt='%Y-%m-%d',
    level=logging.INFO,
    filemode="a"
)
logger = logging.getLogger(__file__)

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


def get_data(url):
    try:
        res = requests.get(url)
        data_json = json.loads(res.content)
        data_parsed = pd.json_normalize(data_json, record_path=['results'])

        return data_parsed
    except Exception as e:
        logger.error(e)


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

    # Definimos un DataFrame vacío que iremos poblando sincrónicamente a
    # medida que se obtengan los datos de cada request
    df = pd.DataFrame(columns=columns)
    for url in urls:
        tmp_df = get_data(url)
        df = pd.concat([df, tmp_df], axis=0)

    # Exportamos el resultado obtenido
    df.to_csv('output_sync.csv', index=False, encoding='utf-8-sig')

    # Fin del proceso
    end = time.time()
    seconds = end - start
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)

    logger.info("Execution time: %d:%02d:%02d" % (hours, minutes, seconds))
