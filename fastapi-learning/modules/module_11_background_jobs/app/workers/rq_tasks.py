import logging
import time

log = logging.getLogger(__name__)


def generate_report(user_id: int) -> dict:
    log.info("generate_report user_id=%s", user_id)
    time.sleep(1.0)
    return {"user_id": user_id, "rows": 42}
