from app.ws_manager import ConnectionManager

conn_manager = ConnectionManager()

from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import logging

logger = logging.getLogger("uvicorn")

templates = Jinja2Templates(directory="templates")

router = APIRouter()


@router.get("/chatroom/{username}")
async def chatroom_page_endpoint(request: Request, username: str) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="chatroom.xhtml",
        context={
            "username": username,
        },
    )


@router.websocket("/chatroom/{username}")
async def chatroom_endpoint(websocket: WebSocket, username: str):
    await conn_manager.connect(websocket)
    await conn_manager.broadcast(
        {"sender": "system", "message": f"{username} joined the chat"},
        exclude=websocket,
    )
    logger.info(f"{username} joined the chat")
    try:
        while True:
            data = await websocket.receive_text()
            await conn_manager.broadcast(
                {"sender": username, "message": data}, exclude=websocket
            )
            await conn_manager.send_personal_message(
                {"sender": "You", "message": data},
                websocket,
            )
            logger.info(f"{username} says: {data}")
    except WebSocketDisconnect:
        conn_manager.disconnect(websocket)
        await conn_manager.broadcast(
            {"sender": "system", "message": f"client #{username} left the chat"}
        )
        logger.info(f"{username} left the chat")
