# WMS Pro - Implementation Plan

## Technology Stack Summary

| Layer | Technology |
|-------|------------|
| Backend | Python 3.11+ / FastAPI |
| Frontend | React 18 + TypeScript + Vite |
| Mobile | Flutter (iOS, Android, RF Scanners) |
| Database | PostgreSQL 15+ (Schema-based multi-tenancy + JSONB) |
| Cache | Redis |
| Message Broker | Apache Kafka |
| Search | Elasticsearch (inventory search, analytics) |
| Auth | Keycloak (SSO, SAML2, OAuth2, Azure AD) |
| Deployment | Hybrid: Cloud (AWS/Azure) + On-prem Middleware |

---

## Project Structure

```
wmspro/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API routes (v1)
│   │   ├── core/              # Config, security, dependencies
│   │   ├── models/            # SQLAlchemy models
│   │   ├── schemas/           # Pydantic schemas
│   │   ├── services/          # Business logic
│   │   ├── repositories/      # Data access layer
│   │   ├── integrations/      # ERP adapters
│   │   └── workers/           # Kafka consumers, background tasks
│   ├── alembic/               # Database migrations
│   ├── tests/
│   └── requirements.txt
├── frontend/                   # React Frontend
│   ├── src/
│   │   ├── components/        # Reusable UI components
│   │   ├── pages/             # Route pages
│   │   ├── hooks/             # Custom React hooks
│   │   ├── store/             # Zustand state management
│   │   ├── api/               # API client (React Query)
│   │   └── types/             # TypeScript types
│   └── package.json
├── mobile/                     # Flutter Mobile App
│   ├── lib/
│   │   ├── screens/
│   │   ├── widgets/
│   │   ├── providers/         # Riverpod state
│   │   ├── services/
│   │   └── models/
│   └── pubspec.yaml
├── middleware/                 # On-Prem ERP Connector
│   ├── connectors/            # SAP, Oracle, Dynamics adapters
│   ├── mappers/               # Field mapping engine
│   └── kafka/                 # Message handlers
├── infrastructure/             # IaC & DevOps
│   ├── terraform/
│   ├── kubernetes/
│   └── docker/
└── docs/
```

---

## Implementation Phases

### Phase 1: Foundation (Modules 1, 13, 14)
**Core Platform + System Admin + Developer API**

#### 1.1 Backend Foundation
- [ ] FastAPI project setup with async support
- [ ] PostgreSQL connection with asyncpg + SQLAlchemy 2.0
- [ ] Schema-based multi-tenancy middleware
- [ ] Alembic migrations with per-tenant schema support
- [ ] Redis caching layer
- [ ] Keycloak integration (SSO, RBAC)
- [ ] Audit logging system (all actions tracked)
- [ ] API versioning (v1)
- [ ] OpenAPI documentation

#### 1.2 Database Schema - Core Tables
```sql
-- Tenant Management (public schema)
tenants, tenant_settings, tenant_users

-- Per-tenant schema template
users, roles, permissions, user_roles
audit_logs
system_config, custom_field_definitions
```

#### 1.3 Frontend Foundation
- [ ] React + Vite + TypeScript setup
- [ ] TailwindCSS + Headless UI component library
- [ ] React Query for API state management
- [ ] Zustand for client state
- [ ] React Router v6 routing
- [ ] Auth flow (login, SSO redirect, token refresh)
- [ ] Tenant context provider
- [ ] Base layout (sidebar, header, breadcrumbs)
- [ ] Custom field renderer (dynamic forms)

#### 1.4 Developer API
- [ ] REST API with comprehensive endpoints
- [ ] Webhook system (event subscriptions)
- [ ] WebSocket server (real-time task updates)
- [ ] Service account management
- [ ] API rate limiting
- [ ] SDK documentation

---

### Phase 2: Master Data (Module 2)
**Warehouse Structure + Materials + Workforce**

#### 2.1 Database Models
```python
# Warehouse Structure
Warehouse, StorageLocation, StorageType, Zone, Aisle, Bin

# Material Master
Material, MaterialUOM, MaterialBatch, HandlingUnitTemplate

# Workforce
User, SkillProfile, Equipment, Device
```

#### 2.2 Features
- [ ] Warehouse hierarchy CRUD
- [ ] Bin management (fixed, dynamic, capacity constraints)
- [ ] Material master with UOM conversions
- [ ] Batch & serial number configuration
- [ ] Handling unit templates
- [ ] User skill profiles
- [ ] Equipment/device registry
- [ ] Import/export (Excel, CSV)
- [ ] Bulk operations

