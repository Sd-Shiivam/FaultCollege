# Vulnerabilities in FaultCollege Web Application

## Overview
This repository demonstrates several security vulnerabilities intentionally implemented for educational purposes.

### Vulnerabilities Identified:
1. **Server-Side Request Forgery (SSRF)**
   - **Location:** `home view POST method`
   - **Description:** Allows an attacker to make requests from the server to internal or external resources.

2. **Broken Authentication and Broken Access Control**
   - **Location:** `student login view`
   - **Description:** Direct ID reference allows account takeover via the 'userid' POST variable. Passwords stored in base64 format. Brute-forcing possible via 'forget password' feature.

3. **SQL Injection Vulnerability**
   - **Location:** `student dashboard view POST method`
   - **Description:** Direct execution of SQL with 'Noclass' variable, enabling SQL injection attacks.

4. **Cross-Site Scripting (XSS)**
   - **Location:** `home view POST method`
   - **Description:** Embeds content into the page via the 'currenturl' POST variable, susceptible to XSS attacks.

5. **Insufficient Logging & Monitoring**
   - **Location:** Multiple views
   - **Description:** Lack of proper logging for critical operations and failures.

6. **Security Misconfiguration**
   - **Location:** `show_students view POST method`
   - **Description:** CSRF exempted, sensitive data exposed on POST requests without authentication.

7. **Sensitive Data Exposure**
   - **Location:** `robots.txt view (roborts_view)`
   - **Description:** Sensitive data (like URL exclusions) exposed through a publicly accessible endpoint.

8. **Vulnerable Django Version**
   - **Version:** Django 3.2.24
   - **Description:** Known vulnerabilities in the Django framework version used, including potential Denial of Service (DoS) attacks.

9. **Cross-Origin Resource Sharing (CORS) Misconfiguration**
   - **Location:** `settings.py`
   - **Description:** CORS_ORIGIN_ALLOW_ALL and CORS_ALLOW_CREDENTIALS set to False, potentially restrictive or misconfigured CORS policy.

10. **Insecure Deserialization**
    - **Location:** Session handling (not explicitly mentioned)
    - **Description:** Demonstrates insecure handling of session serialization, vulnerable to exploitation if not properly managed.

---

## Disclaimer
This repository is for educational purposes only. It intentionally contains vulnerabilities that should not be deployed in a production environment. Use responsibly and ethically.
