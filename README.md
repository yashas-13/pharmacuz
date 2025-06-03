# Pharmacuz

dqdva9-codex/summarize-pharmacuz-project-overview
Pharmacuz is a sample repository to demonstrate a pharmaceutical distribution and inventory management system. The backend now exposes basic authentication with role-based APIs for different users.

## Structure

- `backend/` – Flask application exposing authenticated endpoints for manufacturer, CFA, and super stockist roles.
=======
Pharmacuz is a sample repository to demonstrate a pharmaceutical distribution and inventory management system. This repository currently contains a simple Flask backend skeleton and placeholder directories for a frontend implementation.

## Structure

- `backend/` – contains a basic Flask application with placeholder endpoints for products and batches.
 main
- `frontend/` – reserved for the progressive web app (PWA) implementation.

## Getting Started

1. **Set up a Python environment**:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   python app.py
   ```
   The server will run on `http://localhost:5000`.

dqdva9-codex/summarize-pharmacuz-project-overview
2. **Authentication**:
   Send a POST request to `/login` with JSON body `{"username": "admin", "password": "adminpass"}` (or other demo users) to receive a token.
   Use this token in the `Authorization` header (`Bearer <token>`) for subsequent requests.

3. **Role Endpoints**:
   - `POST /manufacturer/products` – create a product (manufacturer role)
   - `GET /manufacturer/products` – list products
   - `POST /cfa/grn` – record goods receipt note (CFA role)
   - `GET /cfa/grn` – list GRNs
   - `POST /super_stockist/requests` – create stock request (super stockist role)
   - `GET /super_stockist/requests` – list requests

These endpoints illustrate how RBAC can be implemented. The data is stored in memory for demonstration purposes.
=======
2. **Explore**: The app exposes simple JSON-based routes to demonstrate inventory data retrieval and batch creation.

Further development will include full CRUD operations, authentication, role-based access, and offline-ready capabilities for the PWA.
main