#### 2.3 UI Screens
- [ ] Warehouse structure tree view
- [ ] Bin matrix/grid view
- [ ] Material master list + detail
- [ ] User management
- [ ] Equipment tracking

---

### Phase 3: Inventory Management (Module 3)
**Stock Model + Visibility + Movements + Physical Inventory**

#### 3.1 Database Models
```python
# Stock
StockBalance, StockMovement, StockType, SpecialStockType

# Handling Units
HandlingUnit, HUItem, HUHistory

# Physical Inventory
PhysicalInventoryDocument, PICount, PIVariance
```

#### 3.2 Core Stock Engine
- [ ] Multi-dimensional stock tracking:
  - Plant → Sloc → Bin → Batch → HU
  - Stock types: Unrestricted, Blocked, Quality
  - Special stock: Customer (E), Consignment (K), Project (Q)
- [ ] Real-time stock calculations
- [ ] Stock reservation system
- [ ] Negative stock detection & alerts

#### 3.3 Stock Movements
- [ ] Bin-to-bin transfers
- [ ] Sloc transfers
- [ ] HU creation, moves, repack, split, merge
- [ ] Stock adjustments with reason codes
- [ ] Mass transfer (cart-based)
- [ ] Movement type configuration engine

#### 3.4 Physical Inventory
- [ ] Cycle counting (ABC classification)
- [ ] Annual physical inventory
- [ ] Ad-hoc counts
- [ ] Count variance workflow (approve/reject/recount)
- [ ] Adjustment posting

#### 3.5 UI Screens
- [ ] Stock overview dashboard
- [ ] Stock inquiry (multi-filter)
- [ ] Stock movement history
- [ ] HU management screen
- [ ] PI document management
- [ ] Count entry screen

---

### Phase 4: Inbound Management (Module 4)
**ASN + Receiving + Put-away**

#### 4.1 Database Models
```python
InboundDelivery, InboundDeliveryItem, InboundDeliveryStatus
ASN, ASNItem
GoodsReceipt, GRItem
DockAppointment
```

#### 4.2 Features
- [ ] ASN import (API, file upload)
- [ ] Inbound delivery management
- [ ] Dock appointment scheduling
- [ ] GR processing against:
  - Purchase orders
  - Inbound deliveries
  - Production orders
  - Subcontracting
- [ ] Check-in & staging workflow
- [ ] HU/pallet/case scanning
- [ ] Label printing (bin, HU, pallet)
- [ ] Exception handling (damaged, over/under, unexpected)

#### 4.3 Put-away Engine
- [ ] Strategy configuration:
  - Fixed bin
  - Next empty bin
  - Capacity-based
  - Zone-based
- [ ] Multi-level put-away (pallet → case → unit)
- [ ] Auto task generation
- [ ] Manual task assignment

#### 4.4 UI Screens
- [ ] Inbound delivery list
- [ ] Receiving workbench
- [ ] Dock scheduling calendar
- [ ] Put-away task queue

---

### Phase 5: Outbound Management (Module 5)
**Demand + Picking + Packing + Shipping**

#### 5.1 Database Models
```python
OutboundDelivery, OutboundDeliveryItem, OutboundStatus
Wave, WaveItem
PickTask, PackTask
Shipment, ShipmentItem, CarrierLabel
```

#### 5.2 Features
- [ ] Demand import (sales orders, STO, production)
- [ ] E-commerce order API integration
- [ ] Wave planning & creation
- [ ] Wave release rules

#### 5.3 Picking Engine
- [ ] Picking strategies:
  - Cluster picking
  - Batch picking
  - Zone picking
  - Wave picking
- [ ] Pick path optimization
- [ ] Auto task assignment
- [ ] Short pick handling

#### 5.4 Packing & Shipping
- [ ] Packing station UI
- [ ] Cartonization logic
- [ ] HU packing
- [ ] Shipping label generation
- [ ] Carrier integration (pluggable):
  - DHL, UPS, FedEx
  - EasyPost / ShipEngine abstraction
- [ ] PGI confirmation
- [ ] Load/seal confirmation

#### 5.5 UI Screens
- [ ] Outbound delivery list
- [ ] Wave management
- [ ] Pick queue
- [ ] Packing station
- [ ] Shipping workbench

---

### Phase 6: Warehouse Tasks Engine (Module 6)
**Task Types + Assignment + Execution**

#### 6.1 Database Models
```python
WarehouseTask, TaskType, TaskStatus, TaskPriority
TaskAssignment, TaskResult
TaskQueue, QueueRule
```

