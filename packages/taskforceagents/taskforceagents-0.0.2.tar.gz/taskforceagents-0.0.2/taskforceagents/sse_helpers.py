# create a generator that yields the SSE messages
import datetime
import json
import time
import uuid
from enum import Enum

from pydantic import BaseModel
from sse_starlette import ServerSentEvent


def handle_non_serializable(obj):
    if isinstance(obj, Enum) or issubclass(type(obj), Enum):
        return obj.value
    elif isinstance(obj, uuid.UUID):
        return str(obj)
    elif isinstance(obj, datetime.datetime):
        # format as ISO 8601 in utc timezone
        return obj.astimezone(datetime.timezone.utc).isoformat()
    elif isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, BaseModel) or issubclass(type(obj), BaseModel):
        # ConversationMessage
        return obj.model_dump()
    raise TypeError(f"Object of type {type(obj).__name__} is not JSON serializable")


def sse_chatevent(message: str, name: str, id: str = None, **kwargs):
    payload = {
        "id": f"chatevent-{id or str(uuid.uuid4())}",
        "object": "chat_event",
        "created": int(time.time()),
        "message": message,
        "arguments": {
            name: name,
            **kwargs,
        },
    }
    try:
        return ServerSentEvent(
            data=json.dumps(payload, default=handle_non_serializable)
        )
    except TypeError as e:
        print(payload)
        raise e


def sse_text(
    content: str,
    role: str = "assistant",
    model: str = "chatcmpl",
    object: str = "chat.completion.chunk",
    id: str = None,
):
    payload = {
        "choices": [
            {
                "finish_reason": "",
                "index": 0,
                "delta": {"content": content, "role": role},
            }
        ],
        "created": int(time.time()),
        "id": f"{model}-{id or uuid.uuid4()}",
        "model": model,
        "object": object,
    }
    return ServerSentEvent(data=json.dumps(payload, default=handle_non_serializable))


def sse_error(message: str):
    return ServerSentEvent(data=message, event="error")


def sse_stop(
    model: str = "chatcmpl", object: str = "chat.completion.chunk", id: str = None
):
    payload = {
        "choices": [{"finish_reason": "stop", "index": 0, "delta": {}}],
        "created": int(time.time()),
        "id": f"{model}-{id or uuid.uuid4()}",
        "model": model,
        "object": object,
    }
    return ServerSentEvent(data=json.dumps(payload, default=handle_non_serializable))


def sse_done():
    return ServerSentEvent(data="[DONE]")
