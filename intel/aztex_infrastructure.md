# AZTEX Criminal Infrastructure — Intelligence File
*Last updated: 2026-03-25*

## Overview
AZTEX is the internal name for the infrastructure/operator group behind the BIPPAX/BISSNEX/deptoy.co
pig-butchering scam network. The name appears both as criminal infrastructure (aztex.eu, aztex.digital)
and as fake exchange fronts (aztexchange.com, aztexcoins.com).

## Server Infrastructure

### IP 194.60.201.83 — PRIMARY OPS SERVER (Contabo, France) ⭐
- Provider: Contabo GmbH, AS51167, Lauterbourg, France
- Abuse: abuse@contabo.de
- CRITICAL: TLS certs for BOTH aztex.eu AND deptoy.co co-hosted here
- SMTP banner: `220-mail.aztex.eu ESMTP`
- Reverse IP domains: aztex.eu, bitwarden.aztex.eu, mail.aztex.eu, analytics.goeke.it (stale)
- This is the AZTEX operations hub with direct link to deptoy.co

### IP 37.27.206.233 — DEV/STAGING (Hetzner, Helsinki)
- Provider: Hetzner Online, AS24940, Helsinki, Finland
- Abuse: abuse@hetzner.de
- TLS cert: t-contest.aztex.digital
- Services: Redis (6379), MinIO Console (9000)
- Purpose: Platform development and testing environment

### IP 79.78.160.133 — UK OPERATOR "BARRY" (TalkTalk, England)
- Provider: TalkTalk, AS13285, England, UK
- Type: Residential broadband (MikroTik RouterOS home router)
- RDP port: 21680
- RDP certificate CN: **AZTEX-BARRY**
- Significance: Person named "Barry" uses this home internet to access AZTEX infrastructure via RDP
- UK Action Fraud / NCA referral target
- TalkTalk subscriber identity available via RIPA production order

## aztex.eu Domain
- Registrar: Porkbun LLC (Portland, OR — US company)
- Nameservers: Porkbun Brazilian-named NS
- Registrant: REDACTED (EURid GDPR)
- Last updated: ~March 2026 (recently active)
- Abuse: abuse@porkbun.com

## aztex.eu Subdomain Stack (from CT logs)
### Criminal Operations Infrastructure
- mail.aztex.eu — self-hosted mail server (SMTP/IMAP confirmed)
- bitwarden.aztex.eu / vaultwarden.aztex.eu — shared password manager
- matrix.aztex.eu — encrypted group messaging
- nextcloud.aztex.eu + admin.nextcloud.aztex.eu — shared file storage
- owncloud.aztex.eu — legacy storage
- rdp.aztex.eu — web-based RDP gateway

### Possibly Custom Scam Tools
- route-finder.aztex.eu — custom routing tool (money mule routes?)
- route-lister.aztex.eu — companion tool

### Unknown / Personal
- jukem.aztex.eu — ACTIVELY MAINTAINED (certs renewed every 2 months Apr-Dec 2025)
- ninjazz.aztex.eu — unknown app
- somegoodnews.aztex.eu — unknown content
- twenty48.aztex.eu — 2048 game

## aztex.digital Domain (staging/dev)
- Subdomains (from CT logs): project-cheapeats, project-omikami (Solana memecoin), t-contest, slepsk, obsidian, not-front-contest
- Pattern: "project-*" naming = new scam platform development

## jukem.aztex.eu — ACTIVE SERVICE ⚠️
Certificate history from crt.sh:
- Issued: 2025-04-10 (Let's Encrypt E5)
- Renewed: 2025-06-09 (E5)
- Renewed: 2025-08-08 (E6)
- Renewed: 2025-10-07 (E8)
- Renewed: 2025-12-05 (E8) — MOST RECENT
Total: 10 certificates, all Let's Encrypt, renewed every ~2 months = AUTO-RENEWED = LIVE SERVICE
**jukem.aztex.eu is currently running an active service as of December 2025**

## Fake Exchange Fronts
- aztexchange.com — GoDaddy, 2023-08-09, Alibaba hosting; registered 2026-03-01 (NEW), SUSPENDED 2026-03-03
- aztexcoins.com — GoDaddy, 2023-08-25, TrustAsia/Google Trust Services certs (C=CN)

## Connection to Goeke Brothers (Siegen, Germany)
analytics.goeke.it was pointed to IP 194.60.201.83 between ~2020-2023 (expired cert 2023-08-17).
Goeke brothers (Elias and Maximilian) run goeke.it/goeke.chat from a SEPARATE server (194.60.201.152).
ASSESSMENT: Stale DNS record from when they previously used that IP, not active collaboration.
They are hobbyist developers with no visible criminal connections.

## Key Personnel
- "Barry" — UK operator, TalkTalk England, machine named AZTEX-BARRY
- Registrant: unknown (Porkbun GDPR-redacted)
