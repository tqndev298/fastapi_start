from typing import Annotated
from fastapi import (
    Depends,
    FastAPI,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
import logging
from app.chat import router as chat_router
from app.security import router as login_router
from app.security import get_username_from_token

logger = logging.getLogger("uvicorn")


app = FastAPI()
app.include_router(chat_router)
app.include_router(login_router)


@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    # if not websocket.headers.get("Authorization"):
    #     return await websocket.close()
    await websocket.accept()
    await websocket.send_text("Welcome to the chat room")
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Message received: {data}")
            await websocket.send_text("Message received!")
            if data == "disconnect":
                logger.warning("Disconnecting...")
                return await websocket.close(
                    code=status.WS_1000_NORMAL_CLOSURE,
                    reason="Disconnecting...",
                )
            if "bad message" in data:
                raise WebSocketException(
                    code=status.WS_1008_POLICY_VIOLATION, reason="Inappropriate message"
                )
    except WebSocketDisconnect:
        logger.warning("Connection closed by the client")
    await websocket.close()


@app.websocket("/secured-ws")
async def secured_websocket(
    websocket: WebSocket,
    username: Annotated[
        get_username_from_token,
        Depends(),
    ],
):
    await websocket.accept()
    await websocket.send_text(f"Welcome {username}")
    async for data in websocket.iter_text():
        await websocket.send_text(f"You wrote: {data}")
