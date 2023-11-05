import logging
from asyncio import run
from os import getenv as env
from dotenv import load_dotenv
from tortoise_api_model import init_db

from antifragility_schema import models

load_dotenv()
logging.basicConfig(level=logging.DEBUG)


def test_init_db():
    assert run(init_db(env('PG_DSN'), models)) == True, "DB corrupt"
