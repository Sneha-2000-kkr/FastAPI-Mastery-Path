# Lesson 09 — Async Programming Deep Dive

## 1. Concept Deep Dive

### The event loop
`asyncio` is a **cooperative scheduler**. It runs coroutines on a single thread; each `await` is a *yield point* where the loop can run something else. There is no preemption — a tight CPU loop blocks every other task until it returns to an `await`.

### Coroutines vs Tasks
- **Coroutine**: result of calling an `async def`. Inert until awaited.
- **Task**: a coroutine scheduled on the loop (`asyncio.create_task(coro)`). It runs eagerly.
- `await coro` ≈ "run this and pause me until it's done".
- `await task` ≈ "wait for this already-running thing".

### Concurrency primitives
- `asyncio.gather(*coros, return_exceptions=...)` — fan-out, fan-in. Cancels siblings on first error unless `return_exceptions=True`.
- `asyncio.TaskGroup` (3.11+) — **structured concurrency**: failures cancel siblings, exceptions are aggregated into an `ExceptionGroup`. Prefer this.
- `asyncio.timeout(seconds)` (3.11+) — context manager that cancels its body.
- `asyncio.Semaphore`, `Lock`, `Event`, `Queue` — same primitives, async edition.

### CPU-bound work
The loop is single-threaded. A 200ms hash blocks every concurrent request for 200ms. Solutions:
- `loop.run_in_executor(None, fn, *args)` → thread pool (good for blocking I/O).
- `loop.run_in_executor(ProcessPoolExecutor(), fn, *args)` → process pool (good for CPU).
- `anyio.to_thread.run_sync` is the modern cross-runtime equivalent.

## 2. Production Code Walkthrough

- `services/external.py` — three async "service calls" with random delays.
- `services/cpu.py` — a CPU-heavy `count_primes` function called via a process pool initialised in lifespan.
- `routes/fanout.py` — `gather` and `TaskGroup` variants side by side.
- `routes/timeout.py` — `asyncio.timeout` example.
- `routes/cpu.py` — offloads work via the lifespan-managed pool.

## 3. Why This Matters

99% of FastAPI performance problems trace to two mistakes:
1. Calling blocking I/O inside an `async def` handler.
2. Doing CPU-heavy work on the loop thread.

This module gives you the diagnostic vocabulary to spot and fix both.

## 4. Common Mistakes

- **`time.sleep(1)` in async code.** Use `await asyncio.sleep(1)`.
- **`requests.get(url)` in async code.** Use `httpx.AsyncClient`.
- **Forgetting to `await`.** The coroutine is never scheduled; you get a `RuntimeWarning: coroutine ... was never awaited`.
- **Awaiting tasks inside a loop sequentially.** Build the list, then `await asyncio.gather(*tasks)`.
- **Catching `asyncio.CancelledError` and swallowing it.** Re-raise it — cancellation must propagate.

## 5. Senior-Level Insights

- **Backpressure**: an unbounded `asyncio.Queue` is a memory leak waiting to happen. Use `maxsize=...` and `await queue.put(...)` to block producers.
- **Concurrent client limits**: an `httpx.AsyncClient` shares a connection pool — share one client per app, never per request.
- **Cancellation safety**: any `await` may be cancelled. Hold critical sections under a `try/finally` that releases resources.
- **Don't mix `asyncio.run` inside FastAPI** — the loop is already running; nesting deadlocks.
- **`uvloop`** drops latency 2–4× on Linux. `pip install uvloop` and pass `--loop uvloop`.

## 6. Hands-on Task

Add a `Semaphore(5)` around the external fanout to cap concurrency to 5 simultaneous calls.

## 7. Mini Project

Build a `/scrape?urls=...` endpoint that fetches up to 50 URLs concurrently with httpx, with a per-request timeout, returning per-URL `{ok, status, ms}`.
