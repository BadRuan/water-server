from fastapi import HTTPException


class APIException(HTTPException):
    def __init__(
        self, status_code: int, error_type: str, message: str, details: dict = None
    ):
        super().__init__(status_code, detail=message)
        self.error_type = error_type
        self.details = details or {}


class ValidationError(APIException):
    def __init__(self, errors: list):
        super().__init__(
            status_code=400,
            error_type="Validation_Error",
            message="Request validation failed",
            details={"errors": errors},
        )


class NotFoundException(APIException):
    def __init__(self, resource: str, identifier: str):
        super().__init__(
            tatus_code=404,
            error_type="Resource_Not_Found",
            message=f"{resource} {identifier} not found",
            details={"resource": resource, "identifier": identifier},
        )
