# Pharmacuz

Pharmacuz is a sample repository to demonstrate a pharmaceutical distribution and inventory management system. The backend exposes basic authentication with role-based APIs for different users.

## Structure

- `backend/` – Flask application exposing authenticated endpoints for manufacturer, CFA, and super stockist roles.
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
   Visit this URL in your browser to see the login page served from
 f2igg8-codex/modify-get_user_from_token-to-return-username-and-role
  
 main

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

 f2igg8-codex/modify-get_user_from_token-to-return-username-and-role

 main
 main
Each role is presented with its own dashboard when logging in:
   - **Manufacturer** – manage products you supply.
   - **CFA** – record and review goods receipt notes.
   - **Super Stockist** – create and view stock requests.

These endpoints and dashboards illustrate how RBAC can be implemented. The data is stored in memory for demonstration purposes.
 f2igg8-codex/modify-get_user_from_token-to-return-username-and-role


These endpoints illustrate how RBAC can be implemented. The data is stored in memory for demonstration purposes.
 main
 main
 main

Further development will include full CRUD operations, authentication, role-based access, and offline-ready capabilities for the PWA.
