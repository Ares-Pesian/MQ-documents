# AI FXDealer — Project Baseline

## What This Is

A multi-tenant SaaS platform for Forex Brokers and Prop Trading Firms.

The platform:
- Collects trading, client, infrastructure, and market data from external systems
- Detects behavioral and technical risks via rule engines
- Assists or automates dealer decisions via an AI layer
- Provides monitoring, investigation tools, and action automation via a dashboard

Core data flow:
```
Collectors → Platform DB → Rule Engines → AI Layer → Dashboard / API → Actions
```

---

## Official Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python (FastAPI) |
| Frontend | Next.js (App Router) |
| Database | PostgreSQL + TimescaleDB |
| Queue / Streaming | Redis Streams |
| Job Scheduler | ARQ (async, Redis-native) |
| Auth | JWT (custom, no third-party auth provider) |
| Secret Management | AWS Secrets Manager |
| Observability | structlog + Prometheus + Grafana + Sentry |
| Deployment | Docker on AWS — monorepo, no Kubernetes in Phase 1 |
| ORM (backend / collectors) | SQLAlchemy + Alembic |
| ORM (product-facing CRUD) | Prisma (only if explicitly needed) |
| API validation | Pydantic (Python), Zod (Node.js if used) |
| Testing | pytest (backend), Jest + Playwright (frontend) |
| Frontend state | TanStack Query (server state) + Zustand (UI state) |
| MT5 integration | MT5Manager pip package (official MetaQuotes Python SDK) |
| MT4 integration | MT4 Manager API DLL via Python ctypes wrapper |
| cTrader integration | Spotware Manager API via Protobuf over TCP |

### Stack decisions — do not change without updating this file

**Python + FastAPI** — collector-heavy, analytics-heavy, rule-heavy, AI-heavy platform. Python fits better than Node.js or Go for data processing, async APIs, and AI integration.

**PostgreSQL + TimescaleDB** — tick data, latency series, event logs, and rule outputs are time-series workloads. TimescaleDB is a PostgreSQL extension — full SQL compatibility, native time-series partitioning. Do not use plain PostgreSQL for time-series tables.

**Redis Streams** — not plain Pub/Sub. Streams give at-least-once delivery with consumer groups and acknowledgment. Required for reliable collector job queuing.

**ARQ** — async job scheduler built on Redis. Used for collector scheduling (run incremental sync every N seconds per broker per server), rule engine job dispatch, and retry orchestration. Do not use cron or bare asyncio loops for scheduled collector runs.

**JWT** — B2B multi-tenant admin platform. JWT gives full control over broker_id, role, permissions, and token lifecycle. No Supabase Auth or Auth0 — external dependency where tight tenant-aware control is needed.

**AWS Secrets Manager** — all credentials (Manager API, CRM tokens, LP keys, SMTP, Telegram, Slack) stored in AWS Secrets Manager. Never in .env files committed to git. Never in plain environment variables in docker-compose for production.

**structlog + Prometheus + Grafana + Sentry** — structured logging from day one. Collector failures must be visible immediately. Silent failures on live broker data are a serious operational problem.

**Docker on AWS, monorepo, no Kubernetes** — all services in one repo. Kubernetes is premature complexity for Phase 1. Add ECS or EKS only when horizontal scaling is actually needed.

**MT5Manager pip** — official MetaQuotes Python SDK. Installed via `pip install MT5Manager`. Provides full Manager API access: accounts, deals, orders, positions, groups, symbols, ticks, server logs, balance operations. Windows-only binary — runs in Windows Docker container or Wine-based container on Linux.

**MT4 Manager API DLL** — MetaQuotes provides the Manager API as a C++ DLL. Wrapped in Python via `ctypes`. DLL is provided by each broker from their MetaTrader 4 Server installation. Windows-only.

**cTrader Manager API** — Spotware's Manager API uses Protocol Buffers (Protobuf) over TCP. Language-neutral. Python client built with `protobuf` + `grpcio` or raw TCP socket handling Protobuf-serialized messages. Docs: https://docs.spotware.com/en/Managers_API

**Prisma** — only if a product-facing CRUD service explicitly needs it. All collector and backend services use SQLAlchemy + Alembic.

---

## Project Structure — Monorepo

```
ai-fxdealer/                           ← monorepo root
│
├── CLAUDE.md                          ← this file
├── pyproject.toml                     ← root workspace (uv or poetry workspaces)
│
├── .claude/
│   ├── settings.json
│   ├── skills/
│   │   ├── collector/SKILL.md
│   │   ├── rule-engine/SKILL.md
│   │   ├── mt5-integration/SKILL.md
│   │   ├── mt4-integration/SKILL.md
│   │   ├── ctrader-integration/SKILL.md
│   │   └── multi-tenancy/SKILL.md
│   └── references/
│       ├── mql4/                      ← MT4 Manager API docs
│       ├── mql5/                      ← MT5 Manager API docs
│       ├── mt5manager-sdk/            ← MT5Manager Python SDK docs
│       ├── ctrader/                   ← Spotware Manager API + Protobuf docs
│       └── fxbo/                      ← FXBO CRM API docs
│
├── services/
│   ├── api/                           ← FastAPI main API service
│   │   ├── routes/
│   │   ├── middleware/
│   │   ├── models/
│   │   └── tests/
│   ├── collector-mt4/                 ← MT4 DLL ctypes collector
│   ├── collector-mt5/                 ← MT5Manager pip collector
│   ├── collector-ctrader/             ← cTrader Protobuf collector
│   ├── collector-fxbo/                ← FXBO CRM collector
│   ├── collector-bridge/              ← Bridge collector
│   ├── collector-lp/                  ← LP collector
│   ├── collector-market/              ← News + economic calendar
│   ├── rule-engine/                   ← Rule engine service
│   └── ai-layer/                      ← AI evaluation service
│
├── dashboard/                         ← Next.js frontend
│   ├── app/
│   ├── components/
│   ├── lib/
│   └── tests/
│
├── packages/
│   ├── shared/                        ← Shared Pydantic models, constants, BaseCollector
│   ├── db/                            ← SQLAlchemy models, Alembic migrations
│   └── queue/                         ← Redis Streams client + ARQ workers
│
├── tests/
│   ├── integration/                   ← Cross-service integration tests
│   └── fixtures/                      ← Captured JSON payloads from real sources
│
├── docker/
│   ├── docker-compose.yml             ← Full stack local dev
│   └── docker-compose.test.yml        ← Test environment
│
└── infra/                             ← AWS infrastructure config
```

