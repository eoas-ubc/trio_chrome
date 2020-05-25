"""
examples for trio_cdp

read_page -- visit a page and get the title

take_screenshot -- take a screenshot of a page

"""
import functools as ft
import gc
import json
import logging
import os
import socket
import subprocess
import time
from base64 import b64decode

import asks
import trio
from cdp import dom
from cdp import emulation
from cdp import page
from cdp import target
from trio_cdp import open_cdp
from pyppeteer.chromium_downloader import chromium_executable

log_level = os.environ.get("LOG_LEVEL", "info").upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger("try_cdp")
logging.getLogger("trio-websocket").setLevel(logging.WARNING)


async def save_pdf(browserurl, targeturl, pdfpath):
    """
    take a screenshot of a webpage
    originally https://github.com/HyperionGray/trio-chrome-devtools-protocol/blob/master/examples/screenshot.py

    Parameters

    browserurl: str
        ws address for chrome developer protocol commands

    targeturl: str
        url of page to screenshot

    pngfile: str
        filename for png file
    """
    logger.info("Connecting to browser: %s", browserurl)
    async with open_cdp(browserurl) as conn:
        logger.info("Listing targets")
        targets = await conn.execute(target.get_targets())
        target_id = targets[0].target_id

        logger.info("Attaching to target id=%s", target_id)
        async with conn.open_session(target_id) as session:
            logger.info("Setting device emulation")
            await session.execute(
                emulation.set_device_metrics_override(
                    width=1200, height=2000, device_scale_factor=1, mobile=False
                )
            )

            logger.info("Enabling page events")
            await session.execute(page.enable())

            logger.info("Navigating to %s", targeturl)
            async with session.wait_for(page.LoadEventFired):
                await session.execute(page.navigate(url=targeturl))

            time.sleep(1)
            root_node = await session.execute(dom.get_document())
            title_node_id = await session.execute(
                dom.query_selector(root_node.node_id, "body")
            )
            body_html = await session.execute(dom.get_outer_html(title_node_id))

            logger.info(body_html)

            logger.info("Saving a pdf")
            # TODO: capture_screenshot knows how to wait for javascript to finish
            #  rendering, but print_do_pdf doesn't
            # await session.execute(page.capture_screenshot(format="png"))
            pdf_data, _ = await session.execute(page.print_to_pdf())

            pdf_file = await trio.open_file(pdfpath, "wb")
            async with pdf_file:
                await pdf_file.write(b64decode(pdf_data))
            logger.info(f"wrote {pdfpath}")


async def read_page(browserurl, targeturl):
    """
    read a page and get the title
    originally https://github.com/HyperionGray/trio-chrome-devtools-protocol/blob/master/examples/get_title.py
    """
    logger.info("Connecting to browser: %s", browserurl)
    async with open_cdp(browserurl) as conn:
        logger.info("Listing targets")
        targets = await conn.execute(target.get_targets())
        target_id = targets[0].target_id

        logger.info("Attaching to target id=%s", target_id)
        session = await conn.open_session(target_id)

        logger.info("Navigating to %s", targeturl)
        await session.execute(page.enable())
        async with session.wait_for(page.LoadEventFired):
            await session.execute(page.navigate(targeturl))
            key, item = await session.execute(page.print_to_pdf())
            print(f"pdf is: {type(item)}")

        logger.info("Extracting page title")
        root_node = await session.execute(dom.get_document())
        title_node_id = await session.execute(
            dom.query_selector(root_node.node_id, "title")
        )
        html = await session.execute(dom.get_outer_html(title_node_id))
        print(html)


def get_free_port():
    """Get free port."""
    sock = socket.socket()
    sock.bind(("localhost", 0))
    port = sock.getsockname()[1]
    sock.close()
    del sock
    gc.collect()
    return port


