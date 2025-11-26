
import code
from fastapi.responses import JSONResponse


def success_response(status: str = "success", message: str = None, data: dict = None, status_code: int = 200) -> JSONResponse:
    return JSONResponse(
        content={
            "status": status,
            "message": message,
            "data": data
        },
        status_code=status_code
    )

def error_response(status: str = "error", message: str = None, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        content={
            "status": status,
            "message": message,
        },
        status_code=status_code
    )