### Monorepo dependency model

```
packages/shared     ← no internal dependencies
packages/db         ← depends on: shared
packages/queue      ← depends on: shared

services/api              ← depends on: shared, db, queue
services/collector-mt5    ← depends on: shared, db, queue
services/collector-mt4    ← depends on: shared, db, queue
services/collector-ctrader ← depends on: shared, db, queue
services/collector-fxbo   ← depends on: shared, db, queue
services/rule-engine      ← depends on: shared, db, queue
services/ai-layer         ← depends on: shared, db, queue
```

Each service has its own `pyproject.toml` with local package references. Shared packages are never copied — always imported as workspace dependencies.

---

## Environment Configuration Standard

### Naming convention

All environment variables use the prefix `FXDEALER_`:

```
FXDEALER_DB_URL
FXDEALER_REDIS_URL
FXDEALER_JWT_SECRET
FXDEALER_JWT_EXPIRY_SECONDS
FXDEALER_AWS_REGION
FXDEALER_SENTRY_DSN
FXDEALER_LOG_LEVEL
```

### Environment files

```
.env.local         ← local dev only, never committed
.env.test          ← test environment, committed (no real secrets)
.env.example       ← template with all keys, no values, committed
```

### Secret storage by environment

| Secret type | Local dev | Production |
|---|---|---|
| DB credentials | .env.local | AWS Secrets Manager |
| JWT secret | .env.local | AWS Secrets Manager |
| MT5 Manager credentials | .env.local | AWS Secrets Manager |
| MT4 DLL path + credentials | .env.local | AWS Secrets Manager |
| cTrader API credentials | .env.local | AWS Secrets Manager |
| CRM API keys | .env.local | AWS Secrets Manager |
| Notification tokens | .env.local | AWS Secrets Manager |

### Rules

- Never hardcode secrets in code
- Never commit .env.local
- Never use plain environment variables for production secrets
- Always retrieve from AWS Secrets Manager at service startup
- .env.example must be kept up to date with every new variable

---

## Multi-Tenancy Architecture

This is a strict multi-tenant SaaS. Getting this wrong is a legal and security problem.

### Tenant model

- Each broker or prop firm = one tenant
- Primary tenant key = `broker_id` (UUID)
- One broker can have multiple trading servers, CRM connections, and integrations
- Collectors are instantiated per broker per source connection/server

### Core tenant entities

```
brokers
broker_users
broker_servers
broker_crm_connections
broker_integrations
broker_roles
audit_logs
```

### Data isolation rules

- ALL tenant-owned tables MUST include `broker_id`
- ALL application queries MUST filter by `broker_id`
- ALL API requests MUST resolve `broker_id` from authenticated JWT context
- API middleware MUST enforce `broker_id` scope BEFORE route logic executes
- Background jobs and collectors MUST run in broker-scoped context
- Audit logs MUST include `broker_id` AND `actor_id`
- Cross-tenant access is forbidden by default — no exceptions

### Authenticated request context

Every authenticated request resolves:
```
user_id
broker_id
role
permissions
```

Middleware enforces:
- User belongs to broker
- Route permits role
- Requested resource belongs to same broker

### Collector instantiation model

```python
collector_instance = {
    "broker_id": ...,
    "source_system": ...,      # mt4 | mt5 | ctrader | fxbo | bridge | lp | news | calendar
    "connection_id": ...,
    "server_id": ...,
    "sync_mode": ...,          # bootstrap | incremental
    "status": ...,
    "cursor": ...,
    "last_success_at": ...
}
```

---

## RBAC — Roles and Permissions

RBAC enforced in API middleware before any route logic executes.

### Roles

| Role | Description |
|---|---|
| `admin` | Full access. Manages users, config, rules, executes all actions. |
| `dealer` | Investigates accounts, views all data, executes dealer actions. Cannot manage users. |
| `readonly` | Views data and dashboards only. Cannot execute actions or change config. |

### Permissions by resource

| Resource | admin | dealer | readonly |
|---|---|---|---|
| View accounts / trades / positions | ✅ | ✅ | ✅ |
| View rule findings / evidence | ✅ | ✅ | ✅ |
| View monitoring dashboards | ✅ | ✅ | ✅ |
| View AI suggestions | ✅ | ✅ | ✅ |
| View audit logs | ✅ | ✅ | ❌ |
| Execute dealer actions (profit adj, restrictions) | ✅ | ✅ | ❌ |
| Approve / reject AI suggestions | ✅ | ✅ | ❌ |
| Manage tags | ✅ | ✅ | ❌ |
| Configure rules and thresholds | ✅ | ❌ | ❌ |
| Manage automation triggers | ✅ | ❌ | ❌ |
| Invite / remove team members | ✅ | ❌ | ❌ |
| Assign roles | ✅ | ❌ | ❌ |
| Configure trading server connections | ✅ | ❌ | ❌ |
| Configure notification connectors | ✅ | ❌ | ❌ |

### Enforcement rules

- RBAC check in middleware, never inside route handlers
- Action routes check both role AND broker_id ownership
- A user cannot assign a role higher than their own
- A user cannot remove themselves from a broker
- All action attempts logged in audit_logs including rejected ones

---

## Integration Details

### MT5 — MT5Manager Python Package

**Library:** `MT5Manager` (official MetaQuotes Python SDK)
**Install:** `pip install MT5Manager`
**PyPI:** https://pypi.org/project/mt5manager/
**Docs:** https://support.metaquotes.net/en/docs/mt5/api/managerapi_python

