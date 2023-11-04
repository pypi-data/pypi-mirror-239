from contextlib import asynccontextmanager

import asyncpg
import grpc
from loguru import logger


@asynccontextmanager
async def ErrorAsyncContextManager(context: any) -> asyncpg.Connection:
    try:
        yield None
    except Exception as e:
        message = type(e).__name__ + ": " + str(e)
        logger.error(message)
        await context.abort(grpc.StatusCode.UNKNOWN, message)


@asynccontextmanager
async def GrpcContextManager(grpc_stub, api_hostname: str, api_port: int = 8080) -> any:
    logger.debug(f"Connecting to grpc api: {api_hostname}:{api_port}")

    with grpc.insecure_channel(f"{api_hostname}:{api_port}") as channel:
        # create the client
        stub = grpc_stub(channel)

        # return the stub
        yield stub

    logger.debug(f"Disconnected from grpc api: {api_hostname}:{api_port}")
