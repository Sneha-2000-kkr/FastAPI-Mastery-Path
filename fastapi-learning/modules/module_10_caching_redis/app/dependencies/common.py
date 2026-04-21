from app.core.redis_client import get_redis
from app.services.quote_service import QuoteService


def get_quote_service() -> QuoteService:
    return QuoteService(get_redis())
