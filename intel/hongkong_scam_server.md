# Hong Kong Scam Server — Intelligence File
*Created: 2026-03-26*

## Server Details

- **IP:** 202.79.174.5
- **Hostname:** fsazegsrr.qpon (random/generated)
- **Location:** Tung Chung, Hong Kong (Islands district)
- **ASN:** AS152194 CTG Server Limited
- **Type:** Bare-metal VPS with exposed database

## Open Ports (Shodan InternetDB)
| Port | Service | Notes |
|------|---------|-------|
| 22 | SSH OpenSSH 7.4 | Old version (2016), multiple CVEs |
| 80 | HTTP Nginx | Web server |
| 83 | HTTP | Alternate web port |
| 443 | HTTPS Nginx | TLS |
| 3306 | **MySQL 8.0.24** | **EXPOSED TO INTERNET — SEVERE MISCONFIGURATION** |
| 8080 | HTTP | Alternate web port |

**MySQL CVEs present:** CVE-2022-21278, CVE-2023-22078, CVE-2024-21171, and ~100 others
**SSH CVEs:** CVE-2018-20685, CVE-2019-6109/6110/6111, CVE-2023-38408 (OpenSSH RCE), CVE-2023-51385, CVE-2023-48795 (Terrapin), CVE-2025-26465

## Confirmed Hosted Domains (Reverse IP — hackertarget)
All confirmed as fake investment/finance scam sites:

### Priority Targets (Impersonating Major Institutions)
- **www.alliancebernsteinn.com** — typosquat of AllianceBernstein (NYSE: AB, $700B AUM legitimate fund manager)
- **ww.alliancebernstseinn.com** — second typosquat variant
- **www.alliancebernstseinn.com** — third typosquat variant
- **www.bankofamerilcasl.com** — typosquat of Bank of America
- **www.eatonvancci.com** — typosquat of Eaton Vance (institutional asset manager)
- **www.pimco-tw.com** — typosquat of PIMCO (Pacific Investment Management, Taiwan-targeted)
- **www.jpngrowthmarket.com** — Japan Growth Market (targeting Japanese investors)

### nanolite-foundationnlf.com ⭐ KEY DOMAIN
- BaFin-warned WhatsApp investment scam (Germany)
- Registered by Darryl Joel Dorfman (Colorado)
- **HTTrack copy of hvcapital.com** (legitimate German VC firm) made May 28, 2025
- Hardcoded token in JS: `TOKEN:"PpAz5O26OlepQn8sRcL2qgtt"` (do NOT use — for law enforcement only)
- React/Next.js frontend
- Phone number extracted: 573001782 (country code unknown — could be 57 Colombia + number, or other)

### Other Co-Hosted Scam Domains
- alphaitx.com — fake exchange/investment
- alphasll.com — fake finance
- asahisec.com — "Asahi Security" fake firm
- www.assetprivfyers.com — "Asset Privacy" fake
- www.assetpvfyers.com — variant
- www.bettermeent-llc.com — fake LLC
- www.bmtmax.com / www.bmtmaxx.com — fake exchange
- www.dioep.com — unknown
- hmcapitalv.com — "HM Capital" fake
- www.managementcapitalmad.com — fake management
- www.rw-advisoiry.com — "RW Advisory" fake
- www.sofiils.com — typosquat of SoFi (fintech)
- www.stratiformsloogan.com / www.stratiformspi.com / www.stratiformsps.com — multiple variants
- en.stratiformspi.com / en.stratiformsps.com — English versions
- admin.stratiformsloogan.com — ADMIN PANEL exposed on public reverse IP
- www.tactiib.com / www.tactiiv.com — fake platforms
- www.tradiler.com — unknown trading fake

## Key Intelligence
1. **MySQL port 3306 is publicly exposed** — database access point (requires lawful authority to access)
2. **~30 fake finance sites on one server** — organized fraud operation, not isolated
3. **admin.stratiformsloogan.com** — admin subdomain appearing in reverse IP indicates backend infrastructure
4. Server has NO CDN/WAF — direct IP access possible
5. Multiple old CVEs in SSH and MySQL suggest server is not well-maintained (may still be running vulnerable versions)

## Domain Registration Intelligence

### nanolite-foundationnlf.com
- Registered: **2025-08-06** via **NameSilo LLC (Arizona, USA)** — abuse@namesilo.com
- Nameservers: NS1/NS2/NS3.DNSOWL.COM (NameSilo's own DNS)
- 1-year registration, expires 2026-08-06
- **Subpoena target: NameSilo LLC (US company, 18 USC §2703)**

### Hong Kong co-hosted scam domains (bankofamerilcasl.com, alliancebernsteinn.com, jpngrowthmarket.com, pimco-tw.com etc.)
- All registered July-October 2025 (1-year terms)
- Registrars: **Name SRS AB (Sweden)** and **Gname.com Pte. Ltd. (Singapore)**
- All use **SHARE-DNS.COM/NET nameservers** (Chinese DNS provider) — shared fingerprint
- This DNS fingerprint can identify other domains on the same Chinese operator account

## fmtcapitaltc.com Platform Intelligence (2026-03-26)
- **Technology:** ThinkPHP (Chinese PHP MVC framework) — confirmed via `X-Powered-By: ThinkPHP` header
- **Admin panel:** `broker.fmtcapitaltc.com` → title "manager-login", form `/admin/login/action`, HTML comment `登录界面` (Chinese: "Login interface"), PHP/7.4.33 (EOL)
- **Victim CRM:** `trader.fmtcapitaltc.com` → meta "CRM", 8+ languages including Arabic, uploaded content from 2024-11-14 (platform active Nov 2024)
- **MX record:** mx.mail-ussl.com → real SMTP at **67.216.195.233** (IT7 Networks Inc, Los Angeles CA, AS25820)
- **mail-ussl.com registered:** 2023-07-29 via Hostinger operations UAB (Lithuania) — predates fmtcapitaltc.com by 2 years
- **Copyright 2019** on domain registered 2025-08-26 = reused Chinese scam template

## Subpoena Targets
- **CTG Server Limited** (Hong Kong) — server logs, account holder, payment method, all hosted domains
- **HKICECC** (Hong Kong Internet Crime Complaints Centre) — local law enforcement referral
- **Hong Kong Police Cyber Security Division** (cybercrime@police.gov.hk) — direct referral
- **NameSilo LLC** (Scottsdale, AZ — US company) — nanolite-foundationnlf.com registrant identity (18 USC §2703)
- **Name SRS AB** (Sweden) + **Gname.com Pte. Ltd.** (Singapore) — registrar identity for co-hosted scam domains
- **IT7 Networks Inc** (Los Angeles, CA — US company) — mail-ussl.com SMTP server account (18 USC §2703)
- **Hostinger operations, UAB** (Lithuania) — mail-ussl.com registrar
- **Registrar.eu / Hosting Concepts B.V.** (Netherlands, abuse@registrar.eu, +31.104482297) — fmtcapitaltc.com registrar
- If CTG Server Limited refuses: **FBI via MLAT to Hong Kong** (HK has MLAT with US via 1997 agreement)
