# Security Assessment Report
## Secure Web Attack Lab

### Executive Summary
A security assessment was conducted against a custom-built Flask web application. Multiple critical vulnerabilities were identified that could allow full compromise of user accounts and sensitive data.

---

### Application Overview
- Technology: Python (Flask), SQLite
- Authentication: Session-based
- Features: Login, notes, admin dashboard

---

### Vulnerability Summary

| ID | Vulnerability | Severity |
|----|--------------|----------|
| 1  | SQL Injection (Auth Bypass) | Critical |
| 2  | Stored XSS (Notes) | High |
| 3  | Broken Access Control | High |

---

### Methodology
- Manual testing
- OWASP Top 10 mapping
- Black-box testing of endpoints

---

### Detailed Findings
(See individual exploit reports in `/exploits`)
