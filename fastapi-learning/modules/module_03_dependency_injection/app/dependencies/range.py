from datetime import date
from fastapi import HTTPException, Query, status


class DateRange:
    """Class-based dependency. Same signature as a function dep."""

    def __init__(
        self,
        from_: date = Query(..., alias="from"),
        to: date = Query(...),
    ) -> None:
        if from_ > to:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                "from must be <= to")
        self.from_ = from_
        self.to = to

    @property
    def days(self) -> int:
        return (self.to - self.from_).days + 1
