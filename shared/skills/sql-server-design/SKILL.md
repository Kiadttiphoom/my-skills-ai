---
name: sql-server-design
description: Microsoft SQL Server (T-SQL) database design, schema modeling, performance tuning, indexing strategies (B-Tree, Filtered, Columnstore), Temporal Tables (system-versioned audit), Table Partitioning, Row-Level Security (RLS), and Optimistic/Pessimistic Concurrency control. Use when designing, reviewing, or optimizing MS SQL Server databases.
---

# Microsoft SQL Server Database Architect Skill

This skill provides expert T-SQL database design, schema architecture, performance optimization, and enterprise governance standards for Microsoft SQL Server.

## MS SQL Server Architecture Standards

### 1. Data Type Conventions & Guidelines
- **Primary Keys**: Use `UNIQUEIDENTIFIER` with `DEFAULT NEWSEQUENTIALID()` for distributed UUIDs or `BIGINT IDENTITY(1,1)` for sequential IDs.
- **String Types**: Use `VARCHAR` for ASCII-only data, `NVARCHAR` for Unicode/Thai text. Specify explicit lengths (e.g. `NVARCHAR(100)`). Avoid `NVARCHAR(MAX)` unless storing large documents to prevent LOB out-of-row storage overhead.
- **Financial Data**: Always use `DECIMAL(18,4)` or `DECIMAL(19,4)`. Never use `FLOAT` or `REAL`.
- **Date & Time**: Use `DATETIMEOFFSET` for timezone-aware data or `DATETIME2` for high-precision local timestamps. Avoid deprecated `DATETIME` or `MONEY` data types.

### 2. Mandatory Enterprise Columns & T-SQL Pattern
```sql
CREATE TABLE [dbo].[Orders] (
    [OrderId] UNIQUEIDENTIFIER NOT NULL DEFAULT NEWSEQUENTIALID(),
    [TenantId] UNIQUEIDENTIFIER NOT NULL,
    [OrderNumber] NVARCHAR(50) NOT NULL,
    [TotalAmount] DECIMAL(18,4) NOT NULL DEFAULT 0,
    [Status] NVARCHAR(20) NOT NULL,
    
    -- Mandatory Audit & Concurrency Columns
    [CreatedAt] DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    [UpdatedAt] DATETIMEOFFSET NOT NULL DEFAULT SYSDATETIMEOFFSET(),
    [CreatedBy] UNIQUEIDENTIFIER NULL,
    [UpdatedBy] UNIQUEIDENTIFIER NULL,
    [IsDeleted] BIT NOT NULL DEFAULT 0,
    [RowVersion] ROWVERSION NOT NULL, -- Optimistic Concurrency Token
    
    CONSTRAINT [PK_Orders] PRIMARY KEY CLUSTERED ([OrderId] ASC),
    CONSTRAINT [UK_Orders_OrderNumber] UNIQUE ([TenantId], [OrderNumber])
);
```

### 3. Advanced SQL Server Features

#### System-Versioned Temporal Tables (Automated Audit)
```sql
ALTER TABLE [dbo].[Orders] ADD
    [SysStartTime] DATETIME2 GENERATED ALWAYS AS ROW START HIDDEN NOT NULL DEFAULT SYSUTCDATETIME(),
    [SysEndTime] DATETIME2 GENERATED ALWAYS AS ROW END HIDDEN NOT NULL DEFAULT '9999-12-31 23:59:59.9999999',
    PERIOD FOR SYSTEM_TIME ([SysStartTime], [SysEndTime]);

ALTER TABLE [dbo].[Orders] 
    SET (SYSTEM_VERSIONING = ON (HISTORY_TABLE = [dbo].[OrdersHistory]));
```

#### Row-Level Security (RLS) for Multi-Tenancy
- Create an Inline Table-Valued Function for security predicate (`WHERE TenantId = CAST(SESSION_CONTEXT(N'TenantId') AS UNIQUEIDENTIFIER)`).
- Bind to tables via `CREATE SECURITY POLICY`.

### 4. Indexing & T-SQL Performance Rules
- **Clustered Index**: Keep clustered index keys narrow, unique, static, and monotonically increasing.
- **Filtered Non-Clustered Indexes**: Index non-deleted rows only:
  ```sql
  CREATE NONCLUSTERED INDEX [IX_Orders_Tenant_Status] 
  ON [dbo].[Orders] ([TenantId], [Status])
  INCLUDE ([TotalAmount], [CreatedAt])
  WHERE [IsDeleted] = 0;
  ```
- **Columnstore Indexes**: Use Clustered Columnstore Indexes (CCI) for analytical tables with >1M rows to achieve up to 10x compression and batch mode processing.

### 5. Deliverables Checklist
When designing a SQL Server database, output:
1. Architectural Decisions & T-SQL Tech Stack Justification
2. Mermaid.js Visual ERD Diagram
3. Complete T-SQL DDL Script with FK Constraints & Default Constraints
4. Indexing Strategy & Filtered Index Scripts
5. Temporal Audit & RLS Configuration (if applicable)
