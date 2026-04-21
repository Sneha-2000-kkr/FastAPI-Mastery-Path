# Lesson 11 — Background Jobs

## 1. Concept Deep Dive

A web request must finish in milliseconds. Anything slow (sending email, generating reports, calling slow APIs, processing uploads) belongs in a **background worker**.

Architecture:
```
┌────────┐  enqueue  ┌────────┐  pop   ┌────────┐
│  API   │──────────▶│ Broker │───────▶│ Worker │
└────────┘           └────────┘        └────────┘
                       Redis
```

The broker (Redis/RabbitMQ/SQS) decouples producer from consumer. Workers run in a separate process and can scale independently.

### Celery vs RQ vs BackgroundTasks
- **`BackgroundTasks`** — same-process, runs after the response is returned. Fine for "fire and forget" notifications. Dies with the worker.
- **RQ** — Python-only, Redis-only, simple. Good for small teams.
- **Celery** — battle-tested, multiple brokers, retries, scheduling (`celery beat`), routing, priorities. The Boeing 747 of Python task queues.

### Task semantics
- **Idempotency**: tasks may run more than once (retry, restart). Make them safe to re-run.
- **At-least-once vs exactly-once**: most brokers are at-least-once. Build idempotency keys.
- **Visibility timeout**: if a worker dies mid-task, the broker re-queues after a timeout. Set this longer than your worst-case task duration.
- **Dead-letter queue**: tasks that keep failing should not loop forever. Move to DLQ for inspection.

## 2. Production Code Walkthrough

- `workers/celery_app.py` — `Celery("app", broker=..., backend=...)` with safe defaults (`acks_late=True`, `task_reject_on_worker_lost=True`).
- `workers/tasks.py` — `send_email(user_id, subject, body)` with `autoretry_for=(Exception,)` and exponential backoff.
- `workers/rq_tasks.py` — `generate_report(user_id)` callable for RQ.
- `routes/jobs.py` — enqueue + status endpoints.
- `routes/notify.py` — same-process `BackgroundTasks`.

## 3. Why This Matters

Background jobs are the difference between a 200ms API and a 30s API. They also de-risk failures: a flaky third-party doesn't take down your request path.

## 4. Common Mistakes

- **Passing ORM objects as task args.** Workers serialize args (JSON/pickle). Pass IDs, refetch in the worker.
- **Mutating shared state in tasks.** Two workers run two instances; you'll race.
- **No idempotency.** Retries duplicate side effects. Use idempotency keys (`Idempotency-Key` header, persisted).
- **Logging task failures only via `print`.** Use the worker's logger; pipe to your aggregator.
- **One queue for everything.** Heavy tasks block fast ones. Split queues by SLA.

## 5. Senior-Level Insights

- Use **`acks_late=True`** so a task is only acked after success — survives worker crashes mid-task.
- Set **task time limits** (`time_limit` + `soft_time_limit`). The soft limit raises an exception you can catch and clean up.
- For scheduled jobs, prefer **`celery beat`** with a persistent schedule store (`django-celery-beat` or `celery-redbeat`) over `cron + curl`.
- Observe queue depth + per-task latency. A growing queue is the canary for capacity issues.
- Consider **transactional outbox** if a task must atomically follow a DB write: write task to an `outbox` table in the same transaction; a separate process publishes to the broker. Solves the dual-write problem.

## 6. Hands-on Task

Add `@shared_task(bind=True, max_retries=3)` and call `self.retry(countdown=2 ** self.request.retries)` on failure for `send_email`.

## 7. Mini Project

Add a `celery beat` schedule that triggers `cleanup_expired_quotes` every minute (logs only — the actual cleanup wires into module 10's cache).
