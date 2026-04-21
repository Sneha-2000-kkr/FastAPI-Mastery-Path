# Lesson 06 — MongoDB with Motor

## 1. Concept Deep Dive

**Motor** is the official async driver, built on PyMongo. It returns coroutines instead of blocking. The wire protocol is the same.

Mongo's data model:
- **Database → Collections → Documents (BSON)**.
- No schema enforced by the server (unless you opt into JSON schema validation).
- `_id` is the primary key. Default is `ObjectId` — a 12-byte value embedding a timestamp + counter.

Indexing is the core skill. Without indexes, every query is a `COLLSCAN`. With the right index, you get an `IXSCAN` — orders of magnitude faster. Always check `.explain("executionStats")`.

### Transactions
Available since 4.0 on replica sets / sharded clusters. Use `async with await client.start_session() as s, s.start_transaction(): ...`. On a single-node dev Mongo, transactions require running it as a one-node replica set.

## 2. Production Code Walkthrough

- `core/mongo.py` — single `AsyncIOMotorClient` (it manages a connection pool internally), exposed via lifespan.
- `models/article.py` — a thin Python model + `from_doc`/`to_doc` mappers.
- `schemas/article.py` — Pydantic with `PyObjectId` adapter so `_id` round-trips cleanly as a string.
- `repository/article_repository.py` — async CRUD using `find`, `insert_one`, `update_one`, `delete_one`.
- `routes/articles.py` — thin handlers.

## 3. Why This Matters

Mongo shines for:
- Document-shaped domains (CMS articles, event payloads, product catalogs with variant attributes).
- Write-heavy workloads where joins aren't needed.
- Polyglot persistence — Postgres for transactional data, Mongo for content.

It is **not** a replacement for a relational DB when you need joins or strong constraints.

## 4. Common Mistakes

- **Querying without indexes.** Add them eagerly; check with `db.articles.getIndexes()`.
- **Letting `_id` leak as `ObjectId`.** Convert at the boundary (Pydantic schemas).
- **Misusing `$lookup` for joins.** It works but is slow. Often a Postgres-style schema is the wrong fit.
- **Storing huge arrays in a single document** (16 MB BSON limit). Use a separate collection.
- **Casting strings to `ObjectId` without try/except.** Use `bson.errors.InvalidId`.

## 5. Senior-Level Insights

- **Read concerns / write concerns**: tune `w`, `j`, `readConcern` per operation. The defaults favor performance over durability.
- **Schema validation**: use `$jsonSchema` collection validators in production — they catch bad writes server-side.
- **Aggregation pipeline** is its own DSL. Spend a day learning `$match → $group → $sort → $project`. It is the equivalent of SQL window functions.
- **Sharding**: choose the shard key carefully — it's near-impossible to change later. Bad shard keys → hot shards.
- **Schema migrations** in Mongo are a pattern: write code that **handles both old and new shapes** during a migration window, then backfill, then drop the old shape.

## 6. Hands-on Task

Add a `tags` field (`list[str]`). Index it (`articles.create_index("tags")`). Add `GET /articles?tag=python` filter.

## 7. Mini Project

Add a `views` counter incremented atomically with `$inc` on `GET /articles/{id}`. Return the new count in the response.
