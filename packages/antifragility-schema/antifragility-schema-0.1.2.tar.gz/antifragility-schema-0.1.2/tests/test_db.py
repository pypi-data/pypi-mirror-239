import logging
from asyncio import run
from os import getenv as env
from dotenv import load_dotenv
from tortoise import Tortoise

from antifragility_schema import models

load_dotenv()
logging.basicConfig(level=logging.DEBUG)


async def init_db():
    await Tortoise.init(db_url=env('PG_DSN'), modules={'models': [models]})
    await Tortoise.generate_schemas()
    return True


def test_init_db():
    assert run(init_db()) == True, "DB corrupt"
