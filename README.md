# Library Management Web Application

## Project Overview
This project is a **server-rendered Library Management Web Application** built using **Flask**, **JWT-based authentication**, and **SQLite**.  
It demonstrates **secure login**, **role-based access control (RBAC)**, and **page-level authorization** using industry-standard practices.

The application supports **Admin** and **Member** roles with clearly separated permissions.

---

## Technology Stack
- Python 3
- Flask
- Flask-JWT-Extended
- SQLite3 (raw SQL, no ORM)
- Jinja2 (HTML templates)
- bcrypt (password hashing)

---

## Features

### Authentication
- Username and password based login
- Passwords securely hashed using **bcrypt**
- JWT tokens issued on successful login
- JWT stored in **HTTP-only cookies**
- Logout clears JWT cookies

### Authorization (RBAC)
- Role-based authorization using **JWT claims**
- Access enforced at **route level**, not just UI
- Unauthorized access returns **403 Forbidden**

---

## User Roles & Permissions

### Admin
- Login to admin dashboard
- View all books
- Add new books

### Member
- Login to member dashboard
- View available books only

❌ Members cannot add, edit, delete, borrow, or return books  
❌ Members cannot access admin routes

---

## JWT & Security Design
- JWT implemented using **Flask-JWT-Extended**
- Protected routes use `@jwt_required()`
- User role stored as a JWT claim
- Role validated on every protected route
- Passwords never stored in plain text

---

## Database Schema

### users
| Column   | Type    | Description        |
|----------|---------|--------------------|
| id       | INTEGER | Primary key        |
| username | TEXT    | Unique username    |
| password | BLOB    | Hashed password    |
| role     | TEXT    | admin / member     |

### books
| Column    | Type    | Description        |
|-----------|---------|--------------------|
| id        | INTEGER | Primary key        |
| title     | TEXT    | Book title         |
| author    | TEXT    | Author name        |
| available | INTEGER | Availability flag  |

### borrowed_books
| Column      | Type      | Description     |
|-------------|-----------|-----------------|
| id          | INTEGER   | Primary key     |
| user_id     | INTEGER   | User reference  |
| book_id     | INTEGER   | Book reference  |
| borrowed_at | TIMESTAMP | Borrow date     |

---

## Default Login Credentials

### Admin
