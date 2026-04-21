from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, Response, status

from app.schemas.post import PostCreate, PostPage, PostRead, PostUpdate
from app.services.idempotency import IdempotencyStore, get_idempotency_store, hash_body
from app.services.post_service import PostService, get_post_service

router = APIRouter(prefix="/v1/posts", tags=["posts-v1"])


def _to_read(p) -> PostRead:
    return PostRead(id=p.id, title=p.title, body=p.body,
                    created_at=p.created_at, updated_at=p.updated_at)


@router.get("", response_model=PostPage)
def list_posts(
    cursor: int | None = Query(default=None),
    limit: int = Query(20, ge=1, le=100),
    svc: PostService = Depends(get_post_service),
):
    page, nxt = svc.list_cursor(after_id=cursor, limit=limit)
    return PostPage(items=[_to_read(p) for p in page], next_cursor=nxt)


@router.get("/{post_id}", response_model=PostRead)
def get_post(
    post_id: int,
    response: Response,
    if_none_match: str | None = Header(default=None),
    svc: PostService = Depends(get_post_service),
):
    post = svc.get(post_id)
    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "post not found")
    etag = post.etag()
    if if_none_match == etag:
        return Response(status_code=status.HTTP_304_NOT_MODIFIED, headers={"ETag": etag})
    response.headers["ETag"] = etag
    return _to_read(post)


@router.post("", response_model=PostRead, status_code=status.HTTP_201_CREATED)
async def create_post(
    request: Request,
    payload: PostCreate,
    idempotency_key: str | None = Header(default=None),
    svc: PostService = Depends(get_post_service),
    store: IdempotencyStore = Depends(get_idempotency_store),
):
    body_hash = hash_body(await request.body())

    if idempotency_key:
        prior = store.get(idempotency_key)
        if prior:
            prior_hash, prior_resp = prior
            if prior_hash != body_hash:
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY,
                                    "idempotency key reused with different body")
            return prior_resp

    post = svc.create(title=payload.title, body=payload.body)
    resp = _to_read(post)
    if idempotency_key:
        store.put(idempotency_key, body_hash, resp.model_dump())
    return resp


@router.patch("/{post_id}", response_model=PostRead)
def update_post(
    post_id: int,
    payload: PostUpdate,
    response: Response,
    if_match: str | None = Header(default=None),
    svc: PostService = Depends(get_post_service),
):
    current = svc.get(post_id)
    if current is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "post not found")

    if if_match is not None and if_match != current.etag():
        raise HTTPException(status.HTTP_412_PRECONDITION_FAILED,
                            "resource has changed since last read")

    updated = svc.update(post_id, title=payload.title, body=payload.body)
    assert updated is not None
    response.headers["ETag"] = updated.etag()
    return _to_read(updated)
