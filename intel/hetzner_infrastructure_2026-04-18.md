# AZTEX Hetzner Server Infrastructure
**Date:** 2026-04-18
**IP:** 37.27.206.233 (Hetzner HEL)

---

## Open Services

| Port | Service | Auth | Notes |
|------|---------|------|-------|
| 21 | Pure-FTPd (TLS) | Required | No anonymous access |
| 22 | SSH | Required | |
| 80/443 | Caddy (HTTPS) | CapVerified CAPTCHA gateway | All subdomains behind gateway |
| 587 | SMTP submission | Required | |
| 6379 | Redis | **Required** | NOAUTH — password set |
| 9000 | MinIO S3 API | Required | AccessDenied anonymous |
| 9001 | **MinIO Console** | Required (401) | Web UI exposed, no default creds |
| 9090 | Unknown (404) | — | |
| 9099 | **Prometheus** | **NONE — OPEN** | Full metrics exposed |

---

## Critical Finding: Telegram MTProxy (Yandex Cloud Russia)

Prometheus monitors two Telegram proxy servers on Yandex Cloud:

| Instance | IP | Port | Status |
|----------|-----|------|--------|
| yandex-server-1 | 51.250.121.109 | 9095 | UP |
| yandex-server-2 | 51.250.121.79 | 9095 | UP |

- Software: `telemt` v3.3.39 (custom Telegram MTProxy)
- Uptime server-1: ~4.3 days at time of collection
- **Total registered proxy users: 215**
- **Currently active users: 23** (at 2026-04-18 ~23:57 UTC)

### Active Telegram IDs (Server 1 — 51.250.121.109)
| Telegram ID | Active IPs |
|-------------|-----------|
| 31144206 | 2 |
| 185342318 | 1 |
| 188003855 | 1 |
| 196260543 | 1 |
| 287570079 | 1 |
| 319972898 | 1 |
| 401073252 | 1 |
| 408256521 | 1 |
| 539522739 | 1 |
| 551283177 | 1 |
| 569147569 | 2 |
| 723641178 | 1 |
| 914495187 | 1 |
| 1061332674 | 1 |
| 1921591648 | 2 |
| 2115220181 | 2 |
| 5622951042 | 1 |

### Active Telegram IDs (Server 2 — 51.250.121.79)
| Telegram ID | Active IPs |
|-------------|-----------|
| 151775487 | 1 |
| 1130708464 | 1 |
| 1386394376 | 1 |
| 5673942336 | 1 |
| 5798978049 | 1 |
| 7907823179 | 2 |

### Full ID list
Saved to: `/home/me/scamfinder/intel/aztex_telegram_ids.txt`

---

## Subdomains (DNS removed, behind CAPTCHA on Hetzner)
- nextcloud.aztex.eu — Nextcloud (behind CapVerified)
- matrix.aztex.eu — Matrix (behind CapVerified)
- route-finder.aztex.eu — Custom AZTEX tool (behind CapVerified)
- route-lister.aztex.eu — Custom AZTEX tool (behind CapVerified)

---

## Law Enforcement Value
- **Yandex Cloud subpoena** for 51.250.121.109 and 51.250.121.79: account holder KYC, payment method, creation IP
- **Telegram subpoena** for all 215 user IDs: real identity, phone numbers, account history
- **MinIO**: operator file storage — documents, victim data, backups
- **Prometheus config** confirms deliberate monitoring infrastructure = organized operation
