from asyncio import run
from os import getenv as env
from dotenv import load_dotenv
from tortoise_api_model import init_db
from tortoise.backends.asyncpg import AsyncpgDBClient

from antifragility_schema import models

load_dotenv()


def test_init_db():
    assert isinstance(run(init_db(env('PG_DSN'), models)), AsyncpgDBClient), "DB corrupt"
