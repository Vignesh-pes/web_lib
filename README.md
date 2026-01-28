Created a simple Library management system with authentication with RBAC as Admin and members 

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