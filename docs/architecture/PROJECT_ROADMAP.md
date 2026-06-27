# Project Roadmap

## Current Phase

Phase 3: Database Upgrade is complete.

The next phase is Phase 4: Premium UI/UX.

## Phase Plan

| Phase | Name | Goal | Status |
| --- | --- | --- | --- |
| 1 | Production Architecture | Add production-ready structure without changing features | Complete |
| 2 | Backend Modernization | Add API structure, versioning, health checks, and stronger backend contracts | Complete |
| 3 | Database Upgrade | Add SQLAlchemy, migrations, and PostgreSQL support | Complete |
| 4 | Premium UI/UX | Improve the full frontend experience and visual system | Pending |
| 5 | Prediction Experience | Improve result explanations, safety notes, and export options | Pending |
| 6 | Admin Analytics | Add charts, filters, reporting, and exports | Pending |
| 7 | Deployment | Prepare Render, Vercel, Docker, and deployment documentation | Pending |
| 8 | Optimization | Improve performance, accessibility, monitoring, and reliability | Pending |
| 9 | Future Expansion | Prepare larger product capabilities and integrations | Pending |

## Phase 3 Acceptance Criteria

- SQLite remains the default development database.
- SQLAlchemy models represent the database schema.
- Repositories use SQLAlchemy queries.
- Alembic migrations are available.
- PostgreSQL is supported through `DATABASE_URL`.
- Indexes exist for common user, diagnosis, and activity queries.
- Default admin seeding remains available.
- Existing pages and API endpoints continue working.

## Next Phase

After Phase 3 is approved, Phase 4 should improve the frontend experience without changing backend behavior.
