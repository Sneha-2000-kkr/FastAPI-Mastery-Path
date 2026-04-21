# Lesson 04 — Project Structuring (Layered Architecture)

## 1. Concept Deep Dive

Layered (a.k.a. **Onion** or **Hexagonal** when taken further) architecture splits the codebase along **direction of dependency**:

```
        ┌─────────────────────────┐
        │  routes (HTTP)          │  knows: schemas, services
        ├─────────────────────────┤
        │  services (use cases)   │  knows: domain models, repository interfaces
        ├─────────────────────────┤
        │  repository (storage)   │  knows: domain models, DB driver
        ├─────────────────────────┤
        │  models (domain)        │  knows: nothing
        └─────────────────────────┘
```

Dependencies point **inward**. The domain knows nothing about HTTP or SQL. This is what makes the system testable, swappable, and scalable across teams.

### Key components
- **Schema** = wire format. Pydantic BaseModel.
- **Domain model** = the thing the business cares about. Pure Python.
- **Repository** = "give me / save me a domain object." Hides storage.
- **Service** = orchestrates repositories, enforces invariants, emits events.
- **Unit of Work (UoW)** = atomically commits a set of repository operations. Critical when you write to two tables in one request.

## 2. Production Code Walkthrough

- `core/config.py`, `core/exceptions.py` — settings + the domain exception hierarchy.
- `models/` — `Customer`, `Order`, `OrderItem` dataclasses.
- `repository/` — in-memory implementations + a `UnitOfWork` that snapshot/rollback dicts.
- `services/order_service.py` — `place_order` shows the real shape of a use case: load customer, validate stock, create order, commit through UoW.
- `routes/` — slim handlers that map exceptions → HTTP codes via `core.exceptions`.

## 3. Why This Matters

Real backends grow. A flat `main.py` collapses under its own weight by month 3. The structure here is the smallest one that **doesn't change** as you scale from 1 to 100 endpoints.

## 4. Common Mistakes

- **"Anemic" services** that just delegate one call to the repo. Either inline them or do real orchestration — don't add a layer for the sake of it.
- **Importing `app` from inside services.** Circular imports follow. Services must not know `FastAPI` exists.
- **Reaching from a route into a repository directly** to "save a query." Now the business rule lives in two places.
- **Mixing Pydantic schemas with domain models.** When validation rules differ from invariants (e.g. an `Order` with empty `items` is invalid in the domain but accepted by the schema during construction), the gap matters.

## 5. Senior-Level Insights

- **Dependency inversion**: services should depend on a `Protocol`/ABC, not the concrete repository. That's how you swap Postgres ↔ Mongo without touching services. We use Protocols here.
- The **Unit of Work** boundary should match the **HTTP request boundary** — exactly one commit per request. Anything else means partial writes.
- Group code by **feature** (e.g. `app/orders/`) once the project gets large enough; the layered structure inside each feature stays the same.
- Use the **lifespan** context to construct shared resources once and inject them via `app.state` or DI providers.

## 6. Hands-on Task

Add a `cancel_order` use case: only allowed when the order is `PENDING`. Throw `OrderNotCancellable` (a domain exception) → 409.

## 7. Mini Project

Add a `/customers/{id}/orders` endpoint that returns the customer's orders with totals. Implement it without adding any new method to `OrderRepository` — write a `customer_orders_view` query in a new `views/` package.
