# Sync Plan for Pharmacuz

This document outlines checks performed on the repo and a short plan to keep the frontend, backend, and database in sync for the remaining work.

## Checks Performed

- Installed backend dependencies with `pip install -r backend/requirements.txt`.
- Started the Flask server via `python main.py` (port 8001 due to 8000 conflict).
- Verified `/api/products` returns data when authenticated.
- Inspected `pharmacuz.db` to ensure tables match SQLAlchemy models.
- Reviewed frontend HTML files for fetch endpoints pointing to `/api/...` routes.

No schema mismatches or obvious routing errors were found.

## Feature Review

### Manufacturer
- Tested `/api/manufacturer/products`, `/api/manufacturer/batches`,
  `/api/manufacturer/pack-configs` and `/api/manufacturer/users` using a
  manufacturer token. All endpoints responded with JSON and no errors.
- Frontend `manufacterer.html` calls these APIs. Charts are placeholders but
  CRUD operations work when triggered.

### CFA
- Verified `/api/cfa/grn` for creating and listing GRNs with a CFA token.
- `cfa.html` fetches products, batches, pricing, orders and inventory through the
  common API prefixes; responses were empty arrays on a fresh database but the
  routes executed successfully.

### Super Stockist
- Confirmed `/api/super_stockist/requests` works for the super-stockist role.
- `stockist.html` interacts with orders and inventory endpoints and was able to
  retrieve empty JSON lists during testing.

### Sync Endpoint
- `/api/sync/erp` aggregates orders and inventory. Tested successfully with an
  authenticated request returning empty arrays.

Overall the Flask server and SQLite database operate correctly and the
frontends store JWT tokens to access the APIs.

### Gaps Observed
- No automated tests are present; `pytest` fails because the `tests/` directory
  does not exist.
- Dashboard charts and analytics are placeholders across all HTML pages.
- Offline caching/service worker has not been implemented yet.

## Suggested Next Steps

1. **Automated Testing**
   - Create unit tests for each route under a new `tests/` directory.
   - Use `pytest` and add sample data fixtures for consistent results.
2. **Database Migration Tool**
   - Integrate a migration tool like Alembic to handle future schema changes.
   - Track versions so frontend and backend stay aligned with the DB schema.
3. **API Documentation**
   - Generate OpenAPI docs from route definitions. This helps frontend developers keep fetch calls consistent.
4. **Continuous Integration**
   - Set up a CI workflow to run `pytest` and lint checks on each PR.
5. **Frontend Build**
   - Organize JS/CSS under `frontend/assets/` and consider bundling for production.
6. **Service Worker for Offline Support**
   - Implement caching strategies and sync logic to enable offline usage.

This plan keeps all project layers synchronized as development continues.
