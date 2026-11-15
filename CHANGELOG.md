# Changelog

## [v0.1.0] - 2026-11-15

First tagged release of the live `master`.

### Added
- Task CRUD on MongoDB (Motor): `POST /tasks/`, `GET /tasks/?email=`, `PUT /tasks/{id}`, `DELETE /tasks/{id}`
- Clerk bearer-token (RS256 JWT) authentication with per-endpoint scopes
- Health check: `GET /tasks/health-check`
- AI endpoints (OpenAI): `POST /ai/chat`, `GET /ai/balance`
- Authenticated `/docs`, `/redoc` and `/openapi.json`
- Docker image for AWS ECS (`infra/aws`) and Modal deployment (`infra/modal`)
- MIT licence

[v0.1.0]: https://github.com/JPhlpL/taskmgmt-fastapi/releases/tag/v0.1.0
