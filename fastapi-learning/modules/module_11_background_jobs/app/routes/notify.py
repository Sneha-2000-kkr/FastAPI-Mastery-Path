import logging

from fastapi import APIRouter, BackgroundTasks

from app.schemas.jobs import EmailIn

log = logging.getLogger(__name__)
router = APIRouter(tags=["notify"])


def _send(payload: EmailIn) -> None:
    log.info("inline notify -> %s subject=%s", payload.to, payload.subject)


@router.post("/notify")
def notify(payload: EmailIn, bg: BackgroundTasks) -> dict:
    bg.add_task(_send, payload)
    return {"queued": True}
