## Authentication & Authorization

This application uses JWT-based authentication implemented using
Flask-JWT-Extended.

- JWT tokens are issued during login
- Tokens are stored securely in HTTP-only cookies
- Protected routes use @jwt_required() decorator
- Role-based authorization is enforced using JWT claims
- Admin and Member roles are validated on every protected route

Project Structure
library-web-app/
├── app.py
├── auth.py
├── admin.py
├── member.py
├── database.py
├── templates/
│ ├── base.html
│ ├── login.html
│ ├── register.html
│ ├── admin/
│ │ ├── dashboard.html
│ │ └── books.html
│ └── member/
│ ├── dashboard.html
│ └── books.html
├── static/
│ └── style.css
├── requirements.txt
└── README.md