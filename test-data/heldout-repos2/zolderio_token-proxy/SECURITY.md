# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in llm-token-proxy, please report it responsibly.

**Do not open a public GitHub issue for security vulnerabilities.**

Instead, use [GitHub Security Advisories](https://github.com/zolderio/token-proxy/security/advisories/new) to file a private report. Please include:

- A description of the vulnerability
- Steps to reproduce
- Impact assessment
- Any suggested fix (optional)

We will acknowledge your report within 48 hours and aim to release a fix within 7 days for critical issues.

## Scope

The following are in scope:

- PII leaking through the proxy (pseudonymization bypass)
- Session data exposure
- Configuration API vulnerabilities
- Denial of service via crafted payloads

## Out of Scope

- The proxy is designed for internal/trusted networks. Attacks requiring network access to the proxy host are expected to be mitigated by network-level controls.
- The config/audit API has no authentication by design (internal-only). Do not expose it to untrusted networks.
