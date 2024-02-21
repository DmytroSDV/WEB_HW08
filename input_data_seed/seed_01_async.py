import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from customs.custom_logger import my_logger
from customs.custom_timer import sync_time, async_time

from conn_modd.models import Author, Quote
import conn_modd.connect

import json
import asyncio
from aiopath import AsyncPath
from  aiofile import async_open

async def data_from_file(filename: str) -> dict: 

    apath_to_file = AsyncPath(os.path.join(os.path.dirname(os.path.abspath(__file__)), filename))
    await asyncio.sleep(0.1)
    try:
        async with async_open(apath_to_file, 'r', encoding='utf-8') as fh:
            content = await fh.read()
            res = json.loads(content)
            return res
    except FileNotFoundError as ex:
        my_logger.log(f"File does not exist - {ex} !", 40)

async def upload_authors():

    try:
        await asyncio.sleep(0.1)
        authors = await data_from_file("authors.json")
        for el in authors:
            Author(fullname=el.get('fullname'), born_date=el.get('born_date'),
                born_location=el.get('born_location'), description=el.get('description')).save()
    except Exception as ex:
        my_logger.log(ex, 40)

async def upload_quotes():
    
    try:
        await asyncio.sleep(0.1)
        quotes = await data_from_file('quotes.json')
        for el in quotes:
            author, *_ = Author.objects(fullname=el.get('author'))
            Quote(quote=el.get('quote'), tags=el.get('tags'), author=author).save()
    except Exception as ex:
        my_logger.log(ex, 40)

@async_time
async def main():
    
    try:  
        await upload_authors()
        await upload_quotes()
    except Exception as ex:
        my_logger.log(ex, 40)

if __name__ == "__main__":
    asyncio.run(main())
