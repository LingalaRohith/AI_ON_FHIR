# Security & HIPAA Compliance Strategy

This document outlines how the FHIR Query Tool ensures **HIPAA compliance** and securely handles sensitive patient data.

---

## 1. Authentication & Authorization

- **OAuth 2.0 with SMART on FHIR**:
  - The application uses **SMART on FHIR** for secure, standardized access to electronic health records.
  - Supports both **standalone** and **EHR-launched** workflows.
  - Access tokens are issued with precise **FHIR scopes** (e.g., `patient/*.read`, `user/*.write`) depending on user roles.
  - All tokens are **short-lived** and **revocable** to limit exposure in case of compromise.

- **Token-Based Access**:
  - Every request to the backend API is authenticated using **Bearer tokens**.
  - Tokens are validated for integrity, expiration, and scope before data access.

---

## 2. Data Privacy & Audit Logging

- **Encryption**:
  - **Transport encryption** via HTTPS (TLS 1.2+).
  - **Data at rest** is protected using AES-256 encryption.

- **Audit Logging**:
  - All access to FHIR resources is **audited**.
  - Each log entry includes:
    - `timestamp`
    - `user identifier`
    - `access type (read/write)`
    - `resource accessed`
    - `IP address`
  - Logs are stored in an **immutable** and **secure audit trail** for at least **6 years**, meeting HIPAA retention requirements.

- **De-identification**:
  - For research or export purposes, data is **de-identified** by removing PHI (names, addresses, SSNs, etc.).
  - Optionally, **pseudonymization** techniques are applied using UUIDs.

---

## 3. Role-Based Access Control (RBAC)

- **User Roles & Permissions**:
  | Role       | Permissions                                  |
  |------------|----------------------------------------------|
  | Admin      | Full access to all data and audit logs       |
  | Clinician  | View/edit records of their assigned patients |
  | Patient    | Read-only access to their own data           |
  | Researcher | Access only to de-identified datasets        |

- **Enforced via OAuth scopes and server-side logic**:
  - Example: A `patient` role is only allowed `patient/Patient.read` scoped data.
  - Unauthorized access is rejected with HTTP 403 responses.

---

## Summary

This FHIR system follows industry best practices for security and privacy, including:

- SMART on FHIR + OAuth 2.0 authorization
- HTTPS + AES encryption
- Immutable audit logging
- RBAC enforcement
- PHI de-identification for non-clinical use cases

Together, these controls ensure the application is **HIPAA-compliant** and safeguards sensitive healthcare information at every layer.
