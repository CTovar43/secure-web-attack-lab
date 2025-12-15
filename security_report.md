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

### Remediation Summary
All identified vulnerabilities were remediated using industry best practices:
- SQL injection fixed via parameterized queries
- Passwords secured with bcrypt hashing
- Stored XSS mitigated through output encoding
- Admin access restricted via role-based access control (RBAC)

```markdown
### Defense-in-Depth Hardening
- Hardened session cookies (HttpOnly, SameSite; Secure in production)
- Added security headers (CSP, X-Frame-Options, nosniff, referrer policy)
- Added basic security logging (failed logins, admin access attempts)
