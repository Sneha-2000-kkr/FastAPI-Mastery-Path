import logging
import time

from app.workers.celery_app import celery_app

log = logging.getLogger(__name__)


@celery_app.task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3},
    retry_backoff=True,
    retry_backoff_max=60,
    retry_jitter=True,
    name="tasks.send_email",
)
def send_email(self, *, user_id: int, subject: str, body: str) -> dict:
    log.info("send_email user_id=%s subject=%s try=%s", user_id, subject, self.request.retries)
    time.sleep(0.5)  # simulate SMTP
    return {"user_id": user_id, "delivered": True}