Key facts:
- Official MetaQuotes package — not a third-party wrapper
- Provides full Manager API access as a Python developer
- Windows-only binary (ships as a `.whl` for `win_amd64`)
- Requires numpy >= 1.7
- For Linux deployment: run collector-mt5 service in a Windows Docker container or Wine-based container
- Connects to MT5 Server as manager — not as a trading account
- Supports: accounts, deals, orders, positions, symbols, groups, ticks, server logs, balance operations, margin events

**SDK examples available** (from MetaTrader5SDK):
```
Manager/BalanceExample       ← balance operations reference
Manager/DealerExample        ← dealer workflow reference
Manager/ManagerAPIExtension  ← API extension reference
Manager/SimpleDealer         ← minimal dealer implementation
Manager/SimpleManager        ← minimal manager implementation
```

Reference docs: `.claude/references/mql5/` and `.claude/references/mt5manager-sdk/`

**Collector pattern:**
```python
import MT5Manager

class MT5Collector(BaseCollector):
    def connect(self):
        self.manager = MT5Manager.ManagerAPI()
        self.manager.Connect(server, login, password)

    def fetch_entity(self, entity_name, **kwargs):
        # Returns raw dicts — store exactly as received
        ...
```

---

### MT4 — Manager API DLL via ctypes

**Library:** MT4 Manager API DLL (C++ library from MetaQuotes)
**Format:** `.dll` file provided by each broker's MT4 Server installation
**Python access:** `ctypes` wrapper

Key facts:
- Not pip-installable — DLL is provided directly by MetaQuotes to licensed brokers
- Each broker client provides their own DLL from their server installation
- Windows-only — run collector-mt4 in a Windows Docker container
- Full admin access: accounts, orders, deals, positions, groups, symbols, ticks, server logs
- DLL path configured per broker via AWS Secrets Manager / environment config
- Never hardcode DLL path — always load from broker connection config

**SDK examples available** (from MetaTrader5SDK, also applies to MT4 pattern):
```
Manager/BalanceExample       ← balance operations
Manager/DealerExample        ← dealer workflow
Manager/SimpleManager        ← manager connection baseline
Report/Trades.Standard.Reports ← trade report reference
Report/Accounts.Standard.Reports ← account report reference
```

**Collector pattern:**
```python
import ctypes

class MT4Collector(BaseCollector):
    def connect(self):
        dll_path = get_secret(f"fxdealer/broker/{self.broker_id}/mt4_dll_path")
        self.lib = ctypes.WinDLL(dll_path)
        # Init and connect via DLL functions
```

Reference docs: `.claude/references/mql4/`

---

### cTrader — Spotware Manager API (Protobuf over TCP)

**Library:** Spotware Manager API
**Protocol:** Protocol Buffers (Protobuf) over TCP
**Docs:** https://docs.spotware.com/en/Managers_API
**Python deps:** `protobuf`, `grpcio` (or raw TCP with Protobuf serialization)

Key facts:
- Language-neutral — Python client built against the Protobuf schema
- Protobuf messages define all entities: accounts, orders, deals, positions, ticks, execution reports
- Two data sources: real-time Manager API + Report API (use both, store separately)
- Keep endpoint/version metadata in every raw payload record
- TCP connection is persistent — handle reconnects explicitly in collector

**Collector pattern:**
```python
import grpc
# or raw socket with protobuf serialization

class CTraderCollector(BaseCollector):
    def connect(self):
        # Establish TCP connection to cTrader Manager API
        # Authenticate with credentials from AWS Secrets Manager
        ...

    def fetch_entity(self, entity_name, **kwargs):
        # Serialize request as Protobuf, send over TCP
        # Deserialize response, return as dict
        ...
```

Reference docs: `.claude/references/ctrader/`

---

### FXBO CRM

**Integration:** Read-only REST API or direct DB access
**Mode:** Initial full sync → incremental polling (no writeback in Phase 1)
**Source identifiers:** Preserved exactly, no transformation in raw layer

Entities: `clients, trading_accounts, ibs, transactions, deposits, withdrawals, reports, relation_data`

Reference docs: `.claude/references/fxbo/`

---

## Database Policy

### Raw source data rules

- Raw data MUST be stored EXACTLY as returned by the source
- Raw source payload MUST always be preserved in `payload_json`
- NO normalization in raw tables
- NO business interpretation in raw tables
- Raw tables are the source of truth for replay, debugging, and parser fixes
- Raw source records are append-only — archive instead of delete
- Corrections or re-syncs MUST create superseding records

### Schema design process (critical)

```
For each external integration:
1. Connect to source
2. Inspect actual response payload
3. Store exact raw payload
4. Design raw schema based on REAL returned fields
5. Add normalized/derived schema only in later phases
```

Do NOT design raw schemas from imagination. Design from real source responses.

### Raw table standard pattern

```sql
id                   UUID PRIMARY KEY DEFAULT gen_random_uuid()
broker_id            UUID NOT NULL
source_system        VARCHAR NOT NULL   -- mt4 | mt5 | ctrader | fxbo | ...
source_entity        VARCHAR NOT NULL   -- deals | orders | accounts | ...
source_server_id     UUID
external_id          VARCHAR            -- nullable if source has none
payload_json         JSONB NOT NULL     -- exact source payload, never modified
collected_at         TIMESTAMPTZ NOT NULL
source_timestamp     TIMESTAMPTZ        -- nullable
ingestion_hash       VARCHAR            -- for deduplication
status               VARCHAR NOT NULL DEFAULT 'active'  -- active | archived | superseded
created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW()
updated_at           TIMESTAMPTZ
archived_at          TIMESTAMPTZ
```

### Hybrid raw storage (Phase 1 standard)

Keep `payload_json` AND extract top-level fields for indexing/filtering.

Example for MT5 deals:
```sql
raw_mt5_deals (
    id, broker_id, server_id,
    deal_id, login, symbol,
    volume, price, time_msc,
    action, entry,
    payload_json,
    collected_at
)
```

