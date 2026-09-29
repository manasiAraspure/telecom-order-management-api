# Telecom Order Management API

A backend REST API for managing fiber broadband subscribers and service orders, built with FastAPI. Simulates core workflows from telecom BSS (Business Support Systems) — subscriber management, order lifecycle tracking, and service feasibility checks — inspired by real-world telecom provisioning systems.

🔗 **Live Demo:** [telecom-order-api.onrender.com/docs](https://telecom-order-api.onrender.com/docs)

## Features

- **Full CRUD** for Subscribers and Orders
- **Order lifecycle management** with status transitions (`REQUESTED` → `FEASIBILITY_CHECKED` → `APPROVED`/`REJECTED` → `ACTIVATED`)
- **Feasibility check** — simulates an external API integration to determine service availability based on subscriber coordinates
- **JWT authentication** — secures create/delete operations with token-based auth
- **Layered architecture** — routers, services, models, and schemas kept separate for maintainability and testability
- **Global error handling** — unexpected errors are logged in full detail server-side, while clients receive safe, generic error messages
- **Auto-generated interactive API docs** via Swagger UI

## Tech Stack

- **FastAPI** — web framework
- **SQLAlchemy** — ORM
- **Pydantic** — request/response validation
- **SQLite** — database (designed to be swappable to MySQL/PostgreSQL via SQLAlchemy)
- **JWT (python-jose)** + **passlib/bcrypt** — authentication
- **Uvicorn** — ASGI server

## Project Structure

app/
├── main.py # App entry point, router registration, global error handler
├── database.py # DB connection and session management
├── models/ # SQLAlchemy models (database table definitions)
├── schemas/ # Pydantic schemas (API request/response shapes)
├── services/ # Business logic layer
└── routers/ # API endpoint definitions


## Getting Started

### Prerequisites
- Python 3.10+

### Setup

```bash
# Clone the repo
git clone https://github.com/manasiAraspure/telecom-order-management-api.git
cd telecom-order-management-api

# Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Create a .env file in the project root with:
# JWT_SECRET_KEY=your-secret-key-here

# Run the server
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`
Interactive docs (Swagger UI): `http://127.0.0.1:8000/docs`


## API Overview

### Auth
| Endpoint         | Method | Description               | Auth Required  |
|------------------|--------|---------------------------|----------------|
| `/auth/register` | POST   | Register a new user       | No             |
| `/auth/login`    | POST   | Login and receive a JWT   | No             |

### Subscribers
| Endpoint                | Method | Description               | Auth Required  |
|-------------------------|--------|---------------------------|----------------|
| `/subscribers/`         | POST   | Create a subscriber       | No             |
| `/subscribers/`         | GET    | List all subscribers      | No             |
| `/subscribers/{id}`     | GET    | Get a subscriber by ID    | No             |
| `/subscribers/{id}`     | DELETE | Delete a subscriber       | Yes            |

### Orders
| Endpoint                           | Method | Description                        | Auth Required  |
|------------------------------------|--------|------------------------------------|----------------|
| `/orders/`                         | POST   | Create an order                    | Yes            |
| `/orders/`                         | GET    | List all orders                    | No             |
| `/orders/{id}`                     | GET    | Get an order by ID                 | No             |
| `/orders/{id}`                     | PATCH  | Update an order                    | No             |
| `/orders/{id}`                     | DELETE | Delete an order                    | Yes            |
| `/orders/{id}/check-feasibility`   | POST   | Run feasibility check for an order | No             |


## Design Decisions

- **Mock feasibility service**: simulates an external API call (including realistic latency) rather than calling a real paid service, keeping the demo reliable. The function is isolated so swapping in a real API is a contained change — no other code needs to know or care.
- **Blocking subscriber deletion with existing orders**: rather than cascading deletes (which could silently destroy order history) or crashing, the API returns a clear `400` error, preserving data integrity.
- **PATCH over PUT for order updates**: partial updates only modify the fields explicitly provided, preventing accidental data loss.

## Future Improvements

- Swap the mock feasibility service for a real geocoding + coverage API
- Add role-based access control (admin vs staff permissions)
- Add automated tests (pytest) and CI (GitHub Actions)
- Migrate from SQLite to PostgreSQL/MySQL for production use
- Add Alembic for database migrations


## Author

Manasi — Python Backend Developer
GitHub: [github.com/manasiAraspure](https://github.com/manasiAraspure)
