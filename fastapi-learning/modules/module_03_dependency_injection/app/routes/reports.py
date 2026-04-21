from fastapi import APIRouter, Depends

from app.dependencies.range import DateRange

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("")
def report(rng: DateRange = Depends()) -> dict:
    return {"from": rng.from_.isoformat(), "to": rng.to.isoformat(), "days": rng.days}
