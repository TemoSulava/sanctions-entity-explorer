"""FastAPI dependencies.

The repository is loaded once on startup into `app.state` (see `app.main`
lifespan) and handed to route handlers through this dependency.
"""

from fastapi import Request

from app.repository import EntityRepository


def get_repository(request: Request) -> EntityRepository:
    return request.app.state.repository
