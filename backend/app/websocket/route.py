from fastapi import APIRouter, Query, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from starlette.concurrency import run_in_threadpool

from app.websocket.manager import manager
from app.websocket.service import (
    authenticate_websocket,
    save_websocket_message,
    WebSocketMessageError,
)
from app.websocket.schemas import ErrorEvent, MessageSendEvent, MessageCreatedEvent

router = APIRouter()


@router.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket, token: str | None = Query(default=None)
):
    if token is None:
        await websocket.close(code=1008, reason="Authentication required")
        return

    user_id = run_in_threadpool(authenticate_websocket, token)

    if user_id is None:
        await websocket.close(code=1008, reason="Invalid token")
        return

    await manager.connect(user_id, websocket)

    try:
        while True:
            payload = await websocket.receive_json()

            try:
                event = MessageSendEvent.model_validate(payload)
            except ValidationError:
                error = ErrorEvent(message="Invalid event payload")
                await websocket.send_json(error.model_dump())
                continue

            try:
                result = await run_in_threadpool(
                    save_websocket_message,
                    user_id,
                    event.conversation_id,
                    event.content,
                )
            except WebSocketMessageError as e:
                error = ErrorEvent(message=str(e))
                await websocket.send_json(error.model_dump())
                continue

            created_event = MessageCreatedEvent(message=result.message)
            event_data = created_event.model_dump(mode="json")

            await manager.send_to_user(user_id, event_data)

            for recipient_id in result.recipient_id:
                await manager.send_to_user(recipient_id, event_data)

    except WebSocketDisconnect:
        manager.disconnect(user_id, websocket)