async def headless_chrome(receive_channel, chrome_args, options):
    """
    run chrome headless as a background process

    Parameters
    ----------

    receive_channel: FdStream
       channel to listen for terminae signal

    chrome_args: list 
       arguments for headless chrome command

    options: dict
       keyword options for open_process
       
    """
    async with await trio.open_process(chrome_args, **options) as process:
        saveit = []
        async with receive_channel:
            async for value in receive_channel:
                saveit.append(value)
        #
        # after channel is closed by make request
        # go through messages and look for terminate
        #
        for item in saveit:
            if item == "terminate":
                print("received terminate")
                process.terminate()


async def get_addr(url, send_channel):
    """
    wait until headless crhome has started, then
    get the websocket information from the port
    
    Parameters
    ----------

    url: str
       http://localhost:port

    send_channel:  Fdchannel
       channel to send the websocket address back to make_request 

    Returns
    -------

    webSocketDebuggerURL: str
       ws address for chrome developer protocol
    """
    url = url + "/json/version"
    response = None
    while response is None:
        await trio.sleep(0.5)
        print(f"sleeping {url}")
        response = await asks.get(url)
    out = json.loads(response.content.decode())
    async with send_channel:
        await send_channel.send(out["webSocketDebuggerUrl"])


async def make_request(targetlist, send_channel, receive_channel):
    """
    go through targetlist and take png snapshots of pages

    Parameters
    ----------

    targetlist: list of tuples
       (url, pngfile) pairs for snapshots

    send_channel: FdStream
       channel to send terminate messsage to headless_chrome
       when done

    receive_channel: FdStream
       channel to listen to for ws browserurl
    
    """
    async with receive_channel:
        async for value in receive_channel:
            browser_url = value
    print(f"got browser_url = {browser_url}")
    # await read_page(browser_url, targeturl)
    for targeturl, pdfpath in targetlist:
        await save_pdf(browser_url, targeturl, pdfpath)
    async with send_channel:
        print("sending terminate message")
        await send_channel.send("terminate")


async def main(headless, get_addr, make_request):
    """
    run functions in nursery
    """
    async with trio.open_nursery() as nursery:
        #
        # channel pair so get_url can send ws address to make_request
        #
        send_channel, receive_channel = trio.open_memory_channel(0)
        #
        # channel pair so make_request can send shutdown to headless_chrome
        #
        send_channel_1, receive_channel_1 = trio.open_memory_channel(0)
        nursery.start_soon(headless, receive_channel_1)
        nursery.start_soon(get_addr, url, send_channel)
        targetlist = [
            (
                r"file:///Users/phil/repos/paged_trio/testhtml/test_message.html",
                "test_message.pdf",
            ),
            (
                r"file:///Users/phil/repos/paged_trio/testhtml/day5_quiz_students.html",
                "day_5_students.pdf",
            ),
            # (r"https://google.com", "google.png"),
            # (r"https://nytimes.com", "nytimes.png"),
            # (r"https://www.eoas.ubc.ca", "eoas.png"),
            # (r"https://www.washingtonpost.com", "washingtonpost.png"),
            # (r"https://www.latimes.com", "latimes.png"),
            # (r"https://www.amazon.com", "amazon.png"),
        ]
        nursery.start_soon(make_request, targetlist, send_channel_1, receive_channel)
    print(f"through main")


if __name__ == "__main__":
    asks.init("trio")
    the_port = get_free_port()
    print(f"{the_port}")
    the_remote = f"--remote-debugging-port={the_port}"
    CHROME_PATH = str(chromium_executable())
    options = dict(
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    chrome_args = [
        CHROME_PATH,
        "--headless",
        "--disable-gpu",
        the_remote,
        r"about:blank",
    ]
    the_command = " ".join(chrome_args)
    print(the_command)
    print(chrome_args)
    url = f"http://localhost:{the_port}"
    print(f"first try: {url}")
    headless_ft = ft.partial(headless_chrome, chrome_args=chrome_args, options=options)
    trio.run(
        main,
        headless_ft,
        get_addr,
        make_request,
        restrict_keyboard_interrupt_to_checkpoints=True,
    )