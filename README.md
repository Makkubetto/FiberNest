# 🌿 FiberNest

A full-stack e-commerce web application for selling eco-friendly coconut coir products made in the Philippines.

> **For educational purposes only, and no copyright infringement is intended.**

---

## 📋 Project Overview

FiberNest is a complete e-commerce platform built as a requirement under E-commerce course. It features a buyer-facing storefront and a seller dashboard, backed by a FastAPI REST API and a PostgreSQL database hosted on Supabase.

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React.js (via CDN), Tailwind CSS (via CDN) |
| Backend | FastAPI (Python 3.11) |
| Database | PostgreSQL (Supabase) |
| Auth | JWT (python-jose + passlib bcrypt) |
| ORM | SQLAlchemy |

---

## 📁 Folder Structure

```
FiberNest/
├── frontend/
│   ├── api.js                        ← Shared API config & cart utilities
│   ├── buyer/
│   │   ├── index.html                ← Home page
│   │   ├── login.html                ← Buyer login
│   │   ├── register.html             ← Registration
│   │   ├── storefront.html           ← Featured products
│   │   ├── products.html             ← All products
│   │   ├── cart.html                 ← Shopping cart
│   │   ├── checkout.html             ← Checkout (3-step)
│   │   ├── transactions.html         ← Order history
│   │   └── profile.html              ← User profile
│   └── seller/
│       ├── seller-layout.js          ← Shared sidebar layout
│       ├── seller-login.html         ← Seller login
│       ├── seller-dashboard.html     ← Dashboard overview
│       ├── seller-storefront.html    ← Manage storefront
│       ├── seller-inventory.html     ← Manage products
│       └── seller-reports.html       ← Sales & inventory reports
│
└── backend/
    ├── app/
    │   ├── main.py                   ← FastAPI entry point
    │   ├── config.py                 ← Environment settings
    │   ├── database.py               ← SQLAlchemy engine & session
    │   ├── models/                   ← Database models
    │   │   ├── user.py
    │   │   ├── product.py
    │   │   ├── order.py
    │   │   └── storefront.py
    │   ├── schemas/                  ← Pydantic schemas
    │   │   ├── user.py
    │   │   ├── product.py
    │   │   ├── order.py
    │   │   └── storefront.py
    │   ├── routers/                  ← API route handlers
    │   │   ├── auth.py
    │   │   ├── users.py
    │   │   ├── products.py
    │   │   ├── orders.py
    │   │   ├── storefront.py
    │   │   └── seller.py
    │   └── utils/
    │       ├── auth.py               ← JWT & password hashing
    │       └── deps.py               ← Dependency injection
    ├── .env                          ← Environment variables (DO NOT COMMIT)
    ├── requirements.txt
    └── venv/                         ← Virtual environment (DO NOT COMMIT)
```

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.11
- A Supabase account (or local PostgreSQL)

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/FiberNest.git
cd FiberNest
```

### 2. Set up the backend
```bash
cd backend
py -3.11 -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Create the `.env` file
Create a `.env` file inside the `backend/` folder:
```env
DATABASE_URL=postgresql://postgres:yourpassword@yourhost:5432/postgres
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

> Ask the project lead for the Supabase credentials.

### 4. Run the backend
```bash
py -3.11 -m uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`
Swagger docs at `http://localhost:8000/docs`

### 5. Open the frontend
No build step needed. Just open the HTML files directly in your browser:
```
frontend/buyer/index.html
```

Or use VS Code Live Server extension for best results.

---

## 🔌 API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Register new user | None |
| POST | `/auth/login` | Login (returns JWT) | None |
| GET | `/users/me` | Get current user | Buyer/Seller |
| PUT | `/users/me` | Update profile | Buyer/Seller |
| GET | `/products` | Get all products | None |
| POST | `/products` | Create product | Seller |
| PUT | `/products/{id}` | Update product | Seller |
| DELETE | `/products/{id}` | Delete product | Seller |
| POST | `/orders` | Place an order | Buyer |
| GET | `/orders/my` | Get my orders | Buyer |
| GET | `/orders` | Get all orders | Seller |
| GET | `/storefront` | Get storefront config | None |
| PUT | `/storefront` | Update storefront | Seller |
| GET | `/seller/stats` | Dashboard stats | Seller |
| GET | `/seller/reports` | Sales reports | Seller |
| GET | `/seller/inventory-report` | Inventory report | Seller |

---

## 👥 Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Buyer | buyer@fibernest.ph | password123 |
| Seller | seller@fibernest.ph | seller123 |

---

## 🚫 .gitignore

Make sure these are in your `.gitignore` before pushing:
```
venv/
__pycache__/
*.pyc
.env
*.egg-info/
```

---

## 👨‍💻 Group Members

- *(Mapoy, Pauline Erika)*
- *(Ibarrientos, Forest Red)*
- *(Julius De leon)*
- *(Batac, John Gabriel)*


---

## 📝 Notes

- The frontend uses React and Tailwind via CDN — no `npm install` or build step required.
- All pages are standalone `.html` files that communicate with the FastAPI backend via `fetch()`.
- The cart is stored in `localStorage` for guest users and synced to the backend on checkout.
- Tables are auto-created on first run via `Base.metadata.create_all()` in `main.py`.