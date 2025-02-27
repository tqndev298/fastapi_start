from datetime import date, timedelta
from typing import Annotated, Tuple
from fastapi import Depends, HTTPException, Path, Query


def check_start_end_condition(start: date, end: date):
    if end and end < start:
        raise HTTPException(
            status_code=400, detail="End date must be greater than start date"
        )


def time_range(
    start: date | None = Query(
        default=date.today(),
        description="If not provided the current date is used",
        example=date.today().isoformat(),
    ),
    end: date | None = Query(None, example=date.today() + timedelta(days=7)),
) -> Tuple[date, date | None]:
    check_start_end_condition(start, end)
    return start, end


def select_category(
    category: Annotated[
        str,
        Path(
            description="Kind of travel your are interested in",
            enum=["Cruises", "City Breaks", "Resort Stay"],
        ),
    ]
) -> str:
    return category


def check_coupon_validity(
    category: Annotated[select_category, Depends()],
    code: str | None = Query(None, description="Coupon code"),
) -> bool:
    coupon_dict = {
        "cruises": "CRUISE10",
        "city-breaks": "CITYBREAK15",
        "resort-stays": "RESORT20",
    }
    if code is not None and coupon_dict.get(category, ...) == code:
        return True
    return False
