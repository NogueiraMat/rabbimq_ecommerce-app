from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from threading import Thread
from fastapi import FastAPI
from loguru import logger

from workers.create_order_item_worker import consume_messages

from .routes.authentication import router as authentication_router
from .routes.product import router as product_router
from .routes.stock import router as stock_router
from .routes.order import router as order_router
from .routes.user import router as user_router


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


app.include_router(authentication_router, prefix="/api/v1", tags=["Authentication"])
app.include_router(product_router, prefix="/api/v1", tags=["Product"])
app.include_router(stock_router, prefix="/api/v1", tags=["Stock"])
app.include_router(order_router, prefix="/api/v1", tags=["Order"])
app.include_router(user_router, prefix="/api/v1", tags=["User"])

