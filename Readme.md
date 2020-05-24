# trio notes

## installing chromium

1. Borrow functions from https://github.com/miyakogi/pyppeteer to download chromium, return the
   path to the chromium binary, check install.

2. Install those so that we have a console_script that duplicates the
behavior of `pyppeteer-install`

## installing trio-chrome-devtools

- clone https://github.com/HyperionGray/trio-chrome-devtools-protocol.git

- install using poetry

```
conda install poetry
poetry update
poetry install
pytest tests
```
there should be 9 passing tests

## running the example code
