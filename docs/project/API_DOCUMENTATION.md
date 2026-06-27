# API Documentation

Base URL:

```text
/api/v1
```

All API responses use a consistent JSON envelope.

Successful response:

```json
{
  "success": true,
  "data": {}
}
```

Error response:

```json
{
  "success": false,
  "error": {
    "message": "Error message",
    "code": "error_code"
  }
}
```

## Health

### GET `/api/v1/health`

Checks whether the backend is available.

Response:

```json
{
  "success": true,
  "data": {
    "status": "ok",
    "service": "medical-diagnosis-assistant",
    "version": "v1",
    "environment": "development"
  }
}
```

## Symptoms

### GET `/api/v1/symptoms`

Returns available symptom options.

## Predictions

### POST `/api/v1/predictions`

Runs a disease prediction from selected symptoms.

Request:

```json
{
  "symptoms": ["fever", "cough"]
}
```

Response status:

```text
201 Created
```

The prediction is saved as a diagnosis record. If a user is logged in, the record is linked to that user.

Response data includes:

- saved diagnosis id
- predicted disease
- confidence percentage
- selected symptom labels
- report insights with confidence level, risk score, severity, probability rows, recommendations, care notes, emergency warning, and disclaimer

## Authentication

### POST `/api/v1/auth/register`

Creates a user account and starts a session.

Request:

```json
{
  "name": "Student User",
  "email": "student@example.com",
  "password": "password123"
}
```

### POST `/api/v1/auth/login`

Starts a session for an existing user.

Request:

```json
{
  "email": "admin@medscope.local",
  "password": "Admin@12345"
}
```

### POST `/api/v1/auth/logout`

Clears the current session.

### GET `/api/v1/me`

Returns the current authentication state.

## User Records

### GET `/api/v1/history`

Requires login.

Returns diagnosis records for the current user.

## Admin

Admin endpoints require a logged-in admin account.

### GET `/api/v1/admin/summary`

Returns user, diagnosis, activity, and guest diagnosis counts.

### GET `/api/v1/admin/analytics`

Returns chart data and report summaries for the admin analytics dashboard.

### GET `/api/v1/admin/users`

Returns registered users and diagnosis counts.

### GET `/api/v1/admin/diagnoses`

Returns recent diagnosis records.

### GET `/api/v1/admin/activities`

Returns recent activity logs.

## Status Codes

| Status | Meaning |
| --- | --- |
| 200 | Request completed |
| 201 | Resource created |
| 400 | Invalid request |
| 401 | Login required |
| 403 | Admin access required |
| 404 | Route not found |
| 500 | Server error |
