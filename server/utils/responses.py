
from fastapi.responses import JSONResponse


def success_response(message: str = "success", data: dict = None, status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        content={
            "status": "success",
            "message": message,
            "data": data
        },
        status_code=status_code
    )

def error_response(message: str = "error", code: int = 400) -> JSONResponse:
    return JSONResponse(
        content={
            "status": "error",
            "message": message,
            "code": code
        },
        status_code=code
    )
