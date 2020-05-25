#https://stackoverflow.com/questions/51250706/combining-semaphore-and-time-limiting-in-python-trio-with-asks-http-request
from typing import List, Iterator

import asks
import trio

asks.init('trio')

links: List[str] = [
    'https://httpbin.org/delay/7',
    'https://httpbin.org/delay/6',
    'https://httpbin.org/delay/4'
] * 3


async def fetch_urls(urls: List[str], number_workers: int, throttle_rate: float):

    async def token_issuer(token_sender: trio.abc.SendChannel, number_tokens: int):
        async with token_sender:
            for _ in range(number_tokens):
                await token_sender.send(None)
                await trio.sleep(1 / throttle_rate)

    async def worker(url_iterator: Iterator, token_receiver: trio.abc.ReceiveChannel):
        async with token_receiver:
            for url in url_iterator:
                await token_receiver.receive()

                print(f'[{round(trio.current_time(), 2)}] Start loading link: {url}')
                response = await asks.get(url)
                # print(f'[{round(trio.current_time(), 2)}] Loaded link: {url}')
                responses.append(response)

    responses = []
    url_iterator = iter(urls)
    token_send_channel, token_receive_channel = trio.open_memory_channel(0)

    async with trio.open_nursery() as nursery:
        async with token_receive_channel:
            nursery.start_soon(token_issuer, token_send_channel.clone(), len(urls))
            for _ in range(number_workers):
                nursery.start_soon(worker, url_iterator, token_receive_channel.clone())

    return responses

responses = trio.run(fetch_urls, links, 5, 1.)
