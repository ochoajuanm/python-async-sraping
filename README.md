# Proyecto Python Async Scraping

[](https://www.python.org/)
[](https://www.docker.com/)
[](https://flask.palletsprojects.com/en/2.0.x/)
[](https://ubuntu.com/)

Este es un proyecto de scraping asíncrono en Python utilizando asyncio y aiohttp. El objetivo es extraer datos de múltiples sitios web de manera eficiente utilizando programación asíncrona.

## Tecnologías Utilizadas

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/Docker-20.10%2B-blue.svg)](https://www.docker.com/)
[![Flask](https://img.shields.io/badge/Flask-1.1%2B-blue.svg)](https://palletsprojects.com/p/flask/)
[![Linux](https://img.shields.io/badge/Linux-Ubuntu-red.svg)](https://ubuntu.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13%2B-blue.svg)](https://www.postgresql.org/)


## Librerías Utilizadas

- [asyncio](https://docs.python.org/3/library/asyncio.html)
- [aiohttp](https://docs.aiohttp.org/en/stable/)
- [pandas](https://pandas.pydata.org/)
- [jsonmerge](https://jsonmerge.readthedocs.io/en/latest/)
- [requests](https://docs.python-requests.org/en/latest/)
- [json](https://docs.python.org/3/library/json.html)

## Cómo ejecutar el Proyecto

1. Desplegar el entorno:
```bash
docker-compose up -d
```

2. Activar el entorno virtual con el comando:
```bash
source .venv/bin/activate
```
3. Ejecutar el módulo `main_sync.py` para el scraping síncrono:
```bash
python3 main_sync.py
```
4. Ejecutar el módulo `main_async.py` para el scraping asíncrono:
```bash
python3 main_async.py
```
