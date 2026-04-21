from celery import Celery

from app.core.config import get_settings

_s = get_settings()

celery_app = Celery(
    "fapi",
    broker=_s.redis_url,
    backend=_s.redis_url,
    include=["app.workers.tasks"],
)

celery_app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_time_limit=60,
    task_soft_time_limit=50,
    worker_prefetch_multiplier=1,
    task_default_queue="default",
)
