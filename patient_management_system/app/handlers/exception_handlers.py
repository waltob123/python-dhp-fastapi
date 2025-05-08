def value_error_exception_handler(request, exc):
    """
    Custom exception handler for ValueError.

    Args:
        request: The HTTP request object.
        exc: The exception object.

    Returns:
        JSONResponse: A JSON response with the error message and status code.
    """
    # return JSONResponse(
    #     status_code=400,
    #     content={"message": str(exc)},
    # )