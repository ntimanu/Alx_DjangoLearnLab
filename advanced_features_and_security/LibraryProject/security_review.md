# Security Enhancements for HTTPS and Secure Redirects

## Changes Implemented:

1. **Redirect HTTP to HTTPS**
   - `SECURE_SSL_REDIRECT = True`
2. **Enable HTTP Strict Transport Security (HSTS)**
   - `SECURE_HSTS_SECONDS = 31536000`
   - `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
   - `SECURE_HSTS_PRELOAD = True`
3. **Enforce Secure Cookies**
   - `SESSION_COOKIE_SECURE = True`
   - `CSRF_COOKIE_SECURE = True`
4. **Implement Security Headers**
   - `X_FRAME_OPTIONS = "DENY"`
   - `SECURE_CONTENT_TYPE_NOSNIFF = True`
   - `SECURE_BROWSER_XSS_FILTER = True`
5. **Configured Nginx for SSL/TLS**
   - Redirected all HTTP traffic to HTTPS.
   - Added SSL certificate configuration.

## Testing Checklist:

✅ Check that HTTP requests are **redirected** to HTTPS.  
✅ Verify HSTS headers using `curl -I https://yourdomain.com`.  
✅ Test cookies in Chrome DevTools (ensure they have **Secure** and **HttpOnly** flags).  
✅ Confirm that **Clickjacking, XSS, and MIME sniffing protections** are active.

## Next Steps:

- Set up automatic SSL certificate renewal (e.g., with **Certbot**).
- Monitor security headers using **Mozilla Observatory**.
