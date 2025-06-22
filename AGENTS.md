
# 💊 PharmaCuz – AGENTS.md

## 📦 Repository Context

PharmaCuz is a role-based Pharmaceutical Inventory & Distribution Management System. The architecture is modular and mobile-first, with support for offline capabilities and multi-tier supply chain tracking from Manufacturer → CFA → Super Stockist.

## 📁 Folder Overview

```

pharmacuz/
├── backend/
│   ├── models/           # ORM models with SQLAlchemy (or Pydantic)
│   ├── controllers/      # Business logic layer
│   ├── routes/           # REST APIs (restapi or Flask)
│   ├── middleware/       # JWT & RBAC logic
│   └── database/         # Migration scripts and seeders
├── frontend/
│   ├── mobman.html       # Manufacturer dashboard UI
│   ├── cfa.html          # CFA dashboard UI
│   ├── stockist.html     # Super Stockist dashboard UI
│   └── assets/           # JS, CSS, Chart.js, etc.
├── docs/
│   ├── README.md         # Overview & setup
│   └── AGENTS.md         # Agent instructions
├── product name.txt      # Product master list (CUZON Pharma)
└── tests/                # Unit and integration tests

````

---

## 🧠 Codex Agent Instructions

### 🔍 Where to Work
- Focus changes in:
  - `backend/models/` for DB schema updates
  - `backend/routes/` for APIs
  - `frontend/*.html` for dashboard UI enhancements
- Read `product name.txt` for product names
- Never modify `docs/` unless explicitly told

### ⚒️ Tasks Agents Can Perform
- Add CRUD APIs for stock, orders, users, schemes
- Generate restapi/Flask route handlers using JWT-auth guards
- Create Chart.js dashboards from dummy API data
- Add notification alerts based on JSON inputs
- Automatically adjust HTML tabs and content sections

---

## 🧪 Validation & Testing

- Run backend with:

```bash
python  main.py
````

* Test auth & routes via:

```bash
curl -X POST http://localhost:any/api/auth/login -d 'username=admin&password=admin'
```


* Run unit tests:

```bash
pytest tests/
```

---

## ✅ Contribution Guidelines

* several module per PR (e.g., `orders`, `products`)
* Format titles like `[Backend] Add API for Product Create` , 'add frontend'
* Include:

  * Controller logic
  * API routes
  * Model update if needed
  * SQL migrations if schema changes

---

## 🧭 Prompting Agents

✅ Always include:

* Folder path (e.g., `routes/order.py`)
* Expected input/output or HTTP method
* Sample response schema

⚠️ Avoid:

* Ambiguous terms like “optimize” without context
* Modifying multiple unrelated files in one go

✅ Good:

```md
"Add GET /api/orders for manufacturer with optional status filter"
```

---

## 🧰 Dev Setup Tips

* Use virtualenv for Python:

  ```bash
  python -m venv venv && source venv/bin/activate
  pip install -r requirements.txt
  ```

* Use Live Server plugin for HTML preview of dashboards

* For dynamic data in HTML: connect via fetch() from `/api/...` endpoints

---

## 💡 Sample Agent Prompt

```
Create a new route in `routes/order.py` to fetch all pending orders for a super stockist. Use JWT middleware from `middleware/auth.py` and return results using the `OrderModel` in JSON.
```

---

## 🧠 Codex Debugging Tip

Paste errors like:

```
Traceback (most recent call last):
File "main.py", line 20, in <module>
SyntaxError: invalid syntax
```

...to let the agent suggest exact fixes or alternative implementation.

---

## 📚 Reference Docs

* Chart.js: [https://www.chartjs.org/docs/latest/](https://www.chartjs.org/docs/latest/)
* restapi: [https://restapi.tiangolo.com/](https://restapi.tiangolo.com/)
* Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
* JWT Auth: [https://jwt.io/](https://jwt.io/)

---

## 📌 Final Notes

* Always respect file boundaries (no HTML in Python, no DB logic in frontend)
* Agents must generate production-quality, testable code
* dont Prefer single-responsibility changes per task

---

This file will guide intelligent agents (human or AI) to contribute effectively and maintain consistent standards across PharmaCuz.

```

---

Let me know if you want this embedded in a zip, pushed to Git, or split by modules like `agents.manufacturer.md`, `agents.super_stockist.md`, etc.
```
