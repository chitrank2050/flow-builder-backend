"""Main entry point for the `Flow-Builder-Backend` application."""

import sys

import uvicorn
from fastapi import FastAPI

from app.core import lifespan, log, settings

# Initialize the FastAPI
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description=settings.APP_DESCRIPTION,
    debug=settings.DEBUG,
    lifespan=lifespan,
)


def main():
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        log.warning("🛑 Application interrupted by user.")
        sys.exit(0)
