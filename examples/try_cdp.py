import os
import asks
import trio
import subprocess
import logging
import functools as ft

import context
from chroman.run_cdp import run

log_level = os.environ.get("LOG_LEVEL", "info").upper()
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger("try_cdp")
logging.getLogger("trio-websocket").setLevel(logging.WARNING)

if __name__ == "__main__":
    testhtml_dir = context.testhtml_dir.resolve()
    targetlist = [
        (
            fr"file://{str(testhtml_dir)}/test_message.html",
            "test_message.pdf",
        ),
        (
            fr"file://{str(testhtml_dir)}/day5_quiz_students.html",
            "day_5_students.pdf",
        ),
        (
            fr"file://{str(testhtml_dir)}/paged_sample_quiz/index.html",
            "paged_sample_quiz.pdf",
        ),
        # (r"https://google.com", "google.png"),
        # (r"https://nytimes.com", "nytimes.png"),
        # (r"https://www.eoas.ubc.ca", "eoas.png"),
        # (r"https://www.washingtonpost.com", "washingtonpost.png"),
        # (r"https://www.latimes.com", "latimes.png"),
        # (r"https://www.amazon.com", "amazon.png"),
    ]

    run(targetlist, 3)
