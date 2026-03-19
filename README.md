<p align="center">
  <img src="https://img.shields.io/badge/GigShield-v1.0-blue?style=for-the-badge" alt="Version"/>
  <img src="https://img.shields.io/badge/Guidewire-DEVTrails%202026-orange?style=for-the-badge" alt="Hackathon"/>
  <img src="https://img.shields.io/badge/Status-Phase%201-green?style=for-the-badge" alt="Status"/>
  <img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge" alt="License"/>
</p>

<h1 align="center">GigShield</h1>
<h3 align="center">Unified Gig Worker Operating System with AI-Powered Parametric Insurance</h3>

<p align="center">
  <strong>Guidewire DEVTrails 2026 — Phase 1</strong><br/>
  Persona: Food Delivery Partners (Zomato / Swiggy)
</p>

---

> **GigShield is not an insurance application.** It is a financial and operational operating system for gig workers that combines income protection, earnings intelligence, and decision support into a single unified platform. *We protect what workers earn today, and optimize how much they can earn tomorrow.*

---

## Table of Contents

- [Core Thesis](#core-thesis)
- [The Problem](#the-problem-why-gigshield-exists)
- [Solution Architecture](#solution-architecture)
- [Platform Features](#platform-features)
  - [Unified Worker Dashboard](#1-unified-gig-worker-dashboard)
  - [AI Earnings Boost Engine](#2-ai-powered-earnings-intelligence--boost-engine)
  - [Work Decision Engine](#3-work-decision-engine)
  - [Parametric Insurance Engine](#4-ai-powered-parametric-insurance-engine)
  - [Zero-Touch Claims & Payouts](#5-zero-touch-automatic-claims--payout-system)
  - [Hyperlocal Risk Engine](#6-hyperlocal-risk-intelligence-engine)
  - [Predictive Risk Forecast](#7-predictive-risk-forecast--early-warning-system)
  - [Income Stability Score](#8-income-stability-score)
  - [Micro-Savings Wallet](#9-micro-savings-wallet)
  - [Cross-Platform Optimizer](#10-cross-platform-work-optimizer)
  - [Visual Risk Heatmap](#11-visual-risk-heatmap)
  - [Admin Analytics Dashboard](#12-insurer--admin-analytics-dashboard)
- [Fraud Detection & Anti-Spoofing](#adversarial-defense--anti-spoofing-engine)
- [Financial Architecture](#financial-architecture--sustainability)
- [Technology Stack](#technology-stack--architecture)
- [Feature Feasibility Matrix](#feature-feasibility-matrix)
- [Platform Partnership Strategy](#platform-partnership-strategy)
- [Scalability & Future Roadmap](#scalability--future-expansion)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)

---

## Core Thesis

India's gig economy employs **15M+ platform-based delivery workers**, growing at double-digit rates annually. Yet these workers — the operational backbone of Zomato, Swiggy, and Zepto — have **zero financial safety net**. They earn daily, spend daily, and when disruptions hit, they lose daily with no recovery mechanism.

GigShield addresses **three structural gaps** simultaneously:

| Gap | Solution | Approach |
|-----|----------|----------|
| **No Income Protection** | Parametric Insurance | AI-powered auto-payouts triggered by real-time disruption data — zero claim filing |
| **No Earnings Intelligence** | Boost Engine | Data-driven recommendations on when/where to work for maximum earnings |
| **No Financial Structure** | Savings & Tracking | Micro-savings wallet, income tracking, and stability scoring for long-term resilience |

### Strategic Positioning

```
┌─────────────────────────────────────────────────┐
│            DELIVERY PLATFORMS                    │
│      (Zomato, Swiggy, Zepto)                    │
│  Execution Layer: Orders, Routing, Payments     │
├─────────────────────────────────────────────────┤
│               GIGSHIELD                          │
│  Worker Layer: Earnings, Risk, Financial Health  │
│  ➜ Complementary, NOT competitive               │
└─────────────────────────────────────────────────┘
```

---

## The Problem: Why GigShield Exists

### 2.1 Income Instability
Daily income swings between **₹300 – ₹1,200** based on weather, order volume, time of day, zone assignment, and platform incentive structures. Weekly payout cycles compound the instability.

### 2.2 Zero Protection During Disruptions
Extreme rainfall, flooding, severe AQI, curfews, or strikes make work impossible — and the worker bears 100% of the cost. A single flooded day in Chennai = **₹400–₹700 lost**. A week of poor AQI in Delhi = **4–5 working days eliminated**.

### 2.3 No Decision Intelligence
Workers make dozens of daily micro-decisions on instinct: when to start, which zone, when to break. No tool provides data-driven guidance on demand peaks, weather impacts, or zone-level opportunity.

### 2.4 Multi-Platform Fragmentation
Workers operating across Swiggy, Zomato, and Zepto have no unified earnings view, no cross-platform performance comparison, and no tool to optimize across segments.

### 2.5 Financial Exclusion
No salary slips = no credit access. No savings mechanisms calibrated to gig rhythms. No insurance designed for their risk profile. The products simply haven't been built for them.

### 2.6 Platform Power Asymmetry
Sudden incentive changes, zone reassignments, or algorithm updates can slash earnings without notice. Workers have zero data, zero recourse, and zero negotiating power.

---

## Solution Architecture

GigShield is a **three-layer operating system**:

```
┌──────────────────────────────────────────────────────────┐
│  LAYER 1: GIG WORKER OS                                  │
│  Unified dashboard • Earnings intelligence • Work        │
│  guidance • Multi-platform view • Savings wallet         │
├──────────────────────────────────────────────────────────┤
│  LAYER 2: RISK & INSURANCE ENGINE                        │
│  AI premium calculation • Parametric triggers •          │
│  Automated payouts • Hyperlocal risk scoring             │
├──────────────────────────────────────────────────────────┤
│  LAYER 3: TRUST & FRAUD ENGINE                           │
│  Multi-signal validation • Behavioral analysis •         │
│  Coordinated fraud ring detection • Progressive trust    │
└──────────────────────────────────────────────────────────┘
```

---

## Platform Features

### 1. Unified Gig Worker Dashboard

**Problem Solved:** Workers check multiple apps to understand total income — fragmented, time-consuming, and missing the big picture.

**What It Does:**
- Aggregates earnings, hours, and performance across all platforms in a single view
- Shows daily / weekly / monthly breakdowns with platform-wise contribution
- Compares current performance against personal historical averages
- Mobile-first design (workers operate entirely from phones)

**Implementation:**

| Phase | Approach |
|-------|----------|
| Phase 1–2 | Manual data entry + simulated platform API data |
| Phase 3+ | Formal data-sharing partnerships with platforms for live feed |

**Tech Stack:** React Native (mobile-first) → Node.js API → PostgreSQL

**Business Value:**  
This is the **daily active usage driver**. An insurance app used only during disruptions won't retain users. A dashboard used every day builds the habit that makes the insurance layer viable.

---

### 2. AI-Powered Earnings Intelligence & Boost Engine

**Problem Solved:** Workers rely on instinct for where/when to work, consistently underperforming their earnings potential.

**What It Does:**
- Analyzes time-of-day, location, weather, historical demand, and platform promotions
- Generates **zone-level earnings potential scores** updated every 30 minutes
- Delivers actionable recommendations:
  > *"Order demand in Velachery zone is elevated between 7:30–9:30 PM tonight. Shifting there is projected to improve earnings by 20–30%."*

**Implementation:**

| Phase | Model |
|-------|-------|
| Phase 1 | **Rule-based engine** using weather API + manually curated demand patterns by time/day/zone |
| Phase 2 | **Regression model** (scikit-learn) trained on platform's accumulated earnings & demand data |
| Phase 3 | **Gradient Boosted Trees** (XGBoost/LightGBM) for higher accuracy with feature importance analysis |

**Model Inputs:**  
`time_of_day` · `weather_conditions` · `worker_location` · `historical_order_density[zone][time]` · `active_promotions`

**Tech Stack:** Python (scikit-learn/XGBoost) · OpenWeather API · PostgreSQL

**Business Value:**  
If GigShield increases weekly earnings by even **₹200**, workers will recommend it to peers, stay subscribed, and trust the insurance layer. This is the **#1 acquisition driver**.

---

### 3. Work Decision Engine

**Problem Solved:** Workers have no way to assess whether conditions favor working, require caution, or suggest staying home.

**What It Does:**
Generates a **Decision Score (0–100)** at the start of each work session with a simple traffic-light recommendation:

| Score | Recommendation | Action |
|-------|---------------|--------|
| **65–100** | GO | Conditions favor working — high demand, low risk |
| **35–64** | CAUTION | Moderate risk — work with awareness |
| **0–34** | STAY HOME | High disruption risk — insurance alert triggered |

**Scoring Formula:**

```
Decision Score = (Demand × 0.35) + (Weather Safety × 0.35) 
               + (Insurance Coverage × 0.20) + (Historical Stability × 0.10)
```

- **Demand (35%):** Expected order volume for the worker's zone at current time
- **Weather Safety (35%):** Inverse of current/forecast risk (rain, AQI, heat)
- **Insurance Coverage (20%):** Covered workers can tolerate slightly higher risk
- **Historical Stability (10%):** Disruption probability based on historical data for that zone/day

**Tech Stack:** Python scoring service · Firebase Cloud Messaging (push notifications)

**Business Value:**  
Workers who follow stay-home recommendations avoid disruption entirely → **lower claim rate** while maintaining premium revenue. Workers advised to stay home expect a payout → **reinforces insurance value**.

---

### 4. AI-Powered Parametric Insurance Engine

**Problem Solved:** No income protection product exists for gig workers. Traditional insurance requires claims, documentation, and wait times — none of which work for daily earners.

**What It Does:**
- Dynamically calculates a **weekly premium** per worker based on individual risk profile
- Monitors **five disruption categories** via real-time APIs
- Automatically initiates payouts when triggers are met — **zero claim filing**

#### Premium Calculation Model

```
Weekly Premium = Base Premium + Zone Risk Adjustment + Weather Forecast Adjustment
Coverage Ceiling = 70% × Average Weekly Earnings
```

**Worked Example:**
| Component | Value | Explanation |
|-----------|-------|-------------|
| Base Premium | ₹25 | Floor cost of coverage |
| Zone Risk Adjustment | +₹12 | Chennai Adyar zone — moderate flood risk |
| Weather Forecast Adjustment | +₹8 | Moderate rain predicted next week |
| **Total Weekly Premium** | **₹45** | |
| Average Weekly Income | ₹4,200 | Based on earnings history |
| **Coverage Ceiling** | **₹2,940** | 70% of average weekly income |

#### Parametric Trigger Definitions

| Trigger | Condition | Data Source |
|---------|-----------|-------------|
| **Heavy Rainfall** | Cumulative rainfall > **40mm in 6-hour window** | OpenWeather API |
| **Severe Air Quality** | AQI > **350 for 3+ consecutive hours** | AQICN API |
| **Flooding** | Active flood alerts for worker's zone | India Meteorological Dept (IMD) API |
| **Civic Disruption** | Zone closures, curfews, or strikes detected | Traffic APIs + Government alert feeds |
| **Extreme Heat** | Temperature > **43°C during standard work hours** | OpenWeather API |

#### Processing Pipeline

```
API Polling (every 15 min)
    │
    ├─► Trigger Condition Met?
    │       │
    │       YES ──► Create Claim Event
    │                   │
    │                   ├─► Fraud Validation (confidence score)
    │                   │
    │                   ├─► Payout Calculation
    │                   │   (inactive hours × avg hourly income)
    │                   │
    │                   └─► Queue Payout (< 10 min total)
    │
    └─► NO ──► Continue monitoring
```

**Tech Stack:** FastAPI (Python) · Celery (task queue) · Redis (cache/session) · PostgreSQL

---

### 5. Zero-Touch Automatic Claims & Payout System

**Problem Solved:** Traditional claims require forms, documentation, and waiting — unacceptable for workers who lose income daily.

**What It Does:**
The worker takes **zero action**. The system detects the disruption, validates the claim, calculates the payout, and transfers money — all automatically. The worker receives a push notification:

> *"Your income was protected. ₹420 has been transferred to your account for 6 hours of rain disruption in your zone."*

**Event-Driven Architecture:**

```
Parametric Engine ──► Claim Event Queue (Celery)
                           │
                    Claim Processor
                    ├── 1. Query Fraud Validation Service
                    │       └── Confidence Score ≥ threshold?
                    ├── 2. Calculate Payout Amount
                    │       └── Inactive Hours × Avg Hourly Income
                    └── 3. Push to Payment Gateway
                            └── Razorpay Test Mode / UPI Sandbox
```

**Tech Stack:** Celery + Redis broker · Razorpay (test mode) · UPI Sandbox · FCM notifications

**Business Value:**  
This is GigShield's **strongest differentiator**. Zero friction in claims = trust. Trust is the single most critical asset in insurance.

---

### 6. Hyperlocal Risk Intelligence Engine

**Problem Solved:** City-level risk assessment is too coarse. Adyar and T. Nagar in Chennai have entirely different flood risk profiles despite being in the same city.

**What It Does:**
- Divides cities into **micro-zones (~1–2 km²)** using Uber's H3 hexagonal grid
- Assigns each hex cell an independent **risk score (0–100)** based on four data layers
- Scores update **daily** and drive premium pricing, payout calculations, and recommendations

**Risk Score Inputs:**

| Data Layer | Source | Weight |
|------------|--------|--------|
| Historical weather events (frequency + severity) | OpenWeather historical data | 30% |
| Terrain & drainage characteristics | Open geospatial datasets (OSM, SRTM) | 25% |
| Historical claims data | Platform accumulation | 25% |
| Real-time conditions (rainfall, AQI, traffic) | Live APIs | 20% |

**Tech Stack:** H3 (Uber Hexagonal Grid) · PostGIS (PostgreSQL extension) · scikit-learn (clustering/scoring) · Mapbox SDK (visualization)

**Business Value:**  
Hyperlocal scoring produces **more accurate premiums** (reduces adverse selection) and **more accurate payouts** (reduces loss ratios). This is a key technical differentiator from competitors.

---

### 7. Predictive Risk Forecast & Early Warning System

**Problem Solved:** Workers have no advance warning of disruptions — they react only after income is already lost.

**What It Does:**
- Sends **12–24 hour advance notifications** of expected disruptions
- Provides **weekly risk forecasts** for each zone at the start of the week
- Links forecast to premium adjustments — workers understand *why* their premium changed

**Example Notification:**
> *"Heavy rain forecast for your Adyar zone tomorrow evening (6–11 PM). Your coverage is active. If you're unable to work, expect an automatic payout."*

**Implementation:**

| Component | Technology | Approach |
|-----------|-----------|----------|
| Weather Forecast | OpenWeather 5-day API | Primary predictive input |
| Time-Series Model | **Prophet** (Meta) | Historical disruption pattern analysis per zone |
| Notifications | Firebase Cloud Messaging | Push alerts for disruption warnings & premium changes |

**Business Value:**  
A platform that tells workers what's coming *before it happens* builds **emotional attachment**. It also reduces the shock of premium increases by explaining them proactively.

---

### 8. Income Stability Score

**Problem Solved:** Workers have no metric to understand or improve the resilience of their financial situation.

**What It Does:**
A single score **(0–100)** quantifying income consistency and resilience, displayed on the dashboard with specific improvement recommendations.

**Scoring Formula:**

```
Stability Score = (Earnings Consistency × 0.40) + (Risk Zone Exposure × 0.25)
                + (Insurance Utilization × 0.20) + (Savings Behavior × 0.15)
```

| Component | Weight | Measurement |
|-----------|--------|-------------|
| Earnings Consistency | 40% | Coefficient of variation of weekly earnings |
| Risk Zone Exposure | 25% | Average risk score of worker's operating zones |
| Insurance Utilization | 20% | Active coverage + claim benefit history |
| Savings Behavior | 15% | Micro-savings wallet contribution rate |

**Example Recommendation:**
> *Score: 42 → "Diversify your working zones to reduce flood-risk exposure. Consider increasing your savings wallet to ₹15/day to build a stronger buffer."*

**Business Value:**  
Workers who see their score improve stay longer on the platform. Opens future pathway to **preferential insurance rates** and **micro-credit products** based on demonstrated financial discipline.

---

### 9. Micro-Savings Wallet

**Problem Solved:** Workers cannot afford coverage during low-earning weeks, and have no savings infrastructure calibrated to their income pattern.

**What It Does:**
- Workers set aside small daily/weekly amounts from logged earnings
- Wallet balance pays insurance premiums first — ensures **uninterrupted coverage**
- Remaining balance acts as an **emergency buffer** during disruptions

**Implementation:**
- **Ledger system** in PostgreSQL — wallet record per worker with running balance
- **Auto-deduction rules** — configurable sweep from logged earnings (e.g., ₹10/day)
- **Premium auto-pay** — deducted from wallet, eliminating missed payments
- Phase 3: Connect to **UPI recurring payment infrastructure** for real money rails

**Business Value:**  
Workers with wallet balances are **lower churn risk** (active financial stake). Creates pathway to broader fintech products (savings goals, credit scoring, lending).

---

### 10. Cross-Platform Work Optimizer

**Problem Solved:** Workers don't know which delivery *segment* (food, grocery, hyperlocal) is most productive at any given moment.

**What It Does:**
Surfaces **segment-level demand intelligence** without naming specific platforms:

> *"Grocery delivery demand is currently higher than food delivery in your zone."*

**Critical Design Decision:** The optimizer operates at the **category level**, not the platform level. It never names Swiggy, Zepto, or any specific app — maintaining platform-neutral positioning.

**Implementation:**
- Rule-based demand simulation engine
- Inputs: time of day, weather, day of week
- Output: Segment-level demand indicators (bar chart on dashboard)
- No actual platform API integration required

---

### 11. Visual Risk Heatmap

**Problem Solved:** Workers have no spatial understanding of where it's safe and profitable to operate.

**What It Does:**
Interactive map overlay showing real-time disruption risk per micro-zone:

| Color | Meaning |
|-------|---------|
| Green | Low risk, high demand — optimal working zone |
| Amber | Moderate risk — work with awareness |
| Red | High risk / active disruption — avoid or expect coverage |

**Implementation:**

| Phase | Data Source |
|-------|-----------|
| Phase 1 | Static mock data for demo |
| Phase 2 | Live OpenWeather + AQICN APIs |
| Phase 3 | Real-time claim data overlay showing actual disruption impact |

**Tech Stack:** Mapbox SDK · H3 hexagonal grid rendering · REST API (10-min refresh cycle)

---

### 12. Insurer & Admin Analytics Dashboard

**Problem Solved:** Insurance partners and investors need real-time visibility into platform financial health and risk exposure.

**Key Metrics Displayed:**
- Active policies & total premiums collected
- Total payouts disbursed & **loss ratios** by zone and time period
- Active fraud flags & investigation status
- **Predictive analytics** — next-week claims estimate based on weather forecasts

**Tech Stack:** React.js · Recharts (charting) · WebSockets (real-time) · PostgreSQL analytics backend

---

## Adversarial Defense & Anti-Spoofing Engine

### The Threat Model

> *A coordinated syndicate of 500 workers using GPS spoofing and encrypted messaging to fake disruption-zone presence has drained a competitor's liquidity pool.*

**Core Principle:** No single data point can be trusted in isolation. GigShield uses **exponentially compounding multi-signal verification**.

### Three Truth Layers

```
┌────────────────────────────────────────────────────────┐
│  ENVIRONMENTAL TRUTH                                    │
│  "Did a real disruption actually occur?"                │
│  Sources: OpenWeather • IMD Alerts • AQICN • Traffic   │
├────────────────────────────────────────────────────────┤
│  LOCATION INTEGRITY                                     │
│  "Was the worker actually in the disruption zone?"      │
│  Sources: GPS trail (60–120 min history) • Cell tower  │
│  data • Wi-Fi triangulation • Movement consistency      │
├────────────────────────────────────────────────────────┤
│  ACTIVITY TRUTH                                         │
│  "Did the disruption actually cause the inactivity?"    │
│  Sources: App activity logs • Delivery history •        │
│  Battery/navigation patterns • Inactivity correlation   │
└────────────────────────────────────────────────────────┘
```

### Claim Confidence Scoring (100-Point System)

| Signal | Data Source | Weight |
|--------|-----------|--------|
| Environmental disruption confirmed | Weather API, IMD, AQICN | **30 pts** |
| Location inside disruption zone | GPS + movement pattern consistency | **25 pts** |
| Prior activity coherent (was working) | App logs, delivery history | **20 pts** |
| Inactivity onset correlated with trigger | Timestamp correlation analysis | **15 pts** |
| Clean device & network profile | Device ID, IP, VPN detection | **10 pts** |

| Score Range | Action |
|-------------|--------|
| **>= 80** | Auto-approved — payout processed immediately |
| **50–79** | Soft review — one additional verification step requested |
| **< 50** | Rejected — transparent explanation + appeal process provided |

### Coordinated Fraud Ring Detection

| Signal | What It Catches |
|--------|----------------|
| **Synchronized claim timing** | Ring members triggered simultaneously from a Telegram signal → statistically abnormal low variance in claim timestamps |
| **Device & network clustering** | Multiple accounts sharing device IDs, OS versions, or IP ranges → single-location operation |
| **Behavioral homogeneity** | Previously unconnected workers suddenly exhibiting matching activity patterns → trained syndicate behavior |

### Protecting Honest Workers

- **Progressive Trust:** Workers with 4+ weeks of clean history get reduced verification thresholds
- **Soft Flagging:** Never outright rejection first — request additional verification via non-accusatory notification
- **Explainable Decisions:** Every declined claim includes human-readable reasoning + appeal pathway

---

## Financial Architecture & Sustainability

### Premium Pool Allocation

```
Weekly Premium Collection
         │
         ├──► [60%] CLAIMS RESERVE
         │     Highly liquid instruments
         │     Accessible within 24 hours
         │     Covers expected claims + 30% buffer
         │
         ├──► [25%] OPERATIONS FUND
         │     Infrastructure, APIs, support, development
         │     Managed separately from claims
         │
         └──► [15%] INVESTMENT CORPUS
               Short-duration debt funds, govt securities
               Generates returns on float (insurance industry model)
```

**Worked Example (weekly):**

| Metric | Value |
|--------|-------|
| Active policies | 10,000 |
| Average premium | ₹40 |
| **Total collected** | **₹4,00,000** |
| → Claims Reserve (60%) | ₹2,40,000 |
| → Operations Fund (25%) | ₹1,00,000 |
| → Investment Corpus (15%) | ₹60,000 |
| Expected claims (45% loss ratio) | ₹1,80,000 |
| **Weekly surplus** | **₹60,000** |

### Loss Ratio Management

- **Target range:** 55–65% (steady-state)
- Below 55% = premiums too high, suppresses adoption
- Above 70% = underpricing risk, trending toward insolvency
- **Primary lever:** Dynamic weekly premium adjustment based on risk engine predictions
- **Secondary lever:** Coverage cap at **70% of average weekly earnings**

### Liquidity Surge Protection

| Mechanism | Description |
|-----------|-------------|
| **Reinsurance** | Excess-of-loss coverage activating when aggregate claims exceed 85% of Claims Reserve |
| **Geographic Diversification** | Multi-city expansion decorrelates disruption events |
| **Payout Smoothing** | Spread payouts over 24–48 hours during surge events to reduce peak liquidity demand |

### Revenue Roadmap

| Phase 1–2 (Months 1–12) | Phase 3+ (Scale) |
|---------------------------|-------------------|
| Free/subsidized premiums for early adopters | Premium margin as primary revenue |
| Focus on DAU through dashboard & alerts | Platform partnership fees (Zomato, Swiggy, Zepto) |
| Collect data to train ML models | B2B analytics products for platforms & insurers |
| Build trust via word-of-mouth network | Micro-credit products based on stability scores |
| Loss acceptable — funded by investment | Premium tier subscriptions for advanced features |

**Sustainable Scale Target (Year 2):** 100K active policies × ₹45 avg premium × 60% loss ratio = **₹18L/week revenue**

---

## Technology Stack & Architecture

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Mobile Frontend** | React Native / Flutter | Cross-platform worker app with offline-capable UI |
| **Admin Dashboard** | React.js, Recharts, WebSockets | Real-time insurer & operations analytics |
| **API Backend** | FastAPI (Python), Node.js | Core business logic & service orchestration |
| **ML & AI** | Python, scikit-learn, XGBoost, Prophet, Pandas | Risk scoring, premium calc, fraud detection, forecasting |
| **Primary Database** | PostgreSQL + PostGIS | Worker data, policies, claims, geospatial zone data |
| **Session & Cache** | Redis | Fast session management, fraud signal caching |
| **Task Queue** | Celery + Redis broker | Async claim processing & trigger evaluation |
| **Geospatial** | H3 (Uber Hex Grid), Mapbox SDK | Zone segmentation & risk heatmap rendering |
| **Push Notifications** | Firebase Cloud Messaging (FCM) | Early warnings, payout confirmations |
| **Payments** | Razorpay Test Mode, UPI Sandbox | Mock payout processing (Phase 2/3) |
| **External APIs** | OpenWeather, AQICN, IMD, Google Maps | Real-time environmental & civic disruption data |
| **DevOps** | Docker, GitHub Actions, CI/CD | Containerized deployment & automated testing |

### System Architecture Diagram

```
                    ┌─────────────────────────┐
                    │   Mobile App (Flutter)   │
                    │   Worker Dashboard UI    │
                    └────────────┬────────────┘
                                 │ REST / WebSocket
                    ┌────────────▼────────────┐
                    │   API Gateway (FastAPI)  │
                    │   + Node.js Services     │
                    └─┬──────┬──────┬────────┘
                      │      │      │
         ┌────────────▼┐  ┌──▼────┐ │  ┌──────────────┐
         │  Insurance   │  │ ML    │ │  │ Fraud Engine  │
         │  Engine      │  │Engine │ │  │ (Multi-Signal │
         │  (FastAPI)   │  │(Py)   │ │  │  Validation)  │
         └──────┬───────┘  └──┬────┘ │  └──────┬───────┘
                │             │      │         │
         ┌──────▼─────────────▼──────▼─────────▼───────┐
         │           PostgreSQL + PostGIS                │
         │    Workers | Policies | Claims | Zones        │
         └──────────────────┬──────────────────────────┘
                            │
                ┌───────────▼───────────┐
                │   Redis + Celery      │
                │   Task Queue & Cache  │
                └───────────┬───────────┘
                            │
              ┌─────────────▼─────────────┐
              │     External APIs          │
              │  OpenWeather │ AQICN │ IMD │
              │  Google Maps │ Razorpay    │
              └───────────────────────────┘
```

---

## AI & Machine Learning Architecture

GigShield relies on an ensemble of specialized machine learning models rather than a single monolithic AI. This architecture ensures high-performance, domain-specific intelligence for earnings predictions, risk assessment, and fraud detection.

### 1. Data Pipeline & Feature Engineering
Before training, raw data flows through our preprocessing pipelines (`backend/ai/pipelines/`):
- **Data Ingestion:** We aggregate multi-modal data including environmental inputs (OpenWeather, IMD, AQICN APIs), geospatial coordinates, and worker activity logs.
- **Spatial Indexing:** Uber's **H3 Hexagonal Grid** system translates raw coordinates into standardized `micro-zones` for spatial aggregations.
- **Feature Engineering:** We handle time-series encoding (cyclic features for time/day), missing value imputation, and correlation clustering to feed clean tensors into our models.

### 2. Core Algorithms & Training Modules
We train five specialized models, defined in `backend/ai/training/`:

#### A. Earnings Boost Engine (Regression)
- **Algorithm:** **XGBoost / LightGBM** (via scikit-learn)
- **How it works:** Predicts zone-level earnings potential to generate actionable routing recommendations.
- **Training:** Trained on historical platform earnings, weather, and order density. Gradient boosting builds sequential decision trees to minimize prediction errors, excelling at tabular numerical data.

#### B. Disruptive Risk Forecast Model (Time-Series)
- **Algorithm:** **Meta's Prophet**
- **How it works:** Forecasts structural disruptions (e.g., monsoon impact) 12-72 hours in advance to provide early warnings.
- **Training:** Learns non-linear trends from historical disruption data, capturing daily, weekly, and seasonal seasonality.

#### C. Hyperlocal Zone Risk Engine (Clustering)
- **Algorithm:** **K-Means / DBSCAN Clustering** (scikit-learn)
- **How it works:** Groups geospatial H3 hexes with similar baseline disruption behaviors (terrain, drainage, traffic density) to establish dynamic 0-100 risk scores.

#### D. Fraud & Anomaly Detection (Classification)
- **Algorithm:** **Isolation Forest / Random Forest Classifier**
- **How it works:** Generates the "Confidence Score" for automatic claims by detecting patterns common in GPS-spoofing or coordinated fraud rings.
- **Training:** Trained on synthetic adversarial data and anomaly parameters (e.g., synchronized claim timing, abnormal movement physics).

#### E. Dynamic Premium Pricing Model (Actuarial Regression)
- **Algorithm:** **Generalized Linear Models (GLMs) / Ridge Regression**
- **How it works:** Adjusts personalized weekly premiums based on a baseline risk profile plus dynamic weather/zone modifiers.

### 3. Model Deployment & Inference Execution
How the AI operates in real-time production:
1. **Model Persistence:** During offline training, optimized models are serialized and saved via `joblib` inside `backend/ai/saved_models/`.
2. **In‑Memory Inference:** Upon FastAPI startup, `model_loader.py` places these binaries into memory.
3. **Live Execution:** When a worker loads the dashboard, the API fetches live geospatial and weather data, constructs a rapid feature vector, and runs inference. Real-time predictions influence the dashboard, premium adjustments, and risk routing.

---

## Feature Feasibility Matrix

| Feature | Tech Stack | Feasibility | Phase | Business Impact |
|---------|-----------|-------------|-------|----------------|
| Unified Dashboard | React Native, Node.js, PostgreSQL | High | 2 | Daily active usage & user retention core |
| Earnings Boost Engine | Python, scikit-learn, OpenWeather | Medium | 2/3 | Direct income increase; #1 acquisition driver |
| Work Decision Engine | Python scoring, Firebase push | High | 2 | Reduces claims; builds habit & trust |
| Parametric Insurance | FastAPI, Celery, Redis, ML | High | 2 | Core revenue & protection product |
| Zero-Touch Claims | Event-driven, Razorpay mock | High | 2/3 | Defines UX differentiation; builds loyalty |
| Hyperlocal Risk Engine | H3, PostGIS, scikit-learn | Medium | 2/3 | Accurate pricing; reduces adverse selection |
| Predictive Forecast | Prophet, OpenWeather 5-day, FCM | Medium | 2/3 | Proactive UX; reduces claim shock |
| Income Stability Score | Python, weighted formula, PostgreSQL | High | 2 | Retention; future credit gateway |
| Micro-Savings Wallet | Ledger system, PostgreSQL | High | 2 | Premium continuity; reduces churn |
| Work Optimizer | Rule-based simulation, React | High | 2 | Worker empowerment; engagement anchor |
| Risk Heatmap | Mapbox SDK, H3, REST API | Medium | 2/3 | Visual impact; spatial intelligence demo |
| Admin Dashboard | React, WebSockets, Recharts | High | 3 | Partner confidence; investor reporting |

---

## Platform Partnership Strategy

### Why Zomato & Swiggy Would Partner

| Platform Pain Point | How GigShield Helps |
|--------------------|-------------------|
| **Workforce attrition** (largest cost driver) | Income protection + stability tools → workers stay longer |
| **Supply shortage during rain** (lost revenue) | Insured workers stay online in marginal conditions |
| **Regulatory & reputational pressure** | Partnership demonstrates worker welfare commitment |

### Conflict Mitigation
- Work Optimizer operates at **category level** (food vs. grocery), never names specific platforms
- GigShield cannot suppress orders, change routing, or affect any platform function
- Partnership model: platforms subsidize worker premiums as an **employment benefit** (analogous to employer health insurance)

---

## Scalability & Future Expansion

| Expansion Vector | Timeline | Key Adaptation |
|-----------------|----------|----------------|
| **Ride-hailing drivers** (Uber/Ola model) | Year 2 | Different trigger set: curfews, night safety, event-based demand |
| **Blue-collar gig workers** (construction, domestic) | Year 3 | Same parametric model; weather triggers directly applicable |
| **Geographic expansion** (Tier 1 → Tier 2 cities) | Year 2+ | Hyperlocal engine learns each city independently; seed with historical data |
| **Financial products** (micro-credit, lending) | Year 3+ | Based on Income Stability Score as creditworthiness proxy |

---

## Getting Started

### Prerequisites

- **Node.js** ≥ 18.x
- **Python** ≥ 3.10
- **PostgreSQL** ≥ 15 (with PostGIS extension)
- **Redis** ≥ 7.x
- **Docker** & **Docker Compose** (recommended)

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/gigshield.git
cd gigshield

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install

# Environment configuration
cp .env.example .env
# Edit .env with your API keys:
# - OPENWEATHER_API_KEY
# - AQICN_API_KEY
# - MAPBOX_ACCESS_TOKEN
# - RAZORPAY_KEY_ID (test mode)
# - FIREBASE_CONFIG

# Database setup
createdb gigshield
psql gigshield -c "CREATE EXTENSION postgis;"
python manage.py migrate

# Start Redis
redis-server

# Start Celery worker
celery -A gigshield worker --loglevel=info

# Start the backend
uvicorn main:app --reload --port 8000

# Start the frontend (in another terminal)
cd frontend
npm run dev
```

### Docker Quick Start

```bash
docker-compose up --build
```

---

## Project Structure

```
gigshield/
├── backend/
│   ├── api/                    # FastAPI route handlers
│   │   ├── dashboard.py        # Unified dashboard endpoints
│   │   ├── insurance.py        # Premium calc & policy management
│   │   ├── claims.py           # Zero-touch claim processing
│   │   ├── risk.py             # Hyperlocal risk scoring
│   │   ├── earnings.py         # Boost engine recommendations
│   │   ├── wallet.py           # Micro-savings wallet
│   │   └── admin.py            # Admin analytics endpoints
│   ├── engine/
│   │   ├── parametric.py       # Parametric trigger monitoring
│   │   ├── premium_calc.py     # Dynamic premium calculation
│   │   ├── decision_engine.py  # Work decision scoring
│   │   ├── boost_engine.py     # Earnings intelligence ML model
│   │   ├── risk_engine.py      # Hyperlocal risk scoring (H3)
│   │   └── forecast.py         # Prophet-based risk forecasting
│   ├── fraud/
│   │   ├── validator.py        # Multi-signal claim validation
│   │   ├── confidence.py       # 100-point confidence scoring
│   │   ├── ring_detector.py    # Coordinated fraud ring detection
│   │   └── trust_manager.py    # Progressive trust system
│   ├── models/                 # SQLAlchemy/Django ORM models
│   ├── tasks/                  # Celery async tasks
│   ├── services/               # External API integrations
│   │   ├── weather.py          # OpenWeather API client
│   │   ├── aqi.py              # AQICN API client
│   │   ├── imd.py              # IMD flood alerts client
│   │   └── payments.py         # Razorpay/UPI integration
│   ├── utils/                  # Shared utilities
│   ├── main.py                 # FastAPI application entry point
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── screens/            # Mobile app screens
│   │   ├── components/         # Reusable UI components
│   │   ├── services/           # API communication layer
│   │   └── utils/              # Frontend utilities
│   └── package.json
├── admin-dashboard/
│   ├── src/
│   │   ├── pages/              # Admin dashboard pages
│   │   ├── components/         # Charts, tables, maps
│   │   └── hooks/              # WebSocket & data hooks
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## API Documentation

Once the backend is running, access the interactive API docs at:

- **Swagger UI:** `http://localhost:8000/docs`
- **ReDoc:** `http://localhost:8000/redoc`

### Key Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/v1/dashboard/{worker_id}` | Unified earnings dashboard data |
| `GET` | `/api/v1/boost/{worker_id}` | Earnings boost recommendations |
| `GET` | `/api/v1/decision/{worker_id}` | Work decision score (GO/CAUTION/STAY) |
| `GET` | `/api/v1/insurance/premium/{worker_id}` | Current premium calculation |
| `POST` | `/api/v1/insurance/subscribe` | Subscribe to weekly coverage |
| `GET` | `/api/v1/claims/{worker_id}` | Claim history and status |
| `GET` | `/api/v1/risk/heatmap/{city}` | Zone-level risk heatmap data |
| `GET` | `/api/v1/risk/forecast/{zone_id}` | 7-day risk forecast |
| `GET` | `/api/v1/stability/{worker_id}` | Income stability score |
| `GET` | `/api/v1/wallet/{worker_id}` | Wallet balance and transactions |
| `POST` | `/api/v1/wallet/deposit` | Add to savings wallet |
| `GET` | `/api/v1/admin/analytics` | Platform-wide analytics (admin only) |

---

## Contributing

We welcome contributions! Please see our contributing guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <strong>GigShield</strong> — <em>We don't ask workers to understand insurance. We ask them to trust that when the rain falls and they cannot work, GigShield has them covered.</em>
</p>
