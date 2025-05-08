from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.custom_exceptions.custom_http_exception import CustomHTTPException
from app.routes.api.v1.user import users_router

app = FastAPI()


@app.exception_handler(CustomHTTPException)
def custom_http_exception_handler(request: Request, exc: CustomHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": exc.success,
            "message": exc.message,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(RequestValidationError)
def request_validation_error_handler(request: Request, exc: RequestValidationError):
    missing_attrs = []
    invalid_data = []
    errors = ""
    _types = [error["type"] for error in exc.errors()]
    print(_types)

    for type_ in range(len(_types)):
        if _types[type_] == "missing":
            missing_attrs.append(exc.errors()[type_]["loc"][1])
        if _types[type_] == "value_error":
            invalid_data.append(exc.errors()[type_]["msg"])

    # if _type == "missing":
        # missing_attrs.append(exc.errors()[0]["loc"][1])

    if missing_attrs:
        errors = errors + f"Fields required: {missing_attrs}"

    if invalid_data:
        errors = errors +  f" Invalid data: {invalid_data}"

    return JSONResponse(
        status_code=422,
        content={
            "success": False,
            "message": "Validation Error",
            "errors": errors
        }
    )

app.include_router(users_router)
