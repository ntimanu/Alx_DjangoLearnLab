# Security Best Practices in LibraryProject

## ✅ Security Configurations

1. **DEBUG Disabled**: `DEBUG = False` to prevent sensitive data leakage.
2. **Secure Cookies**: `CSRF_COOKIE_SECURE = True`, `SESSION_COOKIE_SECURE = True` to enforce HTTPS.
3. **HSTS Enabled**: `SECURE_HSTS_SECONDS = 31536000` to enforce HTTPS.
4. **XSS & Clickjacking Protection**: `SECURE_BROWSER_XSS_FILTER = True`, `X_FRAME_OPTIONS = "DENY"`.

## ✅ CSRF Protection

- Added `{% csrf_token %}` to all forms.

## ✅ SQL Injection Prevention

- Used Django ORM instead of raw SQL queries.
- Implemented `BookSearchForm` for input validation.

## ✅ XSS Protection with CSP

- Implemented **Content Security Policy (CSP)** using `django-csp` middleware.

## ✅ Testing

1. **Check CSRF Protection**
   - Try submitting a form without `{% csrf_token %}`. Django should reject it.
2. **Test SQL Injection**
   - Enter `'; DROP TABLE bookshelf_book; --` in the search field. The database should not be affected.
3. **Check Secure Headers**
   - Use **https://securityheaders.com/** to analyze security headers.
