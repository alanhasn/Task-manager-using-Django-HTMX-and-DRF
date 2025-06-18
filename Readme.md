````markdown
# 📝 ToDo Manager API

A clean and secure ToDo API built with **Django REST Framework**, featuring **JWT Authentication**, advanced filtering, search, ordering, and auto-generated documentation with **drf-spectacular**.

---

## 🚀 Overview

This project allows users to:

- Register a new account
- Log in using JWT (JSON Web Token)
- Create / Read / Update / Delete their own tasks (ToDos)
- Filter, search, and order tasks
- Access a fully interactive API documentation (Swagger & ReDoc)

---

## 🛠️ Tech Stack

| Technology | Description                |
|------------|----------------------------|
| Django     | v5.2.3                     |
| DRF        | Django REST Framework      |
| SimpleJWT  | Token-based authentication |
| drf-spectacular | OpenAPI 3 documentation |
| django-filter | Filtering support         |

---

## 📦 Setup Instructions

1. **Clone the repo**  
```bash
git clone https://github.com/alanhasn/TodoList-API.git
cd todo-api
````

2. **Create a virtual environment**

```bash
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Apply migrations**

```bash
python manage.py migrate
```

5. **Run the server**

```bash
python manage.py runserver
```

---

## 🔐 Authentication (JWT)

We use [Simple JWT](https://django-rest-framework-simplejwt.readthedocs.io/) for secure login.

### ✅ Register

`POST /api/register/`

```json
{
  "username": "alan",
  "email": "alan@example.com",
  "password": "StrongPassword123"
}
```

### 🔑 Login

`POST /api/login/`

```json
{
  "username": "alan",
  "password": "StrongPassword123"
}
```

### 🔁 Refresh Token

`POST /api/token/refresh/`

```json
{
  "refresh": "<your_refresh_token>"
}
```

---

## 📚 API Documentation

Auto-generated API docs using **drf-spectacular**:

* **Swagger UI:**
  `http://127.0.0.1:8000/api/docs/`

* **Schema (OpenAPI):**
  `http://127.0.0.1:8000/api/schema/`

---

## 🧪 API Endpoints

| Method | Endpoint         | Description                                          | Auth Required |
| ------ | ---------------- | ---------------------------------------------------- | ------------- |
| GET    | /api/todos/      | List user’s todos                                    | ✅ Yes         |
| POST   | /api/todos/      | Create a new todo                                    | ✅ Yes         |
| GET    | /api/todos/{id}/ | Retrieve a todo by ID                                | ✅ Yes         |
| PUT    | /api/todos/{id}/ | Update a todo                                        | ✅ Yes         |
| DELETE | /api/todos/{id}/ | Delete a todo                                        | ✅ Yes         |
| GET    | /api/users/      | Get current authenticated user info with their todos | ✅ Yes         |

---

## 🔍 Filtering, Search, Ordering

| Feature           | Query Example                            |
| ----------------- | ---------------------------------------- |
| Filter by status  | `/api/todos/?completed=true`             |
| Filter by date    | `/api/todos/?created_at__gte=2024-01-01` |
| Search title/desc | `/api/todos/?search=meeting`             |
| Order by update   | `/api/todos/?ordering=-updated_at`       |

---

## 📂 Project Structure (Simplified)

```
|── project/
│ └── settings.py
│
├── todo/ # main app
│ ├── models.py
│ ├── admin.py
│ ├── apps.py
│ ├── urls.py 
│ │
│ └── api/ # API logic 
│ ├── views.py
│ ├── serializers.py
│ ├── urls.py 
│ ├── filters.py
│
├── manage.py
└── requirements.txt
```

---

## 🤝 Contributing

Pull requests are welcome. For major changes, please open an issue first.

---

## 📃 License

MIT License – Free to use and modify.

```

