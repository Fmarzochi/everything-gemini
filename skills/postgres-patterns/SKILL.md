---
name: postgres-patterns
description: PostgreSQL database patterns for query optimization, schema design, indexing, and security. Based on Supabase best practices.
origin: ECC
tools: ["run_shell_command", "replace", "read_file", "grep_search", "glob", "list_directory", "write_file"]
---


**CRITICAL INSTRUCTION FOR GEMINI CLI:**
When executing the logic of this skill, you MUST map the conceptual steps to your native toolset:
- Use `read_file` to read file contents.
- Use `replace` to edit files exactly (do not use sed or echo).
- Use `write_file` to create new files.
- Use `grep_search` and `glob` to search across the codebase.
- Use `list_directory` to explore folders.
- Use `run_shell_command` to execute tests, builds, or other terminal commands.
Always verify the output of your tools before proceeding to the next logical step.


# PostgreSQL Patterns

Quick reference for PostgreSQL best practices. For detailed guidance, use the `database-reviewer` agent.

## When to Activate

- Writing SQL queries or migrations
- Designing database schemas
- Troubleshooting slow queries
- Implementing Row Level Security
- Setting up connection pooling

## Quick Reference

### Index Cheat Sheet

| Query Pattern | Index Type | Example |
|--------------|------------|---------|
| `WHERE col = value` | B-tree (default) | `CREATE INDEX idx ON t (col)` |
| `WHERE col > value` | B-tree | `CREATE INDEX idx ON t (col)` |
| `WHERE a = x AND b > y` | Composite | `CREATE INDEX idx ON t (a, b)` |
| `WHERE jsonb @> '{}'` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| `WHERE tsv @@ query` | GIN | `CREATE INDEX idx ON t USING gin (col)` |
| Time-series ranges | BRIN | `CREATE INDEX idx ON t USING brin (col)` |

### Data Type Quick Reference

| Use Case | Correct Type | Avoid |
|----------|-------------|-------|
| IDs | `bigint` | `int`, random UUID |
| Strings | `text` | `varchar(255)` |
| Timestamps | `timestamptz` | `timestamp` |
| Money | `numeric(10,2)` | `float` |
| Flags | `boolean` | `varchar`, `int` |

### Common Patterns

**Composite Index Order:**
```sql
-- Equality columns first, then range columns
CREATE INDEX idx ON orders (status, created_at);
-- Works for: WHERE status = 'pending' AND created_at > '2024-01-01'
```

**Covering Index:**
```sql
CREATE INDEX idx ON users (email) INCLUDE (name, created_at);
-- Avoids table lookup for SELECT email, name, created_at
```

**Partial Index:**
```sql
CREATE INDEX idx ON users (email) WHERE deleted_at IS NULL;
-- Smaller index, only includes active users
```

**RLS Policy (Optimized):**
```sql
CREATE POLICY policy ON orders
  USING ((SELECT auth.uid()) = user_id);  -- Wrap in SELECT!
```

**UPSERT:**
```sql
INSERT INTO settings (user_id, key, value)
VALUES (123, 'theme', 'dark')
ON CONFLICT (user_id, key)
DO UPDATE SET value = EXCLUDED.value;
```

**Cursor Pagination:**
```sql
SELECT * FROM products WHERE id > $last_id ORDER BY id LIMIT 20;
-- O(1) vs OFFSET which is O(n)
```

**Queue Processing:**
```sql
UPDATE jobs SET status = 'processing'
WHERE id = (
  SELECT id FROM jobs WHERE status = 'pending'
  ORDER BY created_at LIMIT 1
  FOR UPDATE SKIP LOCKED
) RETURNING *;
```

### Anti-Pattern Detection

```sql
-- Find unindexed foreign keys
SELECT conrelid::regclass, a.attname
FROM pg_constraint c
JOIN pg_attribute a ON a.attrelid = c.conrelid AND a.attnum = ANY(c.conkey)
WHERE c.contype = 'f'
  AND NOT EXISTS (
    SELECT 1 FROM pg_index i
    WHERE i.indrelid = c.conrelid AND a.attnum = ANY(i.indkey)
  );

-- Find slow queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
WHERE mean_exec_time > 100
ORDER BY mean_exec_time DESC;

-- Check table bloat
SELECT relname, n_dead_tup, last_vacuum
FROM pg_stat_user_tables
WHERE n_dead_tup > 1000
ORDER BY n_dead_tup DESC;
```

### Configuration Template

```sql
-- Connection limits (adjust for RAM)
ALTER SYSTEM SET max_connections = 100;
ALTER SYSTEM SET work_mem = '8MB';

-- Timeouts
ALTER SYSTEM SET idle_in_transaction_session_timeout = '30s';
ALTER SYSTEM SET statement_timeout = '30s';

-- Monitoring
CREATE EXTENSION IF NOT EXISTS pg_stat_statements;

-- Security defaults
REVOKE ALL ON SCHEMA public FROM public;

SELECT pg_reload_conf();
```

## Related

- Agent: `database-reviewer` - Full database review workflow
- Skill: `clickhouse-io` - ClickHouse analytics patterns
- Skill: `backend-patterns` - API and backend patterns

---

*Based on Supabase Agent Skills (credit: Supabase team) (MIT License)*
