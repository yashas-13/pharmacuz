
# 💊 PharmaCuz – Pharmaceutical Distribution and Inventory Management System

**PharmaCuz** is a mobile-first, role-based supply chain management platform for pharmaceutical manufacturers, CFAs, super stockists, and retailers. Built using a Python backend and modern frontends, it enables real-time visibility, order processing, and stock traceability across the distribution chain.

---

## 🚀 Features by User Role

### 🏭 Manufacturer
- Live production dashboard
- Order volume analytics (daily/weekly/monthly)
- Stock heatmaps across warehouses
- Dispatch tracking & delay analytics
- Scheme management (offers & BOGO)
- Top-selling products chart

### 🏢 CFA (Clearing & Forwarding Agent)
- Daily task summary (to pack, dispatch, pending)
- Live feed of dispatch status
- Inventory movement tracking
- Refill suggestions for fast-moving items
- QR code scanner for verification

### 🏬 Super Stockist
- Reorder suggestions and inventory tracking
- Order placement with autosave cart
- Order lifecycle timeline (requested → approved → transit → delivered)
- Offer-based discounts and eligibility
- Order history & receipts

---

## 🧱 Project Structure

```

pharmacuz/
├── backend/               # Python + RESTAPI or Flask backend
│   ├── models/            # ORM Models (SQLAlchemy / Pydantic)
│   ├── controllers/       # Logic layer
│   ├── routes/            # API endpoints
│   └── middleware/        # JWT Auth, Role guards
├── frontend/
│   ├── mobman.html        # Manufacturer Dashboard (Mobile UI)
│   ├── cfa.html           # CFA Dashboard
│   ├── stockist.html      # Super Stockist Dashboard
│   └── assets/            # CSS, JS, Chart.js, Icons
├── database/
│   ├── schema.sql         # DB schema
│   └── seed.sql           # Seed data (products, users)
├── product-list.txt       # Master product names (CUZON Pharma)
├── README.md

````

---

## ⚙️ Installation

### 🔧 Backend (RESTAPI or Flask)

```bash
# Setup virtual environment
python -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
````

### 🌐 Frontend

Simply open any of the HTML dashboards (e.g., `mobman.html`) in the browser for local UI preview.

---

## 📦 Product List (CUZON Pharma)



 { "name": "PANSZ-DSR", "desc": "Pantoprazole 40mg + Domperidone 30mg SR (Capsules)" },
  { "name": "XIMPRAZ", "desc": "Esomeprazole 40mg + Domperidone 30mg SR (Capsules)" },
  { "name": "SOOKRAL SUSP", "desc": "Sucralfate 500mg + Oxetacaine 10mg Suspension (100ml)" },
  { "name": "ZEKMOL 250 SUSP", "desc": "Paracetamol 250mg Suspension (60ml)" },
  { "name": "ZOACE-P", "desc": "Aceclofenac 100mg + Paracetamol 325mg (Tablet)" },
  { "name": "ZOACE-SP", "desc": "Aceclofenac + Paracetamol + Serratiopeptidase (Tablet)" },
  { "name": "CAVIZIC", "desc": "Calcium Citrate + Magnesium + Vitamin K2 + D3 etc." },
  { "name": "ZIFLOZIN", "desc": "Dapagliflozin 10mg (Tablet)" }


Some featured SKUs include:

* **PANSZ-DSR** – Capsules; 10×10 Alu–Alu
* **XIMPRAZ** – Tablets; 10×10 Alu–Alu
* **SOOKRAL SUSP** – Suspension; 100 ml
* **ZEKCLAV-DS** – Syrup; 30 ml
* **GLIMCUZ-M GP 1/2** – Tablets; 10×10
* **ZEKMOL-650 TABLETS** – Tablets; 10×10



Full list in [`product name.txt`](./product%20name.txt)

---

## 📊 Tech Stack

| Layer      | Technology                            |
| ---------- | ------------------------------------- |
| Backend    | Python (RESTAPI , Flask)              |
| Frontend   | HTML5 + CSS + JS (Vanilla + Chart.js) |
| Database   | MySQL (via SQLAlchemy ORM)            |
| Auth       | JWT + Role-based access               |
| Deployment | Hostinger VPS / PWA Mode              |

---

## 🧪 API Testing

```bash
# Sample CURL to authenticate
curl -X POST http://localhost:any/api/auth/login -d 'username=admin&password=admin'

# Get super stockist orders
curl -H "Authorization: Bearer <JWT>" http://localhost:any/api/orders/stockist
```

---

## 📥 Contributing

* Fork and clone the repo
* Add your module under `backend/controllers/`
* Format code with `black`, and document APIs
* Pull Requests must include test validation and updated OpenAPI docs

---

## 🛡️ License

This project is © 2025 \[Pravidhi Solutions]. All rights reserved.

```

---

Let me know if you'd like to autogenerate OpenAPI documentation, Docker setup, or CI/CD deployment steps.
```
