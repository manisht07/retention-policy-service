## `README.md`

```markdown
#  Retention Policy Service

A FastAPI-based microservice to manage and apply data retention policies for enterprise archival systems. Supports complex rule-based expiration logic using a configurable JSON structure.

---

##  Features

- Create, update, and manage retention policies via API (Swagger UI)
- Evaluate expiration date based on dynamic business rules
- Supports nested conditions (`all`, `any`, `not`)
- YAML-based ingestion pipeline configuration
- Adds metadata like `retention_expiration_date`, `policy_name`, `legal_hold_flag` to ingested data
- Supports PostgreSQL (or SQLite for local testing)

---

## Project Structure

```

retention\_policy\_service/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── models.py            # SQLAlchemy model
│   ├── schemas.py           # Pydantic models
│   ├── database.py          # DB session & connection
│   ├── services/
│   │   └── rule\_engine.py   # Rule evaluation logic
│   └── api/
│       └── routes.py        # API endpoints
├── config/
│   └── ingestion.yaml       # Sample batch ingestion config
├── data/                    # Sample input/output
├── tests/
│   └── test\_rule\_engine.py  # Unit tests
├── .env                     # Environment variables
├── requirements.txt         # Python dependencies
└── README.md                # This file

```

---

##  Run Locally

### 1. Clone & Set Up
```bash
git clone https://github.com/YOUR_USERNAME/retention-policy-service.git
cd retention-policy-service
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
# installs dependencies including `python-dateutil` for date-based rule evaluation
```

### 2. Configure Database

PostgreSQL (default):

```bash
createdb mydb
```

Set connection string in `app/database.py`:

```python
DATABASE_URL = "postgresql://postgres@localhost:5432/mydb"
```

Or use SQLite for testing:

```python
DATABASE_URL = "sqlite:///./test.db"
```

### 3. Run the App

```bash
uvicorn app.main:app --reload
```

Open Swagger docs:
 [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Sample API Usage

### Create Policy

```http
POST /api/policies
```

```json
{
  "name": "eu_retention_policy",
  "description": "Retain EU data for 10 years",
  "application": "finance_app",
  "schemas": ["transactions"],
  "tables": ["ledger"],
  "conditions": {
    "type": "conditional",
    "rules": [
      {
        "if": {
          "combinator": "all",
          "conditions": [
            { "field": "region", "operator": "equals", "value": "EU" }
          ]
        },
        "then": {
          "calculate": {
            "field": "created_at",
            "operator": "add_years",
            "value": 10
          }
        }
      }
    ]
  }
}
```

```
