# DBR Management API

Daily Breakdown Report (DBR) Management System built with FastAPI, PostgreSQL, TimescaleDB, and Docker.

---

## Overview

DBR Management API is a backend service designed to manage Daily Breakdown Report data imported from operational Excel reports.

The system provides:

* High-performance Excel import engine
* Duplicate file detection using SHA256
* Historical breakdown storage
* Dashboard analytics
* CN-based reporting
* Date range filtering
* REST API integration for dashboards and reporting tools

---

## Technology Stack

| Component         | Technology      |
| ----------------- | --------------- |
| Backend           | FastAPI         |
| Database          | PostgreSQL 16   |
| Extension         | TimescaleDB     |
| ORM               | SQLAlchemy      |
| Validation        | Pydantic        |
| Containerization  | Docker          |
| API Documentation | Swagger/OpenAPI |

---

## Architecture

```text
Excel File
    │
    ▼
Import Engine
    │
    ▼
PostgreSQL + TimescaleDB
    │
    ├── Breakdown Query API
    ├── Dashboard Analytics API
    └── Future BI Integration
```

---

## Database Schema

Schema:

```sql
dbr
```

Main Table:

```sql
dbr.breakdown_history
```

Import Log Table:

```sql
dbr.import_log
```

---

## Breakdown History Structure

| Column               | Description                     |
| -------------------- | ------------------------------- |
| report_date_raw      | Original DATE value from Excel  |
| report_date          | Parsed report date              |
| breakdown_start_date | Parsed Start Break Down date    |
| cn                   | Equipment code                  |
| section              | Section                         |
| trouble_description  | Breakdown description           |
| breakdown_code       | Breakdown category              |
| hm_start             | Hour meter                      |
| location             | Breakdown location              |
| start_breakdown      | Original Start Break Down value |
| start_time           | Breakdown start time            |
| finish_time          | Breakdown finish time           |
| total                | Total downtime                  |
| wo_number            | Work order number               |
| notification_number  | Notification number             |
| action_taken         | Corrective action               |
| mechanic             | Mechanic                        |
| gl                   | Group leader                    |
| created_at           | Record timestamp                |

---

## Import Engine Features

### Excel Upload

```http
POST /api/v1/import/excel
```

Features:

* Bulk insert optimization
* SHA256 duplicate detection
* Import logging
* Transaction protection
* Audit data preservation

---

### Supported Date Formats

The import engine automatically supports:

```text
dd/mm/yy
dd/mm/yyyy
yyyy-mm-dd
yyyy-mm-dd HH:MM:SS
Excel Serial Date
```

Example:

```text
01/02/26
01/02/2026
2026-02-01
2026-02-01 08:30:00
46012
```

---

## API Endpoints

### Breakdown Query

```http
GET /api/v1/breakdowns
```

Filters:

```text
cn
start_date
end_date
page
size
```

---

### Master Data

```http
GET /api/v1/master/cn
```

Returns available CN list.

---

### Dashboard

#### Summary

```http
GET /api/v1/dashboard/summary
```

#### Breakdown Trend

```http
GET /api/v1/dashboard/breakdown-trend
```

#### Top CN

```http
GET /api/v1/dashboard/top-cn
```

#### Top Breakdown Code

```http
GET /api/v1/dashboard/top-breakdown-code
```

#### Monthly Summary

```http
GET /api/v1/dashboard/monthly-summary
```

---

## Pagination Response

Example:

```json
{
  "page": 1,
  "size": 50,
  "total": 16307,
  "pages": 327,
  "items": []
}
```

---

## Data Quality Validation

Current Validation Result:

```text
Total Records       : 16,307
Report Date Filled  : 16,307
Report Date Null    : 0
```

Data quality status:

```text
PASS
```

---

## Dashboard Aggregation Rules

Important:

All dashboard analytics use:

```text
report_date
```

and never:

```text
breakdown_start_date
```

This rule ensures consistency with the original Daily Breakdown Report reporting period.

---

## Local Development

### Clone Repository

```bash
git clone <repository-url>
cd dbr-api
```

---

### Start Containers

```bash
docker compose up -d
```

---

### View Logs

```bash
docker logs -f dbr-api
```

---

### API Documentation

Swagger UI:

```text
http://localhost:8010/docs
```

OpenAPI JSON:

```text
http://localhost:8010/openapi.json
```

---

## Project Status

### Sprint 1

Database Foundation

* Completed

### Sprint 2

Import Engine

* Completed

### Sprint 3.1

Data Model Revision

* Completed

### Sprint 3.2

Query API Layer

* Completed

### Sprint 3.3

Dashboard Analytics

* Completed

### Sprint 3.4

Advanced Analytics & Export API

* Planned

### Sprint 4.0

TimescaleDB Analytics Optimization

* Planned

---

## Future Roadmap

* Export Excel
* Export CSV
* KPI Dashboard
* Materialized Views
* Timescale Continuous Aggregates
* Grafana Integration
* Power BI Integration
* Role-Based Authentication
* Audit Dashboard

---

## License