### TimescaleDB hypertable policy

MUST be hypertables (partitioned by `collected_at`):
```
raw_mt4_ticks              raw_mt5_ticks
raw_mt4_deals              raw_mt5_deals
raw_mt4_orders             raw_mt5_orders
raw_ctrader_ticks          raw_ctrader_execution_reports
raw_lp_quotes              raw_lp_execution_metrics
raw_connectivity_logs      raw_bridge_routing_logs
raw_collector_runs         raw_collector_errors
raw_news_events            raw_economic_calendar_events
```

Stay as plain PostgreSQL (low volume, config/reference):
```
brokers                    broker_servers
broker_users               broker_roles
broker_crm_connections     broker_integrations
audit_logs                 raw_mt4_accounts
raw_mt5_accounts           raw_mt4_symbols
raw_mt5_symbols            raw_fxbo_clients
raw_fxbo_accounts          raw_fxbo_ibs
```

### Indexing strategy

```sql
-- All raw tables
CREATE INDEX ON raw_<table> (broker_id, collected_at DESC);

-- Login / account tables
CREATE INDEX ON raw_mt5_deals (broker_id, login, collected_at DESC);
CREATE INDEX ON raw_mt5_orders (broker_id, login, collected_at DESC);
CREATE INDEX ON raw_mt5_accounts (broker_id, login);

-- Symbol tables
CREATE INDEX ON raw_mt5_deals (broker_id, symbol, collected_at DESC);
CREATE INDEX ON raw_mt5_ticks (broker_id, symbol, collected_at DESC);

-- Deduplication
CREATE UNIQUE INDEX ON raw_mt5_deals (broker_id, server_id, deal_id)
  WHERE status = 'active';

-- Collector operations
CREATE INDEX ON raw_collector_runs (broker_id, source_system, collected_at DESC);
CREATE INDEX ON raw_collector_errors (broker_id, source_system, collected_at DESC);
```

Apply equivalent patterns to MT4, cTrader, and FXBO tables.

### Data retention policy

| Table category | Retention |
|---|---|
| Raw tick data | 90 days (TimescaleDB retention policy) |
| Raw deals, orders, positions | 2 years |
| Raw account data | Indefinite |
| Connectivity and collector logs | 180 days |
| Rule engine outputs | 2 years |
| AI suggestions and decisions | Indefinite |
| Audit logs | Indefinite |
| News and economic events | Indefinite |

Use TimescaleDB `add_retention_policy()`. Define in Alembic migrations, not manually.

---

## Phase 1 Database Tables

Only these tables exist in Phase 1. Do NOT create rule engine or AI schemas yet.

### Tenant / Platform Core
```
brokers                broker_servers
broker_crm_connections broker_integrations
users                  roles
user_broker_roles      audit_logs
```

### Raw MT4 Tables
```
raw_mt4_accounts       raw_mt4_orders
raw_mt4_deals          raw_mt4_positions
raw_mt4_symbols        raw_mt4_groups
raw_mt4_ticks          raw_mt4_server_logs
```

### Raw MT5 Tables
```
raw_mt5_accounts       raw_mt5_orders
raw_mt5_deals          raw_mt5_positions
raw_mt5_symbols        raw_mt5_groups
raw_mt5_ticks          raw_mt5_server_logs
```

### Raw cTrader Tables
```
raw_ctrader_accounts           raw_ctrader_orders
raw_ctrader_deals              raw_ctrader_positions
raw_ctrader_symbols            raw_ctrader_ticks
raw_ctrader_execution_reports
```

### Raw FXBO CRM Tables
```
raw_fxbo_clients       raw_fxbo_accounts
raw_fxbo_ibs           raw_fxbo_transactions
raw_fxbo_deposits      raw_fxbo_withdrawals
raw_fxbo_reports
```

### Raw Infra / Bridge / LP / Market Tables
```
raw_bridge_execution_reports   raw_bridge_routing_logs
raw_bridge_status              raw_lp_feed_status
raw_lp_execution_metrics       raw_lp_quotes
raw_news_events                raw_economic_calendar_events
raw_market_event_timeline      raw_connectivity_logs
raw_collector_runs             raw_collector_errors
```

### NOT in Phase 1 — do not create yet
```
rule engine output tables
AI evaluation tables
dashboard analytics materialized views
normalized trading entity tables
```

---

## BaseCollector Contract

All collector services MUST implement this interface (in `packages/shared/base_collector.py`).

```python
from abc import ABC, abstractmethod

class BaseCollector(ABC):

    @abstractmethod
    def connect(self) -> None:
        """Establish connection to source system."""
        pass

    @abstractmethod
    def health_check(self) -> dict:
        """Verify connection is alive. Return status dict."""
        pass

    @abstractmethod
    def bootstrap_sync(self, start_time=None, end_time=None) -> dict:
        """Full historical backfill for all entities."""
        pass

    @abstractmethod
    def incremental_sync(self, cursor=None) -> dict:
        """Ongoing collection from last known cursor."""
        pass

    @abstractmethod
    def fetch_entity(self, entity_name: str, **kwargs) -> list[dict]:
        """Fetch a specific entity from source. Returns raw dicts."""
        pass

    @abstractmethod
    def save_raw(self, entity_name: str, records: list[dict]) -> int:
        """Store raw records exactly as received. Returns count saved."""
        pass

    @abstractmethod
    def log_run(self, result: dict) -> None:
        """Write collector run result to raw_collector_runs."""
        pass

    @abstractmethod
    def handle_error(self, error: Exception, context: dict) -> None:
        """Handle and log error to raw_collector_errors."""
        pass
```

### Required collector metadata
```python
broker_id         # UUID — tenant scope
source_system     # mt4 | mt5 | ctrader | fxbo | bridge | lp | news | calendar
connection_id     # UUID
server_id         # UUID
sync_mode         # bootstrap | incremental
cursor            # last processed timestamp or ID
last_success_at   # datetime
status            # connected | disconnected | error | syncing
```

