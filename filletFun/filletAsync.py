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
import async_timeout
import os
from .filletClass import filletTarget


added = []
all_targets = []
HREF_RE = re.compile(r'href="(.*?)"')

async def download_coroutine(session, url):
    basedir = url[0]
    url = url[1]
    print(url)
    filename = os.path.basename(url)
    fPath = str(basedir)+'/'+str(filename)
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            with open(fPath, 'a+') as f_handle:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f_handle.write(chunk)
            return await response.release()

async def download_main(urls):
    #this will downlaod all files from desired file paths
    #still need to add functionality for it group downloads to index url
    async with aiohttp.ClientSession() as session:
        for url in urls:

            await download_coroutine(session, url)



async def fetch_html(test, url: str, session: ClientSession,*args, **kwargs) -> str:
    """GET request wrapper to fetch page HTML.

    kwargs are passed to `session.request()`.
    """
    resp = await session.request(method="GET", url=url, **kwargs)
    if resp.raise_for_status():
        del(test)
    else:
        all_targets.append(test)
    html = await resp.text()
    return html

async def parse(test, url: str, session: ClientSession,*args, **kwargs) -> set:
    """Find HREFs in the HTML of `url`."""
    found = set()

    try:
        html = await fetch_html(test=test, url=url, session=session, **kwargs)
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
            link = str(url+"/"+link)

            try:
                abslink = urllib.parse.urljoin(url, link)
            except (urllib.error.URLError, ValueError):
                pass
            else:
                if abslink not in found and not abslink.endswith("css"):
                    found.add(abslink)
                  
                    pass                

        return found

async def write_one(test, file: IO, url: str, *args, **kwargs) -> None:
    
    res = await parse(test=test, url=url, **kwargs)
    if not res:
        return None
    
    async with aiofiles.open(file, "a") as f:
        for p in res:
            if p.endswith("php"):
                added.append([url, p])
                test.downloads.append(p)
            await f.write(f"{p}\n")
async def bulk_crawl_and_write(file: IO, urls: set, config:str, **kwargs) -> None:
    """Crawl & write concurrently to `file` for multiple `urls`."""
    timeout = aiohttp.ClientTimeout(total=3)
    async with ClientSession(timeout=timeout) as session:
        tasks = []
        for url in urls:
            target = filletTarget()
            target.url = url
            #very sloopy but was having circular importing errors so 
            #im calling a function isn't yet defined and throws an error when called:

            from .filletFun1 import fil_urlConstruct

            fil_urlConstruct(target, config)
            tasks.append(
                write_one(test=target, file=file, url=url, session=session,**kwargs)

            )
        await asyncio.gather(*tasks)



def fil_async(urls, test):
    here = pathlib.Path(__file__).parent

   
    outpath = here.joinpath("foundurls.txt")

    asyncio.run(bulk_crawl_and_write(file=outpath, urls=urls, config=test))
    print("Found {}  Possible Targets".format(len(all_targets)))
    for x in all_targets:
        x.show()

    

    #print("Starting Downlaods")
    
    #asyncio.run(download_main(added))
    print("Finshed")