#### 6.2 Task Engine
- [ ] Task types: Pick, Putaway, Count, Transfer, Replenishment, Packing
- [ ] Task lifecycle management
- [ ] Priority queue system
- [ ] Auto-assignment engine:
  - User skills matching
  - Proximity calculation
  - Workload balancing
  - Performance history
- [ ] Manual assignment override
- [ ] Task execution tracking
- [ ] Result validation
- [ ] Photo/note attachments

#### 6.3 UI Screens
- [ ] Task queue dashboard
- [ ] Task assignment matrix
- [ ] Worker productivity view

---

### Phase 7: Replenishment & Slotting (Module 7)

#### 7.1 Database Models
```python
ReplenishmentRule, ReplenishmentTask
SlotConfiguration, SlotRecommendation
SKUVelocity
```

#### 7.2 Features
- [ ] Min/max replenishment rules
- [ ] Auto-generation of replenishment tasks
- [ ] Bulk → pick-face replenishment
- [ ] Slotting optimization engine:
  - SKU popularity analysis
  - Dimension-based assignment
  - Zone affinity
  - Velocity-based placement
- [ ] Re-slotting recommendations

---

### Phase 8: Mobile Application (Module 8)
**Flutter App for iOS, Android, RF Scanners**

#### 8.1 Core Features
- [ ] Authentication (SSO support)
- [ ] Warehouse/location selection
- [ ] Barcode/QR scanning (camera + hardware)
- [ ] Offline mode with sync engine
- [ ] Retry queue for failed operations

#### 8.2 Functional Modules
- [ ] Receiving workflow
- [ ] Put-away execution
- [ ] Picking execution
- [ ] Packing workflow
- [ ] Counting (cycle count, PI)
- [ ] Stock transfer
- [ ] HU management
- [ ] Stock inquiry

#### 8.3 Device Support
- [ ] iOS (iPhone, iPad)
- [ ] Android phones/tablets
- [ ] Zebra RF scanners
- [ ] Honeywell devices

---

### Phase 9: ERP Integration Framework (Module 9)
**Canonical Model + Multi-ERP Support**

#### 9.1 Canonical Data Model
```python
# Inbound Objects (ERP → WMS)
CanonicalMaterial
CanonicalInboundDelivery
CanonicalOutboundDelivery
CanonicalStockPosting

# Outbound Objects (WMS → ERP)
CanonicalGoodsReceipt
CanonicalGoodsIssue
CanonicalStockAdjustment
CanonicalHUUpdate
```

#### 9.2 Integration Flows
- [ ] Material master sync
- [ ] Plant/Sloc/Bin sync
- [ ] Inbound delivery sync
- [ ] Outbound delivery sync
- [ ] GR confirmation
- [ ] GI/PGI confirmation
- [ ] Stock adjustment posting
- [ ] Movement type mapping engine

#### 9.3 Movement Type Configuration
```python
MovementTypeConfig:
  - movement_type: str      # e.g., "101", "261", "311"
  - special_stock_type: str # E, K, Q, etc.
  - direction: enum         # IN, OUT, INTERNAL
  - reference_required: bool
  - ui_flow_type: str
  - posting_behavior: dict
```

---

### Phase 10: Middleware Connector (Module 10)
**On-Premise ERP Bridge**

#### 10.1 Architecture
```
[ERP] <--RFC/IDoc/OData--> [Middleware] <--Kafka--> [WMS Cloud]
```

#### 10.2 SAP Connectors
- [ ] RFC/BAPI connector (pyrfc)
- [ ] IDoc parser/generator
- [ ] OData client (S/4HANA)
- [ ] CPI/PI/PO proxy support

#### 10.3 Other ERP Connectors
- [ ] Oracle REST adapter
- [ ] Dynamics 365 adapter
- [ ] Generic REST/SOAP adapter

#### 10.4 Message Handling
- [ ] Kafka producer/consumer
- [ ] Guaranteed delivery
- [ ] Dead-letter queue (DLQ)
- [ ] Replay mechanism
- [ ] Schema versioning

#### 10.5 Mapping Engine
- [ ] Configurable field mapping
- [ ] Transform functions
- [ ] Validation rules
- [ ] Mapping UI

#### 10.6 Security
- [ ] mTLS authentication
- [ ] IP allowlisting
- [ ] Token-based auth with cloud

---

### Phase 11: AI Features (Module 11)
**Predictions + Optimization + Assistant**

