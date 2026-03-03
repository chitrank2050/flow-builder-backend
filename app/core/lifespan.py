"""
This file contains the bootloader for the application.
"""

from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI

from .logger import log


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load environment
    load_dotenv()
    log.info("🔄 Loaded environment variables from .env file.")

    # --- STARTUP ---
    log.info("🚀 Server starting up...")

    yield

    # --- SHUTDOWN ---
    log.info("🛑 Server shutting down...")
