from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from threading import Thread
from fastapi import FastAPI
from loguru import logger

from workers.create_order_item_worker import consume_messages
from .routes.order import router as order_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    thread = Thread(target=consume_messages, daemon=True)
    thread.start()
    logger.info("Worker started successfully!")

    yield

    logger.info("Turn off app...")


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(order_router, prefix="/api/v1", tags=["Order"])
