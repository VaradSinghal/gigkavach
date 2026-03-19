# GigShield Backend — Team Structure Guide

## Module Ownership

This backend is split into **3 independent modules** so each team member can work without merge conflicts.

---

### Person 1 — `worker_os/` (Gig Worker OS Layer)
**Scope:** Dashboard, Earnings intelligence, Wallet, Stability Score, Decision Engine

| File | Responsibility |
|------|----------------|
| `routes/dashboard.py` | Unified earnings dashboard endpoints |
| `routes/earnings.py` | Earnings data + boost recommendations |
| `routes/wallet.py` | Micro-savings wallet CRUD |
| `routes/stability.py` | Income stability score endpoint |
| `routes/decision.py` | Work decision engine (GO/CAUTION/STAY) |
| `services/dashboard_service.py` | Dashboard aggregation logic |
| `services/boost_engine.py` | Earnings boost ML/rule engine |
| `services/decision_engine.py` | Decision score calculator |
| `services/wallet_service.py` | Wallet ledger operations |
| `services/stability_score.py` | Stability score formula |
| `schemas.py` | Request/response Pydantic schemas |

---

### Person 2 — `insurance/` (Risk & Insurance Engine)
**Scope:** Premium calculation, Parametric triggers, Claims, Risk scoring, Forecasting

| File | Responsibility |
|------|----------------|
| `routes/premium.py` | Premium calculation + subscription endpoints |
| `routes/claims.py` | Claim history and status endpoints |
| `routes/risk.py` | Risk heatmap + forecast endpoints |
| `services/premium_calculator.py` | Dynamic weekly premium formula |
| `services/parametric_engine.py` | Trigger monitoring (rain/AQI/flood/heat/civic) |
| `services/claim_processor.py` | Zero-touch payout pipeline |
| `services/risk_engine.py` | H3 zone-level risk scoring |
| `services/forecast.py` | Prophet time-series forecasting |
| `schemas.py` | Request/response Pydantic schemas |
| `tasks.py` | Celery async tasks (trigger polling, claim queue) |

---

### Person 3 — `fraud/` (Trust & Fraud Engine + Admin)
**Scope:** Claim validation, Confidence scoring, Ring detection, Trust system, Admin dashboard API

| File | Responsibility |
|------|----------------|
| `routes/admin.py` | Admin analytics + fraud flag endpoints |
| `services/validator.py` | Multi-signal claim validation (3 truth layers) |
| `services/confidence_scorer.py` | 100-point claim confidence scoring |
| `services/ring_detector.py` | Coordinated fraud ring detection |
| `services/trust_manager.py` | Progressive trust system |
| `schemas.py` | Request/response Pydantic schemas |

---

## Shared Code (everyone can use, coordinate changes)

### `models/` — Database Models (SQLAlchemy)
| File | Used By |
|------|---------|
| `worker.py` | All modules |
| `earnings.py` | Person 1, Person 2 |
| `wallet.py` | Person 1 |
| `policy.py` | Person 2, Person 3 |
| `claim.py` | Person 2, Person 3 |
| `zone.py` | Person 2 |

### `services/` — External API Clients
| File | Used By |
|------|---------|
| `weather.py` | Person 1 (boost), Person 2 (triggers, risk) |
| `aqi.py` | Person 2 (triggers), Person 3 (validation) |
| `imd.py` | Person 2 (flood triggers) |
| `payments.py` | Person 2 (payouts) |
| `notifications.py` | Person 1 (decision alerts), Person 2 (claim alerts) |

### Root Files
| File | Purpose |
|------|---------|
| `main.py` | FastAPI app — registers all module routers |
| `config.py` | Env vars, API keys, DB connection strings |
| `database.py` | SQLAlchemy engine + session factory |
| `requirements.txt` | Python dependencies |
| `.env.example` | Environment variable template |

### `ai/` — ML Models, Training & Data (shared, coordinate changes)
| File / Folder | Purpose | Used By |
|--------------|---------|---------|
| `training/train_boost_model.py` | Earnings boost regression model | Person 1 |
| `training/train_premium_model.py` | Premium pricing risk model | Person 2 |
| `training/train_fraud_model.py` | Fraud anomaly detection model | Person 3 |
| `training/train_forecast_model.py` | Prophet disruption forecast model | Person 2 |
| `training/train_zone_risk_model.py` | Hyperlocal zone risk clustering | Person 2 |
| `pipelines/data_pipeline.py` | Data preprocessing pipelines | All |
| `pipelines/feature_engineering.py` | Feature engineering utilities | All |
| `model_loader.py` | Load saved models for inference | All |
| `saved_models/` | Trained model files (.pkl, .joblib) | All |
| `data/` | Sample/seed datasets for training | All |

---

## Rules for Clean Collaboration

1. **Stay in your module folder.** Don't edit files in another person's module.
2. **Shared models** — if you need a new field on a shared model, discuss with the team first.
3. **Shared services** — import and use them, but coordinate before modifying.
4. **Each module registers its own router** in `main.py` — one line per module.
5. **Schemas stay local** — each module has its own `schemas.py` for request/response validation.
