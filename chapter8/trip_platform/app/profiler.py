import os
from fastapi import Request
from pyinstrument import Profiler
from starlette.middleware.base import BaseHTTPMiddleware

profiler = Profiler(interval=0.001, async_mode="enabled")


class ProfileEndPointsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if not profiler.is_running:
            profiler.start()
        response = await call_next(request)
        if profiler.is_running:
            profiler.stop()
            profiler.write_html(os.getcwd() + "/profiler.xhtml")
            profiler.start()
        return response