---

## Error Handling Standard

### Collector error policy

```
On connection failure:
  1. Log warning (broker_id, source_system, error) via structlog
  2. Retry with exponential backoff: [5s, 30s, 120s]
  3. After 3 retries: status = 'error', write to raw_collector_errors, alert Sentry
  4. Do NOT crash — other broker collectors must keep running

On fetch failure (single entity):
  1. Log error with full context (broker_id, entity, cursor, error)
  2. Write to raw_collector_errors
  3. Skip entity, continue with next
  4. Do NOT stop entire sync run

On save failure:
  1. Log error with payload context
  2. Write to raw_collector_errors
  3. Retain cursor at last successful position
  4. Do NOT advance cursor past failed records
```

### Circuit breaker

5 consecutive failures on a source system:
- Set connection status = `circuit_open`
- Stop attempting for 10 minutes
- Alert Sentry with broker_id and source_system tags
- Resume automatically after cooldown

### API error response shape

```json
{
  "error": {
    "code": "RESOURCE_NOT_FOUND",
    "message": "Account not found",
    "detail": {},
    "request_id": "uuid"
  }
}
```

Never return raw Python exceptions or stack traces in API responses.

### Structured logging standard

```python
log.info(
    "collector.sync.completed",
    broker_id=str(broker_id),
    source_system="mt5",
    server_id=str(server_id),
    entity="deals",
    records_fetched=450,
    records_saved=450,
    duration_ms=1240,
    cursor=new_cursor,
)
```

Never use `print()`. Never use bare `logging.info("message")` without context fields.

---

## API Layer Standard

### Versioning

All routes prefixed `/api/v1/`. No unversioned routes.

```
/api/v1/accounts/
/api/v1/deals/
/api/v1/rules/
/api/v1/collectors/
/api/v1/actions/
/api/v1/audit/
```

Breaking changes introduce `/api/v2/` for affected routes. Deprecate v1 with sunset header before removal.

### Middleware execution order

```
Request in
  → Rate limiting
  → JWT validation
  → broker_id resolution
  → RBAC enforcement
  → Route handler
Response out
  → Request ID injection
  → Structured access log
```

### Route pattern (FastAPI)

```python
router = APIRouter(prefix="/api/v1/accounts", tags=["accounts"])

@router.get("/")
async def list_accounts(
    broker_ctx: BrokerContext = Depends(get_broker_context),
    filters: AccountFilters = Depends(),
    db: AsyncSession = Depends(get_db),
):
    ...
```

---

## Testing Standard

| Layer | Framework |
|---|---|
| Backend unit tests | pytest |
| Backend integration tests | pytest + real PostgreSQL (Docker) |
| Frontend unit tests | Jest |
| Frontend E2E tests | Playwright |

### Test locations

```
services/api/tests/             ← API route and middleware tests
services/collector-mt5/tests/   ← Collector unit tests with mocked MT5Manager
services/collector-mt4/tests/   ← Collector unit tests with mocked DLL
services/collector-ctrader/tests/ ← Collector unit tests with mocked Protobuf
packages/db/tests/              ← DB model and migration tests
tests/integration/              ← Cross-service integration tests
tests/fixtures/                 ← Real captured JSON from MT5, MT4, cTrader, FXBO
dashboard/tests/                ← Frontend unit and E2E tests
```

### Test rules

- Every collector method MUST have a unit test with mocked source responses
- Every API route MUST have integration tests: success, auth failure, wrong broker_id, invalid payload, RBAC rejection
- Mock payloads MUST be real captured JSON from source systems in tests/fixtures/
- Never write tests that require a live MT4/MT5/cTrader/FXBO connection
- All tests must pass in CI before merge

---

## Observability Standard

### Logging — structlog

JSON output in production. Pretty output in local dev. Level via `FXDEALER_LOG_LEVEL`.

```
DEBUG    ← collector step traces (local only)
INFO     ← normal operations, sync completions, route access
WARNING  ← retries, degraded state, slow queries
ERROR    ← failures requiring attention
CRITICAL ← service-level failures, circuit breakers open
```

### Metrics — Prometheus

```
fxdealer_collector_sync_duration_seconds{broker_id, source_system, entity}
fxdealer_collector_records_ingested_total{broker_id, source_system, entity}
fxdealer_collector_errors_total{broker_id, source_system, error_type}
fxdealer_api_request_duration_seconds{route, method, status}
fxdealer_rule_engine_evaluations_total{rule_id, severity}
fxdealer_db_query_duration_seconds{query_type, table}
```

### Error tracking — Sentry

Every service configures Sentry. Every unhandled exception and every circuit breaker event reported with:
- `broker_id` tag
- `source_system` tag
- `environment` tag (dev / staging / production)

Never silence exceptions without logging to Sentry first.

---

## Architecture Rules — MUST Follow

```
- All collector services MUST implement BaseCollector interface
- All collectors MUST be tenant-aware and carry broker_id
- All collectors MUST support: connect, health_check, bootstrap_sync,
  incremental_sync, fetch_entity, save_raw, log_run, handle_error
- All collector scheduling MUST use ARQ — not cron, not raw asyncio loops
- MT5 collectors MUST use MT5Manager pip package
- MT4 collectors MUST use ctypes wrapper around the broker-provided DLL
- cTrader collectors MUST use Protobuf over TCP (Spotware Manager API)
- Raw source data MUST be stored exactly as returned by source
- Raw source payload MUST always be preserved in payload_json
- Rule engine outputs MUST include:
    rule_id, broker_id, account_id, severity (low|medium|high|critical),
    evidence_json, timestamp
- All API routes MUST be prefixed /api/v1/
- All API routes MUST validate payloads with Pydantic (Python) or Zod (Node.js)
- All API routes MUST pass through RBAC middleware before handler executes
- All credentials MUST be stored in AWS Secrets Manager
- All services MUST use structlog for structured logging
- All services MUST expose Prometheus /metrics endpoint
- All unhandled exceptions MUST be reported to Sentry with broker_id tag
- All AI suggestions MUST be logged before any action is taken
- All manual and automatic actions MUST create audit log entries
- All database writes MUST include broker_id where applicable
- All queries touching tenant data MUST filter by broker_id
- All collector runs MUST produce success/failure logs in raw_collector_runs
- Time-series raw tables MUST be created as TimescaleDB hypertables
- All raw tables MUST have composite index on (broker_id, collected_at DESC)
- TimescaleDB retention policies MUST be defined in Alembic migrations
```

