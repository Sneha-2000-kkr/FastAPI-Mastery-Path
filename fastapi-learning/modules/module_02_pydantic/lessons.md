# Lesson 02 — Pydantic v2 Deep Dive

## 1. Concept Deep Dive

Pydantic v2's core is written in Rust (`pydantic-core`). At class definition time, Pydantic builds a **validation schema** (an immutable tree of validator functions) and a **serialization schema**. Both are compiled once and reused for every instance.

When `MyModel(**data)` runs:
1. The validator schema walks the input dict.
2. Each field's coercion + constraints run in C.
3. Errors are accumulated and raised as a single `ValidationError` containing every problem.
4. On success, fields are stored in `__dict__`; default `model_config.frozen=False`.

### Validators
- `@field_validator("x")` — runs after Pydantic's own coercion (mode `"after"` is default).
- `@field_validator("x", mode="before")` — runs on raw input, useful to massage strings.
- `@model_validator(mode="after")` — runs once after every field is validated; use it for cross-field rules.

### Serialization
- `model_dump()` → `dict`, `model_dump_json()` → `str`.
- `by_alias=True` swaps field names for their `alias`. FastAPI does this when `response_model_by_alias=True`.
- `mode="json"` produces JSON-safe primitives (e.g. `datetime` → ISO string).

### Discriminated unions
A union with a `Field(discriminator="kind")` lets Pydantic pick the right variant in O(1) instead of trying each one. Always prefer it over plain `Union`.

## 2. Production Code Walkthrough

- `schemas/user.py` — `UserCreate` enforces a strong password via `field_validator`. `UserRead` uses `computed_field` for `display_name`.
- `schemas/product.py` — `Book | Electronic` discriminated by `kind`. Each variant has its own constraints.
- `schemas/common.py` — `CamelModel` base sets `alias_generator=to_camel`, `populate_by_name=True` so the API talks camelCase but Python stays snake_case.
- `services/user_service.py` — hashes password (placeholder), assigns id, returns the domain `User`.
- `routes/users.py` — uses `response_model=UserRead` to enforce the response contract; the password field never leaves the boundary.

## 3. Why This Matters

- Pydantic is your **first line of defense**. SQL injection, mass-assignment, and JSON-bomb attacks are mitigated by strict schemas.
- Aliases let backend devs write idiomatic Python while frontend devs receive idiomatic JSON. No translation layer needed.
- Discriminated unions model real product variation cleanly — and produce a clean OpenAPI schema with `oneOf + discriminator`, which client codegen tools understand.

## 4. Common Mistakes

- **Re-using the DB model as the API model.** Now any column you add leaks. Always project.
- **`from_attributes=True` everywhere.** Only enable it for response models that map from ORM objects. Enabling it on input schemas accepts arbitrary attributes from junk objects.
- **Calling validators with side effects.** A validator should be pure — running a DB query in there will surprise you when Pydantic re-validates on `model_copy(update=...)`.
- **Stringly-typed fields.** Use `EmailStr`, `HttpUrl`, `UUID4`, `Decimal`, `PositiveInt`. They are free constraints.
- **Mutating defaults.** `tags: list[str] = []` shared between instances → use `Field(default_factory=list)`.

## 5. Senior-Level Insights

- **Schema vs Model**: separate input, update, and output schemas. Update should be all-Optional with `model_config = ConfigDict(extra="forbid")` to reject typos.
- **`extra="forbid"`** for write endpoints: rejects unknown fields → catches frontend bugs early.
- **`extra="ignore"`** for read DTOs from third-party APIs: tolerate provider field changes.
- **Performance**: `model_validate(data)` is faster than `MyModel(**data)` for large dicts because it skips the Python-level `__init__` overhead.
- **Strict mode**: `ConfigDict(strict=True)` rejects coercions like `"1" → 1`. Useful for internal service-to-service calls; harmful for browsers (they send everything as strings).

## 6. Hands-on Task

Add an `Address` nested model on `UserCreate` with `street`, `city`, `country` (ISO-3166 alpha-2). Validate `country` with a `field_validator` that uppercases and rejects unknown codes (use a small whitelist).

## 7. Mini Project

Add a `MovieMedia` and `BookMedia` discriminated union under `/media`. Both share `id`, `title`, `tags`. `MovieMedia` has `runtime_minutes`, `BookMedia` has `pages`. Persist them in an in-memory dict and add `GET /media` returning a properly serialized list.
