from fastapi import APIRouter, HTTPException
from redis import Redis
from rq import Queue

from app.core.config import get_settings
from app.schemas.jobs import EmailIn, EnqueueOut, ReportIn
from app.workers.celery_app import celery_app
from app.workers.rq_tasks import generate_report
from app.workers.tasks import send_email

router = APIRouter(prefix="/jobs", tags=["jobs"])

_settings = get_settings()
_rq = Queue("reports", connection=Redis.from_url(_settings.redis_url))


@router.post("/email", response_model=EnqueueOut)
def enqueue_email(payload: EmailIn) -> EnqueueOut:
    res = send_email.delay(user_id=payload.user_id, subject=payload.subject, body=payload.body)
    return EnqueueOut(task_id=res.id, queue="celery:default")


@router.post("/report", response_model=EnqueueOut)
def enqueue_report(payload: ReportIn) -> EnqueueOut:
    job = _rq.enqueue(generate_report, payload.user_id)
    return EnqueueOut(task_id=job.id, queue="rq:reports")


@router.get("/{task_id}")
def status(task_id: str) -> dict:
    res = celery_app.AsyncResult(task_id)
    if not res:
        raise HTTPException(404, "task not found")
    return {"task_id": task_id, "state": res.state, "result": res.result if res.ready() else None}