---

## Architecture Rules — MUST NOT Do

```
- Never connect directly to MT4/MT5/cTrader/CRM from frontend
- Never store only transformed data without preserving raw payload_json
- Never expose secrets, credentials, or manager connection details in API responses
- Never return raw Python exceptions or stack traces in API responses
- Never use print() — always structlog
- Never commit .env.local or any file with real credentials
- Never store production secrets in plain environment variables
- Never execute actions without first creating an audit log entry
- Never execute AI-based actions without storing AI suggestion and evidence first
- Never delete trading data physically — soft delete / archive only
- Never mix data across tenants
- Never query tenant data without broker_id filtering
- Never allow one broker user to access another broker's data
- Never let collectors write rule-engine outputs into dashboard tables
- Never let frontend call privileged endpoints without RBAC check
- Never design raw schemas from imagination — always from real source responses
- Never create rule engine or AI schema tables until collector contracts are stable
- Never create unversioned API routes
- Never advance collector cursor past failed records
- Never silence exceptions without logging to Sentry
- Never use cron or bare asyncio loops for collector scheduling — use ARQ
- Never hardcode MT4 DLL paths — always load from broker connection config
```

---

## Soft Delete Policy

```
- Raw source records are append-only by default
- Archive instead of delete: status = 'archived', archived_at = NOW()
- Re-syncs create superseding records: status = 'superseded'
- Audit logs are immutable — no soft delete, no archive, no modification
```

---

## Current Development Phase

```
Current Phase: Phase 1 → Phase 2

Active focus:
- Finalize architecture baseline                ✅ done
- Finalize multi-tenant model                   ✅ done
- Finalize raw DB strategy                      ✅ done
- Define BaseCollector contract                 ✅ done
- Lock tech stack + integrations                ✅ done
- MT5 collector: discover real endpoints        ← in progress
- MT5 collector: implement and stabilize        ← next
- MT5 raw schema: design from real payloads     ← next
```

### Full Roadmap

```
Phase 1  — Architecture + Foundation
  1.1    Multi-tenant architecture definition
  1.2    Tech stack finalization
  1.3    Core service contracts and architecture rules
  1.4    Core DB strategy for raw ingestion
  1.5    Auth, RBAC, audit log foundation
  1.6    Environment config and secret management setup
  1.7    Observability setup (structlog, Sentry, Prometheus)

Phase 2  — Collector Framework
  2.1    BaseCollector interface
  2.2    ARQ job scheduler setup
  2.3    Collector runner / scheduler (per broker per server)
  2.4    Broker connection management
  2.5    Raw payload storage
  2.6    Collector logs, retry handling, circuit breaker

Phase 3  — Source Integrations
  3.1    MT5 collector (MT5Manager pip — discover → implement → stabilize)
  3.2    MT4 collector (DLL ctypes wrapper — discover → implement → stabilize)
  3.3    cTrader collector (Protobuf TCP — discover → implement → stabilize)
  3.4    FXBO CRM collector
  3.5    Bridge / LP / market-data collectors

Phase 4  — Rule Engine Foundation
  4.1    Normalization pipeline
  4.2    Rule output schema + evidence model
  4.3    First rule sets (IP match, short-duration, news-time trading)
  4.4    Severity model

Phase 5  — Metrics Inventory + Custom Rule Architecture
  5.1    Metrics catalog
  5.2    Dimensions catalog
  5.3    Custom rule grammar / DSL design
  5.4    Rule configuration model

Phase 6  — Normalized Schemas
  6.1    Normalized trading entity tables
  6.2    Rule output and findings tables
  6.3    Reusable metrics tables

Phase 7  — API Layer
  7.1    Internal service APIs
  7.2    Dashboard data APIs (versioned /api/v1/)
  7.3    AI-facing APIs
  7.4    RBAC middleware enforcement

Phase 8  — Dashboard
  8.1    Auth + tenant scope
  8.2    Collector status pages
  8.3    Account investigation panel
  8.4    Rule findings and evidence panels
  8.5    Monitoring dashboard
  8.6    Rule configuration UI

Phase 9  — AI Layer
  9.1    Case summarization
  9.2    Account risk judgement
  9.3    Suggested action generation
  9.4    Evidence-based justification
  9.5    Dealer review workflow

Phase 10 — Connectors + Action Automation
  10.1   Telegram
  10.2   Slack
  10.3   Email (SMTP + SendGrid)
  10.4   WhatsApp
  10.5   Template-based communications
  10.6   Trigger automation (event → action workflows)
  10.7   Future autonomous actions
```

---

## Reference Implementations

Fill these in as you build. Point Claude to real files rather than re-explaining patterns.

```
BaseCollector           → packages/shared/base_collector.py
MT5 collector           → services/collector-mt5/collector.py
MT4 collector           → services/collector-mt4/collector.py
cTrader collector       → services/collector-ctrader/collector.py
ARQ worker pattern      → packages/queue/workers/collector.py
API route pattern       → services/api/routes/accounts.py
Auth middleware         → services/api/middleware/auth.py
RBAC middleware         → services/api/middleware/rbac.py
Pydantic model pattern  → services/api/models/account.py
Raw ingestion pattern   → services/collector-mt5/ingestion.py
Structured log pattern  → services/collector-mt5/collector.py
Dashboard page pattern  → dashboard/app/investigation/page.tsx
TanStack Query pattern  → dashboard/lib/queries/accounts.ts
```

---

## Documentation References

