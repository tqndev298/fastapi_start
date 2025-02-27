from typing import Annotated
from fastapi import Depends, FastAPI, BackgroundTasks
from app.middleware import ClientInfoMIddleware
from app.profiler import ProfileEndPointsMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.rate_limiter import limiter
from slowapi.middleware import SlowAPIMiddleware


from app.dependencies import check_coupon_validity, select_category, time_range

from app import internationalization
from app.background_tasks import store_query_to_external_db, logger

app = FastAPI()

app.include_router(internationalization.router)


app.add_middleware(ClientInfoMIddleware)
app.add_middleware(ProfileEndPointsMiddleware)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler,
)
app.middleware(SlowAPIMiddleware)


@app.get("/v1/trips")
def get_tours(time_range: Annotated[time_range, Depends()]):
    start, end = time_range
    message = f"Request trip from {start}"
    if end:
        return f"{message} to {end}"
    return message


@app.get("/v2/trips/{category}")
def get_trips_by_category(
    background_tasks: BackgroundTasks,
    category: Annotated[select_category, Depends()],
    discount_applicable: Annotated[bool, Depends(check_coupon_validity)],
):
    category = category.replace("-", " ").title()
    message = f"You requested {category} trips"
    print(discount_applicable)
    if discount_applicable:
        message += "\n. The coupon code is valid! You will get a discount!"
    background_tasks.add_task(
        store_query_to_external_db,
        message,
    )
    logger.info("Query sent to background task, end of request")
    return message
