from fastapi import FastAPI
from starlette.middleware import Middleware
from middleware_project.middleware.asgi_middleware import ASGIMiddleware

app = FastAPI(
    title="Middleware Project",
    middleware=[
        Middleware(
            ASGIMiddleware,
            parameter="example_parameter",
        ),
    ],
)


@app.get("/")
async def read_root():
    return {"Hello": "Middleware World"}
