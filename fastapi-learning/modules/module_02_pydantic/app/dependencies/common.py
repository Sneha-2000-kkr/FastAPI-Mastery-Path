from app.repository.product_repository import get_product_repository
from app.repository.user_repository import get_user_repository
from app.services.product_service import ProductService
from app.services.user_service import UserService


def get_user_service() -> UserService:
    return UserService(get_user_repository())


def get_product_service() -> ProductService:
    return ProductService(get_product_repository())