#### 11.1 Infrastructure
- [ ] ML model serving (FastAPI + ONNX/TensorFlow Lite)
- [ ] Feature store (Redis/PostgreSQL)
- [ ] Training pipeline (optional: MLflow)

#### 11.2 AI Models
- [ ] Receiving workload prediction
- [ ] ASN anomaly detection
- [ ] Pick path optimization (TSP solver)
- [ ] Carton size prediction
- [ ] Replenishment forecasting
- [ ] Slow/fast mover detection
- [ ] Shrinkage anomaly detection
- [ ] Expiry prediction

#### 11.3 AI Assistant
- [ ] Natural language query interface
- [ ] LLM integration (OpenAI/Anthropic)
- [ ] Query → SQL translation
- [ ] Dashboard generation

---

### Phase 12: Analytics & Dashboards (Module 12)

#### 12.1 Data Pipeline
- [ ] Kafka → Elasticsearch ingestion
- [ ] Aggregation jobs (hourly, daily)
- [ ] Data warehouse tables

#### 12.2 Operational Dashboards
- [ ] Receiving rate per hour
- [ ] Put-away cycle time
- [ ] Picking productivity
- [ ] Order fulfillment rate
- [ ] Replenishment alerts

#### 12.3 Inventory Dashboards
- [ ] Inventory accuracy
- [ ] Stock aging analysis
- [ ] Stock value by location
- [ ] Cycle count backlog

#### 12.4 Predictive Dashboards
- [ ] Demand forecast
- [ ] Labor requirement prediction
- [ ] Space utilization projection

#### 12.5 Implementation
- [ ] Chart components (Recharts/Victory)
- [ ] Dashboard builder (drag-drop)
- [ ] Scheduled reports
- [ ] Export (PDF, Excel)

---

### Phase 13: Enterprise Features (Module 15)

- [ ] Multi-warehouse consolidation views
- [ ] 3PL billing module
- [ ] Cost allocation per task
- [ ] Labor management (time tracking, productivity)
- [ ] Workflow automation engine (rule builder)
- [ ] Document management (attachments, BOL, POD)

---

## Key Technical Decisions

### 1. Multi-Tenancy Implementation
```python
# Middleware for schema-based tenancy
class TenantMiddleware:
    async def __call__(self, request, call_next):
        tenant_id = extract_tenant(request)
        set_search_path(f"tenant_{tenant_id}")
        return await call_next(request)
```

### 2. Stock Calculation Engine
```python
# Real-time stock with materialized views + triggers
# OR event-sourced stock movements with CQRS
```

### 3. Task Queue Architecture
```
FastAPI → Kafka (tasks topic) → Task Workers → Redis (state) → WebSocket (UI updates)
```

### 4. ERP Adapter Pattern
```python
class ERPAdapter(ABC):
    @abstractmethod
    async def sync_materials(self) -> List[CanonicalMaterial]: ...

    @abstractmethod
    async def post_goods_receipt(self, gr: CanonicalGoodsReceipt) -> ERPResponse: ...

class SAPAdapter(ERPAdapter): ...
class OracleAdapter(ERPAdapter): ...
```

---

## Files to Create (Phase 1)

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry
│   ├── core/
│   │   ├── config.py           # Settings (pydantic-settings)
│   │   ├── database.py         # Async SQLAlchemy setup
│   │   ├── security.py         # JWT, password hashing
│   │   ├── tenancy.py          # Multi-tenant middleware
│   │   └── dependencies.py     # FastAPI dependencies
│   ├── models/
│   │   ├── base.py             # Base model with tenant_id
│   │   ├── tenant.py           # Tenant, TenantSettings
│   │   └── user.py             # User, Role, Permission
│   ├── schemas/
│   │   ├── tenant.py
│   │   └── user.py
│   ├── api/
│   │   └── v1/
│   │       ├── auth.py
│   │       ├── tenants.py
│   │       └── users.py
│   └── services/
│       ├── tenant_service.py
│       └── user_service.py
├── alembic/
│   └── versions/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml

frontend/
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── api/
│   │   └── client.ts           # Axios + React Query setup
│   ├── components/
│   │   └── ui/                 # Base components
│   ├── pages/
│   │   ├── Login.tsx
│   │   └── Dashboard.tsx
│   ├── store/
│   │   └── authStore.ts
│   └── types/
│       └── index.ts
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

---

## Next Steps

1. Start with **Phase 1: Foundation** - setting up the project structure, database, and core authentication
2. Establish CI/CD pipeline early
3. Set up development, staging, and production environments
