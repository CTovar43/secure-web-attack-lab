# Secure Web Attack Lab (Flask)

A security learning project that demonstrates identifying, exploiting, and remediating common web vulnerabilities (OWASP Top 10).

## Features
- User registration + login (bcrypt password hashing)
- Notes feature (user-generated content)
- Admin dashboard (RBAC-protected)
- Security headers + basic CSP
- Security logging for auth events and admin access attempts

## What I Did
### Vulnerabilities Implemented (Learning Phase)
- SQL Injection (authentication bypass)
- Stored XSS (notes rendering)
- Broken Access Control (admin exposure)

### Remediations Implemented
- Parameterized queries to prevent SQL Injection
- bcrypt password hashing
- Output encoding to mitigate XSS
- Role-based access control (RBAC) for admin routes
- Hardened session cookies + security headers (CSP, clickjacking protection)

## Run Locally
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
export SECRET_KEY="dev-secret"  # Windows PowerShell: $env:SECRET_KEY="dev-secret"
python app.py
