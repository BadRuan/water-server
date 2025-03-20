from pydantic import BaseModel
from typing import Any, Optional


class SuccessResponse(BaseModel):
    data: Any
    meta: Optional[dict] = None


class ErrorResponse(BaseModel):
    error: dict = {"type": str, "message": str, "details": dict}
