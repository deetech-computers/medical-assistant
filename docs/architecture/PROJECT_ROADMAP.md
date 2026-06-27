# Project Roadmap

## Current Phase

Phase 2: Backend Modernization is complete.

The next phase is Phase 3: Database Upgrade.

## Phase Plan

| Phase | Name | Goal | Status |
| --- | --- | --- | --- |
| 1 | Production Architecture | Add production-ready structure without changing features | Complete |
| 2 | Backend Modernization | Add API structure, versioning, health checks, and stronger backend contracts | Complete |
| 3 | Database Upgrade | Add SQLAlchemy, migrations, and PostgreSQL support | Pending |
| 4 | Premium UI/UX | Improve the full frontend experience and visual system | Pending |
| 5 | Prediction Experience | Improve result explanations, safety notes, and export options | Pending |
| 6 | Admin Analytics | Add charts, filters, reporting, and exports | Pending |
| 7 | Deployment | Prepare Render, Vercel, Docker, and deployment documentation | Pending |
| 8 | Optimization | Improve performance, accessibility, monitoring, and reliability | Pending |
| 9 | Future Expansion | Prepare larger product capabilities and integrations | Pending |

## Phase 2 Acceptance Criteria

- Existing HTML routes continue working.
- API routes are available under `/api/v1`.
- JSON responses use a consistent envelope.
- API authentication, prediction, history, and admin endpoints work.
- A health endpoint is available for deployment checks.
- Session settings are safer for production.
- API documentation is available.
- The machine learning model is unchanged.

## Next Phase

After Phase 2 is approved, Phase 3 should upgrade the database layer while keeping SQLite working for development.
