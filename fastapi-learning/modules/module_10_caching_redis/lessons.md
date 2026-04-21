# Lesson 10 — Caching with Redis

## 1. Concept Deep Dive

### Patterns
- **Cache-aside** (lazy loading): app checks cache → miss → load from source → fill cache. Most common.
- **Read-through / write-through**: cache library sits in front and handles both. Less control.
- **Write-behind**: writes go to cache; flushed to DB asynchronously. Risky for durability.

### Anatomy of a cache miss
1. `GET key` → nil
2. Source query (slow)
3. `SET key value EX ttl` (or `SETEX`)
4. Return value

### TTL strategy
- Short TTL keeps data fresh; long TTL maximizes hit ratio.
- Add **jitter** to TTL (`ttl ± random(0..30s)`) to prevent **thundering herd** at expiry.
- For very hot keys, use **stale-while-revalidate**: return stale value while a single worker refreshes.

### Cache stampede
When a hot key expires, every concurrent request misses simultaneously and hammers the DB. Mitigations:
- TTL jitter
- Single-flight via `SET NX` lock
- Soft TTL: serve stale, refresh in background

### Invalidation
The two hard problems in CS. Strategies:
- TTL-only (eventual)
- Explicit `DEL` on writes
- Versioned keys: `user:42:v3` — bump version on write

## 2. Production Code Walkthrough

- `core/redis_client.py` — single `redis.asyncio.Redis` from URL; lifespan-managed.
- `services/quote_service.py` — cache-aside with `SET NX` single-flight.
- `services/external_quote.py` — fake upstream with 300ms latency.
- `routes/quotes.py` — `GET /quotes/{symbol}`, also `DELETE /cache/quotes/{symbol}` for invalidation.

## 3. Why This Matters

A 95% cache hit ratio on a 50ms DB query removes 47.5ms from p50 — and protects the DB from spikes. Caching is the single highest-leverage performance lever in most backends.

## 4. Common Mistakes

- **Caching errors.** Don't store `None` for "not found" without an explicit short TTL; use a sentinel or shorter TTL.
- **No serialization contract.** Pick `json` or `msgpack`/`pickle`; don't mix.
- **Caching mutable references.** A `dict` in cache becomes a string on the wire — round-trip carefully.
- **Single-flight done with `EXISTS+SET`** — race condition. Use `SET key value NX EX ttl` atomically.
- **No max memory eviction policy.** `maxmemory-policy allkeys-lru` is the safe default.

## 5. Senior-Level Insights

- **Hot keys** become a single-shard problem in Redis Cluster. Shard by tenant/user, not by global keys, when you anticipate this.
- For read-heavy + write-light data, prefer **CDN/edge cache** over app-level Redis.
- Track cache **hit ratio per route** in your metrics — module 15 covers exposing it.
- Always set a **per-cache namespace** (`fapi:quotes:AAPL`) to keep multiple services isolated in shared Redis.
- Beware **cache penetration**: queries for keys that never exist. Mitigate with negative caching + bloom filters in extreme cases.

## 6. Hands-on Task

Add jitter (`ttl + random.randint(-10, 10)`) to the cache TTL.

## 7. Mini Project

Implement stale-while-revalidate: serve a `stale=True` flagged response if the cache entry is in the "soft expired" window (last 25% of TTL), and trigger a background refresh.
