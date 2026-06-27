# Project Roadmap

## Current Phase

The project is in Phase 1: Production Architecture Upgrade.

Phase 1 focuses on architecture, configuration, logging, validation, error handling, repository preparation, and documentation while preserving all existing user-facing behavior.

## Phase Plan

| Phase | Name | Goal | Status |
| --- | --- | --- | --- |
| 1 | Production Architecture | Add production-ready structure without changing features | In progress |
| 2 | Backend Modernization | Add API structure, versioning, health checks, and stronger backend contracts | Pending |
| 3 | Database Upgrade | Add SQLAlchemy, migrations, and PostgreSQL support | Pending |
| 4 | Premium UI/UX | Improve the full frontend experience and visual system | Pending |
| 5 | Prediction Experience | Improve result explanations, safety notes, and export options | Pending |
| 6 | Admin Analytics | Add charts, filters, reporting, and exports | Pending |
| 7 | Deployment | Prepare Render, Vercel, Docker, and deployment documentation | Pending |
| 8 | Optimization | Improve performance, accessibility, monitoring, and reliability | Pending |
| 9 | Future Expansion | Prepare larger product capabilities and integrations | Pending |

## Phase 1 Acceptance Criteria

- Existing routes continue working.
- Authentication continues working.
- Prediction flow continues working.
- History and admin pages continue working.
- SQLite remains the active database.
- No machine learning model change is made.
- Configuration supports environment variables.
- Logging is centralized.
- Error handling is centralized.
- Repository layer exists for future database migration.
- Changelog and architecture documentation are updated.

## Next Phase

After Phase 1 is approved, Phase 2 should modernize the backend while preserving the current HTML pages.
