# Project Nexus: E-Commerce Backend

A fully functional, real-world e-commerce backend built to simulate a production-ready environment. This project emphasizes scalability, security, and performance, incorporating authentication, product management, orders, and Chapa payment integration.

This repository consolidates the key learnings from the ProDev Backend Engineering Program while applying them to a complete, industry-ready application.

---

## 📌 Project Objective
- Build a scalable, secure, and high-performance e-commerce backend.  
- Implement user authentication with JWT (register, login, get profile).  
- Manage products and categories with full CRUD operations.  
- Implement orders, order items, and payments (Chapa integration).  
- Optimize database queries with indexing and transactions.  
- Document APIs using Swagger/OpenAPI for frontend integration.  
- Follow professional workflows including version control, documentation, and best practices.  

---

## 🛠️ Tech Stack
- **Programming Language:** Python  
- **Framework:** Django & Django REST Framework (DRF)  
- **Database:** PostgreSQL  
- **Authentication:** JWT (JSON Web Tokens)  
- **Payment Gateway:** Chapa API  
- **API Documentation:** Swagger / OpenAPI  
- **Version Control:** Git & GitHub  

---

## 🧩 Core Features

### 1. Authentication
- Register a new user (`POST /api/auth/register/`)  
- Login and obtain JWT tokens (`POST /api/auth/login/`)  
- Get current user profile (`GET /api/auth/me/`)  

### 2. Products & Categories
- CRUD operations for products and categories  
- Filtering products by category  
- Sorting products by price  
- Pagination for large datasets  

### 3. Orders & Payments
- Create orders with multiple items (`POST /api/orders/checkout/`)  
- Validate product stock before checkout  
- Calculate order totals  
- Chapa payment integration for secure online payments  
- Webhook for automatic order status updates (PAID / FAILED)  
- Reduce stock after successful payment  

---

## 📊 Database Design

### ERD Diagram
![ERD](docs/erd.png)

### Entities & Relationships
- `User` → manages authentication  
- `Category` → organizes products  
- `Product` → contains product details and stock  
- `Order` → links user to purchased items and payment reference  
- `OrderItem` → links products to orders with quantity and price  

### Optimization
- Indexed frequently queried fields (e.g., `Product.slug`)  
- Used transactions to maintain data consistency  

---

## ⚡ Implementation Highlights
- **Secure Authentication:** JWT ensures token-based access.  
- **Robust Order Processing:** Atomic transactions prevent inconsistent stock levels.  
- **Payment Integration:** Chapa API handles payments with webhooks.  
- **Filtering & Sorting:** Efficient queries for product discovery.  
- **API Documentation:** Swagger/OpenAPI provides developer-friendly API docs.  

### Best Practices
- Environment variables for sensitive keys  
- Proper error handling and input validation  
- Clean, maintainable code  
- Version control with descriptive commits  

---

## 🚀 Installation & Setup

1. **Clone the repo:**
```bash
git clone <your-repo-url>
cd project-nexus-backend
````

2. **Create a virtual environment and install dependencies:**

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. **Setup `.env` with your database and Chapa keys:**

```ini
DATABASE_URL=postgres://user:password@localhost:5432/dbname
SECRET_KEY=your_django_secret
CHAPA_SECRET_KEY=your_chapa_secret
```

4. **Run migrations:**

```bash
python manage.py migrate
```

5. **Start the development server:**

```bash
python manage.py runserver
```

6. **Access Swagger docs:**

```
http://localhost:8000/swagger/
```

---

## 📚 API Endpoints Overview

### Authentication

| Endpoint              | Method | Description                  | Auth      |
| --------------------- | ------ | ---------------------------- | --------- |
| `/api/auth/register/` | POST   | Register a new user          | No        |
| `/api/auth/login/`    | POST   | Login and receive JWT tokens | No        |
| `/api/auth/me/`       | GET    | Get current user profile     | Yes (JWT) |

### Products

| Endpoint                | Method      | Description                              | Auth        |
| ----------------------- | ----------- | ---------------------------------------- | ----------- |
| `/api/products/`        | GET         | List all products (filter/sort/paginate) | No          |
| `/api/products/`        | POST        | Create a new product                     | Yes (Admin) |
| `/api/products/<slug>/` | GET         | Retrieve product details                 | No          |
| `/api/products/<slug>/` | PUT / PATCH | Update product                           | Yes (Admin) |
| `/api/products/<slug>/` | DELETE      | Delete a product                         | Yes (Admin) |

### Categories

| Endpoint                | Method      | Description               | Auth        |
| ----------------------- | ----------- | ------------------------- | ----------- |
| `/api/categories/`      | GET         | List all categories       | No          |
| `/api/categories/`      | POST        | Create a new category     | Yes (Admin) |
| `/api/categories/<id>/` | GET         | Retrieve category details | No          |
| `/api/categories/<id>/` | PUT / PATCH | Update category           | Yes (Admin) |
| `/api/categories/<id>/` | DELETE      | Delete category           | Yes (Admin) |

### Orders & Checkout

| Endpoint                | Method | Description                                            | Auth      |
| ----------------------- | ------ | ------------------------------------------------------ | --------- |
| `/api/orders/checkout/` | POST   | Create order, validate stock, initialize Chapa payment | Yes (JWT) |
| `/api/orders/`          | GET    | List current user orders                               | Yes (JWT) |
| `/api/orders/<id>/`     | GET    | Retrieve order details                                 | Yes (JWT) |

### Payments (Chapa)

| Endpoint                 | Method | Description                                        | Auth |
| ------------------------ | ------ | -------------------------------------------------- | ---- |
| `/api/payments/webhook/` | POST   | Chapa webhook to update order status automatically | No   |

---

## 🔍 Filtering & Pagination

**Filter products by category:**

```bash
/api/products/?category=electronics
```

**Sort products by price:**

```bash
/api/products/?ordering=price      # ascending
/api/products/?ordering=-price     # descending
```

**Pagination:**

```bash
/api/products/?page=2&page_size=10
```

---

## ⚡ Example Workflow

1. User registers at `/api/auth/register/`.
2. User logs in at `/api/auth/login/` and receives JWT token.
3. User browses products at `/api/products/`.
4. User creates an order via `/api/orders/checkout/`.
5. Backend validates stock, calculates totals, and initializes Chapa payment.
6. User completes payment, Chapa calls `/api/payments/webhook/`.
7. Order status updates automatically and stock is reduced.

---

## 🌟 Best Practices & Takeaways

* Write clean, maintainable, and well-tested code.
* Prioritize security (environment variables, input validation, JWT).
* Document APIs and database models for collaboration.
* Use version control and descriptive commits.
* Use transactions for atomic operations (e.g., order creation).
* Follow professional backend development workflows.

---

## 📌 Next Steps

* Add advanced search and recommendations.
* Implement async tasks for notifications and order processing.
* Introduce caching for high-performance queries.
* Expand to GraphQL API alongside REST.

---

## 🎯 Hosted Links & Demo

* **Swagger Docs:** [http://yourdomain.com/api/docs/](http://yourdomain.com/api/docs/)
* **Hosted Backend:** [http://yourdomain.com/](http://yourdomain.com/)
* **Demo Video:** <link to demo video>

---

## 📝 References

* [Django Documentation](https://docs.djangoproject.com/)
* [Django REST Framework](https://www.django-rest-framework.org/)
* [Chapa API Docs](https://developers.getchapa.com/)
* [PostgreSQL Documentation](https://www.postgresql.org/docs/)



