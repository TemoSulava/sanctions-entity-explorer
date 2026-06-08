from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.routes import router
from app.config import CORS_ORIGINS, DATA_PATH
from app.repository import EntityNotFound, EntityRepository


async def entity_not_found_handler(_: Request, exc: Exception) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc)})


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

    app.add_exception_handler(EntityNotFound, entity_not_found_handler)
    app.include_router(router)
    return app


app = create_app()
