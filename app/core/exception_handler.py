from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import StockPilotException


def register_exception_handlers(app: FastAPI) -> None:

    @app.exception_handler(StockPilotException)
    async def stockpilot_exception_handler(
        request: Request,
        exc: StockPilotException,
    ):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )

# @app.exception_handler(
#     EmailAlreadyExistsException
# )
# async def email_exists_handler(
#     request: Request,
#     exc: EmailAlreadyExistsException,
# ):
#     return JSONResponse(
#         status_code=409,
#         content={
#             "detail": "Email already exists."
#         },
#     )


# @app.exception_handler(
#     InvalidCredentialsException
# )
# async def invalid_credentials_handler(
#     request: Request,
#     exc: InvalidCredentialsException,
# ):
#     return JSONResponse(
#         status_code=401,
#         content={
#             "detail": "Invalid email or password."
#         },
#     )


# @app.exception_handler(
#     UserNotFoundException
# )
# async def user_not_found_handler(
#     request: Request,
#     exc: UserNotFoundException,
# ):
#     return JSONResponse(
#         status_code=404,
#         content={
#             "detail": "User not found."
#         },
#     )