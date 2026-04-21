from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.dependencies.common import get_article_service
from app.schemas.article import ArticleCreate, ArticleRead, ArticleUpdate
from app.services.article_service import ArticleNotFound, ArticleService

router = APIRouter(prefix="/articles", tags=["articles"])


@router.get("", response_model=list[ArticleRead])
async def list_(
    limit: int = Query(20, ge=1, le=100),
    skip: int = Query(0, ge=0),
    svc: ArticleService = Depends(get_article_service),
):
    return await svc.list(limit=limit, skip=skip)


@router.get("/{article_id}", response_model=ArticleRead)
async def get(article_id: str, svc: ArticleService = Depends(get_article_service)):
    try:
        return await svc.get(article_id)
    except ArticleNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "article not found")


@router.post("", response_model=ArticleRead, status_code=status.HTTP_201_CREATED)
async def create(payload: ArticleCreate, svc: ArticleService = Depends(get_article_service)):
    return await svc.create(**payload.model_dump())


@router.patch("/{article_id}", response_model=ArticleRead)
async def patch(
    article_id: str,
    payload: ArticleUpdate,
    svc: ArticleService = Depends(get_article_service),
):
    diff = {k: v for k, v in payload.model_dump().items() if v is not None}
    try:
        return await svc.update(article_id, diff)
    except ArticleNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "article not found")


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete(article_id: str, svc: ArticleService = Depends(get_article_service)):
    try:
        await svc.delete(article_id)
    except ArticleNotFound:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "article not found")
