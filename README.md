# 🛒 Shopnow (E‑Kart) – Django E‑Commerce Web Application

## 📌 Project Overview

**Shopnow (E‑Kart)** is a full‑stack e‑commerce web application built using **Django**. The project allows users to register, log in, browse products, add items to a cart, and place orders. It follows Django’s **MTV (Model‑Template‑View)** architecture and uses Bootstrap for responsive UI.

This project is designed as a **learning + production‑ready mini e‑commerce platform**, suitable for fresher interviews, real‑world demonstrations, and scalable deployment scenarios including online payments and order management.

---

## 🚀 Features

### 👤 User Module

* User Registration
* User Login & Logout
* Forgot Password (Reset password manually)
* Django Authentication System

### 🛍️ Product Module

* Product listing with price & unit
* Category‑wise products
* Product images using Django Media
* Dynamic product rendering

### 🛒 Cart Module

* Add to cart functionality
* Quantity management
* Dynamic cart update (frontend‑based)

### 💳 Payment Module (Razorpay)

* Razorpay payment gateway integration
* Secure online payments
* Payment verification and order confirmation

### 📦 Order Module

* Order creation after successful payment
* Order history for users
* Order status tracking

### 🎨 UI / Frontend

* HTML5, CSS3
* Bootstrap 5
* Javascript
* Responsive design
* Reusable templates

---

## 🧰 Tech Stack

| Layer        | Technology                       |
| ------------ | -------------------------------- |
| Backend      | Python, Django                   |
| Frontend     | HTML, CSS, Bootstrap 5, JavaScript (Axios) |
| Database     | MySQL (used as primary database) |
| Payments     | Razorpay Payment Gateway         |
| Auth         | Django Auth System               |
| Static Files | Django Static & Media            |

---

## 📁 Project Structure

```
# 📁 Shopnow Project Structure

```
Shopnow/
│
├── apps/
│   └── shop/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── forms.py
│       ├── migrations/
│       │   └── __init__.py
│       ├── models.py
│       ├── templatetags/
│       │   └── custom_tags.py
│       ├── urls.py
│       └── views.py
│
├── config/
│   ├── settings     # Django settings
│   │      ├── __init__.py
│   │      ├── base.py
│   │      ├── dev.py
│   │      └── prod.py
│   │
│   ├── __init__.py
│   ├── urls.py          # Project routing
│   └── wsgi.py          # WSGI entrypoint
│
├── media/
│      ├── images
│      └── media/
│             └── images
│ 
├── static/              # Static assets (CSS, JS, images)
│
├── template/            # Global HTML templates
│
├── .gitignore
├── README.md
├── manage.py            # Django project launcher
└── requirements.txt     # Dependencies list

---

## 🔁 Project Flow (Step‑by‑Step)

### 1️⃣ User Registration Flow

```
User → Register Page → Form Validation → User Created → Redirect to Home
```

### 2️⃣ User Login Flow

```
User → Login Page → Credentials Check → Session Created → Home Page
```

### 3️⃣ Browse Products Flow

```
User → Home Page → Product List → Product Card → Price & Unit Display
```

### 4️⃣ Add to Cart Flow

```
User → Click Add to Cart → Product ID Captured → Cart Updated → Quantity Control
```

User → Click Add to Cart → Product ID Captured → Cart Updated → Quantity Control

```

### 5️⃣ Payment & Order Flow
```

User → Checkout → Razorpay Payment → Payment Verification → Order Created → Order History Updated (MySQL)

```

### 6️⃣ Logout Flow
```

User → Logout → Session Destroyed → Redirect to Home

````

---

## 🧠 Architecture Used

- **MTV (Model-Template-View)**
- AJAX-based client–server communication using **Axios**
- REST-style Django views for cart & order actions
- Separation of concerns between UI, logic, and data
- Secure authentication & CSRF protection


---

### ⚙️ How to Run the Project

### 1️⃣ Clone or Extract Project
```bash
git clone <repository-url>
cd E-Kart/Shopnow

````

### 2️⃣ Activate Virtual Environment

```bash
env\Scripts\activate   # Windows
source env/bin/activate # Linux/Mac
```

### 3️⃣ Install Dependencies

```bash
pip install django
```

### 4️⃣ Run Migrations

```bash
python manage.py migrate
```

### 5️⃣ Create Superuser

```bash
python manage.py createsuperuser
```

### 6️⃣ Start Server

```bash
python manage.py runserver
```

Open browser:

```
http://127.0.0.1:8000/
```

---

## 🔐 Admin Panel

```
http://127.0.0.1:8000/admin/
```

Admin can:

* Add products
* Manage users
* Manage categories

---

## 📈 Future Enhancements

* Invoice generation (PDF)
* Order cancellation & refunds
* REST API for mobile app
* Docker & cloud deployment (AWS)
* Advanced sales analytics dashboard


---

## 👨‍💻 Author

**Sairaj Jadhav**


---