```
MT5 Manager API (Python)  → .claude/references/mt5manager-sdk/
MT5 API general           → .claude/references/mql5/
MT4 Manager API           → .claude/references/mql4/
cTrader Manager API       → .claude/references/ctrader/
  (Protobuf docs at: https://docs.spotware.com/en/Managers_API)
FXBO CRM                  → .claude/references/fxbo/
```

---

## Design System

### UI Stack

| Layer | Technology |
|---|---|
| Styling | Tailwind CSS |
| Component library | shadcn/ui |
| Icons | Lucide React |
| Data tables | TanStack Table v8 |
| Charts / graphs | Recharts |
| Geo maps | React Leaflet + CartoDB Dark Matter tiles |
| Widgets | Custom components built on shadcn/ui primitives |

---

### Color Palette

```
Background (page base)     #020202
Card background            transparent
Sidebar active item        #161616
Borders                    #1C1C1C
Primary action             #2D61FF  ← buttons, links, active states
Green accent               #3BA468  ← success, healthy, positive PnL
Text secondary             #818181
Text primary               #FFFFFF
```

CSS variables — define in `dashboard/styles/globals.css`. Use everywhere. Never hardcode hex values in components.

```css
:root {
  --bg-base:           #020202;
  --bg-card:           transparent;
  --bg-sidebar-active: #161616;
  --border:            #1C1C1C;
  --primary:           #2D61FF;
  --accent-green:      #3BA468;
  --text-primary:      #FFFFFF;
  --text-secondary:    #818181;

  /* Risk severity — used consistently across ALL tables, badges, charts */
  --risk-critical:     #EF4444;
  --risk-high:         #F97316;
  --risk-medium:       #F59E0B;
  --risk-low:          #3BA468;
  --risk-none:         #818181;
}
```

**Light mode toggle** — available in the profile dropdown in the top nav bar. Light mode overrides CSS variables only. All components use variables — never hardcoded colors. Never build light-mode-only or dark-mode-only components.

---

### Typography

```
Primary font:     Inter (Google Fonts)
Monospace font:   JetBrains Mono
                  → used for: trade IDs, account logins, prices,
                    volumes, timestamps, any numeric trading data

Font scale:
  Page title:     20px / 700
  Section title:  16px / 600
  Table header:   13px / 500 / uppercase / letter-spacing wide
  Body:           14px / 400
  Small / muted:  12px / 400 / var(--text-secondary)
  Data values:    14px monospace / tabular-nums
```

Rule: all numeric trading data (prices, volumes, PnL, IDs, logins) renders in monospace with `tabular-nums` so table columns align correctly.

---

### Layout

#### Overall structure

```
┌─────────────────────────────────────────────────────────────┐
│  Top Nav Bar                                                │
│  [Logo]  [       Global Search Bar       ]  [🔔]  [👤]     │
├──────────────┬──────────────────────────────────────────────┤
│              │                                              │
│  Left        │  Main Content Area                          │
│  Sidebar     │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐       │
│  (fixed)     │  │Widget│ │Widget│ │Widget│ │Widget│       │
│              │  └──────┘ └──────┘ └──────┘ └──────┘       │
│  icon +      │                                              │
│  text label  │  [Table / Chart / Map based on page]        │
│              │                                              │
└──────────────┴──────────────────────────────────────────────┘
```

#### Top nav bar

- Fixed, full width, always visible
- Left: Logo
- Center: Global search bar (searches users, accounts, email)
- Right: Notification icon only (no label) + Profile icon only (no label)
- **Notification panel** → opens as a collapsible right sidebar, slides in from right, full height, closeable
- **Profile menu** → dropdown below icon:
  - Profile settings
  - Light / Dark mode toggle
  - Logout

#### Left sidebar

- Fixed left, full height, always visible on desktop
- Each nav item: icon + text label (never icons alone)
- Collapsible sections with sub-items (accordion style)
- Active item: background `--bg-sidebar-active`, left border accent `--primary`
- Section headers: uppercase, small, muted color

#### Responsive behavior

```
Desktop  > 1280px  → sidebar always visible, full layout
Tablet   768–1280px → sidebar hidden, hamburger menu top-left
Mobile   < 768px   → hamburger menu, single column layout
```

On tablet and mobile, hamburger opens sidebar as a full-height overlay.

---

### Sidebar Navigation Structure

```
📊  Dashboard
    └── Overview

🔍  Investigation
    └── Account Investigation

📈  Trading Data
    ├── Positions
    ├── Deals
    ├── Orders
    └── Execution Details

⚠️   Abuse Detection
    ├── Arbitrage
    ├── HFT
    ├── Copy Trading
    ├── Swap Abuse
    └── Negative Balance

📡  Monitoring
    ├── Price Feed
    ├── Spread Monitoring
    ├── Server Connectivity
    ├── CRM Connectivity
    └── Bridge Connectivity

🛡️   Risk Monitoring
    ├── High Risk Traders
    ├── Slippage Statistics
    ├── Daily Book Overview
    └── Exposure Monitoring

📋  Reporting
    ├── Account Reports
    ├── Rule Engine Reports
    ├── AI Reports
    ├── Financial Reports
    ├── Member Reports
    └── Member Logs

⚙️   Configuration
    ├── Trading Servers
    ├── Connectors
    ├── Rule Configuration
    ├── Tag Management
    ├── Automation
    ├── Email Templates
    └── Domain Settings

👥  Team Management

🔧  System Settings
    ├── Notifications
    └── Profile
```

---

### Data Tables

Every table in the platform follows this standard — no exceptions.

**Required features on every table:**

```
- Column sorting (click header — asc / desc / none)
- Global search bar above the table
- Per-column filter (filter icon in each column header)
- Pagination: configurable rows per page (25 / 50 / 100)
- Column visibility toggle (show/hide columns dropdown)
- Export to CSV button
- Row click → opens detail panel or navigates to detail page
- Loading state: skeleton rows (not spinner)
- Empty state: icon + title + description — never a blank space
```

