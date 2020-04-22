import aiohttp
import asyncio
import async_timeout
import os

async def download_coroutine(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            filename = os.path.basename(url)
            with open(filename, 'wb') as f_handle:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f_handle.write(chunk)
            return await response.release()
async def download_main(urls):
    async with aiohttp.ClientSession() as session:
        for url in urls:
            try:
                await download_coroutine(session, url)
            except:
                pass
if __name__ == '__main__':
    urls = []
    with open("../php.txt", "r") as d:
        for line in d:
            urls.append(line)
    asyncio.run(download_main(urls))