#!/usr/bin/env python3

import asyncio
import re
import sys
from typing import IO
import urllib.error
import urllib.parse
import timeit
import aiofiles
import aiohttp
from aiohttp import ClientSession
from sys import exit
import pathlib


added = set()

HREF_RE = re.compile(r'href="(.*?)"')

async def fetch_html(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    html = await resp.text()
    return html

async def parse(url: str, session: ClientSession, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""
    found = set()

    try:
        html = await fetch_html(url=url, session=session, **kwargs)
    except (
        aiohttp.ClientError,
        aiohttp.http_exceptions.HttpProcessingError,
    ) as e:
       
        return found
    except Exception as e:
        print("timeout")
        return found
    else:
        for link in HREF_RE.findall(html):
            added.add(str(url+"/"+link))
            try:
                abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError):
                pass
            else:
                found.add(abslink)

        return found

async def write_one(file: IO, url: str, **kwargs) -> None:
    """Write the found HREFs from `url` to `file`."""
    res = await parse(url=url, **kwargs)
    if not res:
        return None
    async with aiofiles.open(file, "a") as f:
        for p in res:
            await f.write(f"{url}\t{p}\n")

async def bulk_crawl_and_write(file: IO, urls: set, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    timeout = aiohttp.ClientTimeout(total=3)
    print(type(urls))
    print("round 2", urls)
    async with ClientSession(timeout=timeout) as session:
        tasks = []
        for url in urls:
            tasks.append(
                write_one(file=file, url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)
def fil_async(urls):
    here = pathlib.Path(__file__).parent
    
    #with open(here.joinpath("urls.txt")) as infile:
     #   urls = set(map(str.strip, infile))
        
    outpath = here.joinpath("foundurls.txt")
    with open(outpath, "w") as outfile:
        outfile.write("source_url\tparsed_url\n")
    print(urls)
    
    asyncio.run(bulk_crawl_and_write(file=outpath, urls=urls))
    print("$$$$$$$$$")
    print(added)

    #asyncio.run(bulk_crawl_and_write(file=outpath, urls=added))

    print("Finshed")
def test():
    print("doffffffffffffffffne")
