# P-RF03 — Biometric authentication vault

Protect access to the user's data with a Face ID / Touch ID / PIN barrier, validated on the device.

- Requirement and acceptance criteria: `docs/input/requirements.md`, section 1, RF03; parameter: section 10.
- Prototype states: "Tela 0.1 — Biometria", "Tela 0.1b — PIN inicial", "Tela 0.1c — PIN após falha" (prototype extract, section 2.1).
- Backend: no biometric endpoint (requirements, section 6.1). The biometrics preference is stored via `PATCH /account/settings`; the session is renewed with `POST /auth/refresh` or `POST /auth/login`; `POST /auth/logout`.
- Depends on: F000 (session, login).

## Do not

- Implement features of later units.
- Build extension features (requirements, section 2).
- Change the backend.
