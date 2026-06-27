# Final Production Checklist

## Completed

- Core Flask pages render.
- Diagnosis workflow works.
- Review workflow works.
- Prediction workflow works.
- Login and registration work.
- History protection works.
- Admin protection works.
- Admin analytics work.
- CSV export works.
- Versioned API works.
- Health endpoint works.
- SQLite local mode works.
- PostgreSQL configuration is available.
- Render files are available.
- Docker files are available.
- Procfile is available.
- Vercel routing file is available.
- Shared metadata is available.
- Web manifest is available.
- Favicon is available.
- Robots endpoint is available.
- Sitemap endpoint is available.
- Offline fallback is available.
- Static cache headers are available.
- Security headers are available.
- Syntax checks passed.
- Cleanup scans passed.

## Before Public Deployment

- Replace the default admin password.
- Use a strong production `SECRET_KEY`.
- Use PostgreSQL through `DATABASE_URL`.
- Keep `SESSION_COOKIE_SECURE=true`.
- Run migrations on the production database.
- Review application logs after deployment.
- Confirm `/api/v1/health` returns `ok`.
- Verify the admin dashboard with production data.
- Confirm print export on the result page.
