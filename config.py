from dataclasses import dataclass
from typing import Optional
from environs import Env


@dataclass
class TgBot:
    token: str


@dataclass
class Database:
    db_host: str
    db_port: str
    db_name: str
    db_user: str
    db_pass: str


@dataclass
class Redis:
    host: str
    port: int
    db: int


@dataclass
class Config:
    tg_bot: TgBot
    database: Database
    redis: Redis


def load_config(path: Optional[str] = None) -> Config:
    env = Env()
    env.read_env(path)
    return Config(
        tg_bot=TgBot(
            token=env.str("TOKEN")
        ),
        database=Database(
            db_host=env.str("DB_HOST", "localhost"),
            db_port = env.str("DB_PORT", "5432"),
            db_name = env.str("DB_NAME", "postgres"),
            db_user = env.str("DB_USER", "postgres"),
            db_pass = env.str("DB_PASS", "postgres"),
        ),
        redis=Redis(
            host=env.str("R_HOST", "localhost"),
            port=env.int("R_PORT", 6379),
            db=env.int("R_DB", 0)
        )
    )