**Per-column filter operators (all columns support all relevant operators):**

```
Contains
Does not contain
Equals
Does not equal
Greater than          ← numeric / date columns
Less than             ← numeric / date columns
Comma separated       ← multi-value match (e.g. "EURUSD,GBPUSD")
Is blank
Is not blank
```

**Risk / severity badge colors (used consistently everywhere):**

```
CRITICAL  → #EF4444  (red)
HIGH      → #F97316  (orange)
MEDIUM    → #F59E0B  (yellow/amber)
LOW       → #3BA468  (green)
NONE      → #818181  (muted grey)
```

**Implementation:**
- TanStack Table v8
- Column definitions: `dashboard/components/tables/columns/`
- Shared filter logic: `dashboard/lib/table-filters.ts`
- Shared table wrapper component: `dashboard/components/tables/DataTable.tsx`

---

### Charts, Graphs, Widgets, Geo Maps

#### Charts — Recharts

Used for: PnL over time, trade volume by hour/day, exposure by symbol, win rate, slippage distribution, rule engine detection trends.

Rules:
- All chart colors use CSS variables — never hardcoded hex
- Always show skeleton loader while data is loading
- Always show empty state message if no data returns
- Tooltips include: label, value, unit, timestamp where relevant
- Axis labels in `--text-secondary` color
- Grid lines in `--border` color

#### Widgets (summary metric cards)

Top of every page — 4 per row desktop, 2 tablet, 1 mobile:

```
┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐
│  Total Accounts │  │  Flagged Today  │  │  Open Positions │  │  Net Exposure   │
│  12,450         │  │  🔴 34          │  │  892            │  │  $2.4M          │
│  ↑ 2.3% today   │  │  ↑ 5 new        │  │  ↓ 12 closed    │  │  ↑ $140K        │
└─────────────────┘  └─────────────────┘  └─────────────────┘  └─────────────────┘
```

Each widget: label, primary value (large), secondary context (delta / count / %). Color primary value based on meaning (green for positive, risk color for flagged counts).

#### Geo Maps — React Leaflet

Used in: account investigation (IP geolocation), multi-account clustering by region, LP geographic distribution.

Rules:
- Tile layer: CartoDB Dark Matter (`https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png`)
- Cluster dense markers with `react-leaflet-cluster`
- Click marker → opens popover with account/IP details
- Always show a loading state before map tiles render

---

### Global Search Bar

Located center of top nav bar.

**Searchable entities:**
- Users (name, email)
- Trading accounts (login, account number)
- Email address

**Behavior:**
- Dropdown results appear below the bar, grouped by type (Users / Accounts)
- Debounced — API call fires 300ms after typing stops
- Keyboard navigable (↑ ↓ arrows + Enter to select)
- Click result → navigates to relevant detail page
- Shows "No results" state if nothing matches

---

### Component Rules

```
- Use shadcn/ui as base — never rebuild what shadcn already provides
- All modals use shadcn Dialog
- All dropdowns use shadcn DropdownMenu
- All forms use shadcn Form + React Hook Form + Zod validation
- All tooltips use shadcn Tooltip
- All toast notifications use shadcn Sonner
- All date pickers use shadcn Calendar + date-fns
- All skeleton loaders use shadcn Skeleton
- Never use a spinner as the only loading indicator — always skeleton
- Never show a blank page or empty div for empty/loading states
- All timestamps shown in broker local timezone, UTC on hover tooltip
- All monetary values: locale-aware formatting, comma separators, 2 decimal places
- All prices and volumes: monospace font, tabular-nums CSS class
- All risk severity values: colored badge using CSS risk variables
```

---

### Frontend Skill

The frontend design skill is at `.claude/skills/frontend-design/SKILL.md`.

When building any dashboard page or component, Claude must:
1. Read this Design System section in CLAUDE.md
2. Load `.claude/skills/frontend-design/SKILL.md`
3. Check `dashboard/components/` for existing reusable components before creating new ones
4. Never hardcode colors — always use CSS variables
5. Never build a component that shadcn/ui already provides
6. Never skip loading states or empty states

---

## All Decisions Locked ✅

```
✅  Project name:       AI FXDealer
✅  Repo structure:     Monorepo (all services in one repo)
✅  MT5 library:        MT5Manager pip (official MetaQuotes Python SDK)
✅  MT4 library:        MT4 Manager API DLL via Python ctypes wrapper
✅  cTrader library:    Spotware Manager API — Protobuf over TCP
✅  Backend:            Python (FastAPI)
✅  Frontend:           Next.js (App Router)
✅  Database:           PostgreSQL + TimescaleDB
✅  Queue:              Redis Streams
✅  Scheduler:          ARQ
✅  Auth:               JWT (custom)
✅  Secrets:            AWS Secrets Manager
✅  Observability:      structlog + Prometheus + Grafana + Sentry
✅  Deployment:         Docker on AWS (no Kubernetes in Phase 1)
✅  ORM:                SQLAlchemy + Alembic (Prisma only if needed)
✅  Testing:            pytest + Jest + Playwright
✅  Frontend state:     TanStack Query + Zustand
✅  UI components:      shadcn/ui + Tailwind CSS
✅  Icons:              Lucide React
✅  Data tables:        TanStack Table v8
✅  Charts:             Recharts
✅  Geo maps:           React Leaflet + CartoDB Dark Matter
✅  Color palette:      Locked in Design System section
✅  Layout:             Dark theme, left sidebar + top nav, responsive
✅  Light mode:         Toggle in profile dropdown
```

---

## Immediate Next Step

```
Do NOT let Claude generate full platform schemas in one shot.

Correct order:
1. Connect to MT5 test server using MT5Manager
2. Inspect real API responses entity by entity
3. Capture real payloads into tests/fixtures/mt5/
4. Document fields in .claude/references/mt5manager-sdk/
5. Build MT5 collector from real payloads
6. Freeze MT5 raw schema from actual data
7. Only then move to MT4, cTrader, FXBO
```
