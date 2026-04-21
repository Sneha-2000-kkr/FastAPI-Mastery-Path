from fastapi import APIRouter, Depends

from app.dependencies.common import get_quote_service
from app.services.quote_service import QuoteService

router = APIRouter(tags=["quotes"])


@router.get("/quotes/{symbol}")
async def get_quote(symbol: str, svc: QuoteService = Depends(get_quote_service)):
    return await svc.get(symbol)


@router.delete("/cache/quotes/{symbol}")
async def invalidate(symbol: str, svc: QuoteService = Depends(get_quote_service)):
    deleted = await svc.invalidate(symbol)
    return {"deleted": deleted}
