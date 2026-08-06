---
name: database-design
description: Language-agnostic enterprise database design and data modeling architecture. Covers Domain-Driven Design (DDD), conceptual/logical/physical ERD modeling, relational normalization (3NF/BCNF), NoSQL document modeling, indexing strategy, partitioning/sharding, security, audit trails, and concurrency control. Use when designing complex, scalable, production-ready database schemas for any tech stack.
---

# Enterprise Database Design & Schema Architecture Skill

This skill provides comprehensive guidance for designing production-grade, highly scalable, reliable, and secure database architectures across any technology stack.

## Architecture & Data Modeling Workflow

### 1. Domain & Requirements Analysis
- **Domain-Driven Design (DDD)**: Identify Bounded Contexts, Core Entities, Value Objects, and Aggregate Roots.
- **Workload Classification**: Classify OLTP (Transactional, high concurrent write/read) vs OLAP (Analytical, reporting) workloads.
- **SLA & Invariants**: Establish data latency, availability, retention policies, and consistency levels (ACID vs Eventual Consistency).

### 2. Multi-Model Technology Selection
- **Relational (PostgreSQL, MySQL, SQL Server)**: Complex business logic, strict schemas, foreign keys, ACID compliance.
- **Document (MongoDB, PostgreSQL JSONB)**: Dynamic schemas, hierarchical structures, high-frequency polymorphic data.
- **Key-Value / Cache (Redis)**: Session state, distributed locking, high-speed ephemeral data.
- **Time-Series (TimescaleDB, InfluxDB)**: Telemetry, IoT, financial ticks, high-volume audit event logs.

### 3. Enterprise Schema Standards
Every core transactional entity MUST include standard audit & tracking columns:
```sql
id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
deleted_at TIMESTAMPTZ NULL,
created_by UUID NULL,
updated_by UUID NULL,
version INT NOT NULL DEFAULT 1 -- Optimistic Concurrency Control
```

### 4. Indexing & Query Optimization
- **ESR Rule**: Place Equality `=` columns first, Sort `ORDER BY` columns second, Range `<, >, BETWEEN` columns last in composite indexes.
- **Partial Indexes**: Index active rows only (`WHERE is_deleted = FALSE`).
- **Covering Indexes**: Include frequently queried payload columns to avoid heap lookups.

### 5. Security & Governance
- **Multi-Tenancy**: Enforce Row-Level Security (RLS) at database engine level.
- **Data Protection**: Encrypt PII/sensitive data at rest, hash secrets with salt.
- **Audit Trails**: Immutable change data capture (CDC) or event-sourcing history tables.

### 6. Scalability Patterns
- **Table Partitioning**: Range/List partitioning by date for large tables (>10M rows).
- **Sharding**: Horizontal partitioning across nodes using tenant/entity ID hash.
- **CQRS / Read Replicas**: Separate command (write) models from query (read) models.
