# WMS Pro - Warehouse Management System

A modern, multi-tenant SaaS Warehouse Management System built with FastAPI and React.

## Tech Stack

### Backend
- **Framework**: FastAPI (Python 3.11+)
- **Database**: PostgreSQL 15+ (schema-based multi-tenancy)
- **Cache**: Redis
- **Message Broker**: Apache Kafka
- **Auth**: JWT with Keycloak SSO support

### Frontend
- **Framework**: React 18 + TypeScript
- **Build Tool**: Vite
- **Styling**: TailwindCSS
- **State Management**: Zustand + React Query
- **Forms**: React Hook Form

### Infrastructure
- **Containerization**: Docker + Docker Compose
- **Database Migrations**: Alembic

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Node.js 20+ (for local frontend dev)
- Python 3.11+ (for local backend dev)

### Running with Docker

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Services will be available at:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Local Development

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Start dev server
npm run dev
```

## Project Structure

```
wmspro/
├── backend/                 # FastAPI Backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Config, security, database
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   └── services/       # Business logic
│   ├── alembic/            # Migrations
│   └── tests/
├── frontend/               # React Frontend
│   ├── src/
│   │   ├── api/           # API client
│   │   ├── components/    # UI components
│   │   ├── pages/         # Route pages
│   │   ├── store/         # Zustand stores
│   │   └── types/         # TypeScript types
│   └── public/
├── middleware/             # On-prem ERP connector
├── infrastructure/         # Docker, Terraform, K8s
└── docs/                   # Documentation
```

## API Documentation

Once the backend is running, visit:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Features

### Phase 1 (Current)
- [x] Multi-tenant architecture
- [x] User authentication (JWT)
- [x] Role-based access control
- [x] Tenant management
- [x] User management

### Coming Soon
- [ ] Warehouse master data
- [ ] Inventory management
- [ ] Inbound processing
- [ ] Outbound processing
- [ ] Task management
- [ ] Mobile app (Flutter)
- [ ] ERP integration

## Environment Variables

### Backend (.env)

```env
# Database
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_USER=wms
POSTGRES_PASSWORD=wms_secret
POSTGRES_DB=wmsdb

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# Security
SECRET_KEY=your-secret-key-min-32-chars
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend

```env
VITE_API_URL=http://localhost:8000
```

## License

Proprietary - All rights reserved

## Author

Prakash + Claude (AI Assistant)
