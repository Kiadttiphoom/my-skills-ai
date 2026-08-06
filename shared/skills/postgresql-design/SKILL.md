---
name: postgresql-design
description: PostgreSQL database schema design, advanced data modeling, indexing strategies (B-Tree, GIN, GiST, BRIN), JSONB modeling, UUIDv7 primary keys, Table Partitioning, Row-Level Security (RLS) for multi-tenancy, and query optimization. Use when designing, reviewing, or optimizing PostgreSQL databases.
---

# PostgreSQL Database Architect & Schema Design Skill

This skill provides expert database design, schema architecture, performance optimization, and security standards tailored specifically for PostgreSQL.

## PostgreSQL Architecture Standards

### 1. Data Types & Best Practices
- **Primary Keys**: Use `UUID` (preferably `UUIDv7` via `gen_random_uuid()` or extensions for time-ordered UUIDs) or `BIGINT GENERATED ALWAYS AS IDENTITY`. Avoid legacy `SERIAL`.
- **String Types**: Use `TEXT` or `VARCHAR(n)`. PostgreSQL handles `TEXT` efficiently with TOAST compression without arbitrary penalty.
- **Financial / Currency**: Use `NUMERIC(18,4)`. Avoid `FLOAT` or `REAL` due to floating point inaccuracies.
- **Timestamps**: Always use `TIMESTAMPTZ` (timestamp with time zone). Never store timezone-naive `TIMESTAMP`.
- **Semi-Structured Data**: Use `JSONB` for schema-less data, metadata, or polymorphic payloads. Always prefer `JSONB` over `JSON` for indexing capabilities.

### 2. Standard Enterprise Table Schema Template
```sql
CREATE TABLE public.orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID NOT NULL,
    order_number VARCHAR(50) NOT NULL,
    total_amount NUMERIC(18,4) NOT NULL DEFAULT 0.0000,
    status VARCHAR(20) NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    
    -- Mandatory Audit & Concurrency
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    created_by UUID NULL,
    updated_by UUID NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    version INT NOT NULL DEFAULT 1,
    
    CONSTRAINT uk_orders_tenant_number UNIQUE (tenant_id, order_number)
);
```

### 3. Advanced PostgreSQL Indexing Strategy
- **B-Tree**: Default for equality (`=`) and range (`<, >, BETWEEN`) queries.
- **GIN Indexing for JSONB & Arrays**:
  ```sql
  CREATE INDEX idx_orders_metadata_gin ON public.orders USING GIN (metadata jsonb_path_ops);
  ```
- **Partial Indexing**: Index active data only to keep index memory footprint small:
  ```sql
  CREATE INDEX idx_orders_active_tenant ON public.orders (tenant_id, status)
  WHERE is_deleted = FALSE;
  ```
- **BRIN Indexing**: Use BRIN (Block Range Index) for append-only logs or time-series tables exceeding 50M rows to save 99% disk space compared to B-Tree.

### 4. Row-Level Security (RLS) for Multi-Tenant Isolation
```sql
ALTER TABLE public.orders ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation_policy ON public.orders
    USING (tenant_id = NULLIF(current_setting('app.current_tenant_id', true), '')::uuid);
```

### 5. Table Partitioning
- Use Declarative Partitioning (`PARTITION BY RANGE (created_at)`) for high-volume logs, telemetry, or transactions.

### 6. Deliverables Checklist
When designing a PostgreSQL database, output:
1. Architecture Decisions & PostgreSQL Feature Justification
2. Mermaid.js Visual ER Diagram
3. Complete PostgreSQL DDL Script (`CREATE TABLE`, Foreign Keys, Constraints)
4. Indexing & JSONB Optimization Plan
5. RLS & Partitioning Configuration (if applicable)
