# Pharmacuz

Pharmacuz is a sample repository to demonstrate a pharmaceutical distribution and inventory management system. This repository currently contains a simple Flask backend skeleton and placeholder directories for a frontend implementation.

## Structure

- `backend/` – contains a basic Flask application with placeholder endpoints for products and batches.
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

2. **Explore**: The app exposes simple JSON-based routes to demonstrate inventory data retrieval and batch creation.

Further development will include full CRUD operations, authentication, role-based access, and offline-ready capabilities for the PWA.
