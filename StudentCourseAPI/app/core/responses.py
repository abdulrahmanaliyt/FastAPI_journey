from typing import Any

from fastapi.encoders import jsonable_encoder


def success_response(message: str, data: Any = None):
    return {
        "success": True,
        "message": message,
        "data": jsonable_encoder(data)
    }


def error_response(message: str, data: Any = None):
    return {
        "success": False,
        "message": message,
        "data": data
    }