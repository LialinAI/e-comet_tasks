from typing import Annotated
import asyncpg
import uvicorn
from fastapi import APIRouter, FastAPI, Depends
from core.config import pg_config

dsn = (
    f"postgresql://{pg_config.user}:{pg_config.password}"
    f"@{pg_config.host}:{pg_config.port}/{pg_config.db}"
)


async def get_pg_connection() -> asyncpg.Connection:
    connection = None
    try:
        connection = await asyncpg.connect(dsn)
        yield connection
    except asyncpg.PostgresConnectionError as e:
        print(f"Ошибка подключения к базе данных: {e}")
        raise
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        raise
    finally:
        if connection:
            await connection.close()


async def get_db_version(conn: Annotated[asyncpg.Connection, Depends(get_pg_connection)]):
    return await conn.fetchval("SELECT version()")


def register_routes(app: FastAPI):
    router = APIRouter(prefix="/api")
    router.add_api_route(path="/db_version", endpoint=get_db_version)
    app.include_router(router)


def create_app() -> FastAPI:
    app = FastAPI(title="e-Comet")
    register_routes(app)
    return app


if __name__ == "__main__":
    uvicorn.run("main:create_app", factory=True)
