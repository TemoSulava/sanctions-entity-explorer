from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import CORS_ORIGINS, DATA_PATH
from app.repository import EntityRepository


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    # Load and validate the fixture once; shape drift fails loud here, on boot.
    app.state.repository = EntityRepository.load_from_file(DATA_PATH)
    yield


def create_app() -> FastAPI:
    app = FastAPI(title="Sanctions Entity Explorer", lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=CORS_ORIGINS,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    return app


app = create_app()
