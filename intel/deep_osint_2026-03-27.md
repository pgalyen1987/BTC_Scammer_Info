# Deep OSINT Report — 2026-03-27
**Analyst session:** passive sources only (WHOIS/RDAP, crt.sh, DNS, Shodan InternetDB, HackerTarget, archive.org, web search, GitHub API)

---

## 1. mail-ussl.com — Dedicated Mail Server

### WHOIS
| Field | Value |
|-------|-------|
| Registrar | Hostinger operations, UAB (IANA ID 1636) |
| Created | 2023-07-29 |
| Expires | 2026-07-29 |
| Registrant | REDACTED (privacy) |
| Nameservers | ace.ns.cloudflare.com / lina.ns.cloudflare.com |
| Abuse contact | abuse-tracker@hostinger.com |

**Assessment:** Same Cloudflare nameserver pair as fmtcapitaltc.com — strongly suggests same operator manages both domains through a single Cloudflare account.

### DNS
- `mail-ussl.com` → Cloudflare proxy (104.21.1.194, 172.67.129.222)
- `mx.mail-ussl.com` → **67.216.195.233** (real mail server, bypasses Cloudflare)
- SPF: `"v=spf1 mx -all"` (only own MX is authorised to send)

### crt.sh SANs
Only two names on the certificate: `*.mail-ussl.com` and `mail-ussl.com`. No other domains share the cert — operator is not co-locating other sites on this cert.

### 67.216.195.233 (IT7 Networks / Cluster Logic Inc)
| Field | Value |
|-------|-------|
| Hostname | mx.mail-ussl.com (only hostname via Shodan) |
| ASN | AS25820 IT7 Networks Inc |
| City | Los Angeles, CA, USA |
| Open ports | 25, 80, 110, 143, 443, 465, 993, 995 (full mail stack) |
| Stack | Nginx, Postfix, Bootstrap, jQuery |
| TLS | Self-signed cert |
| Org (ARIN) | Cluster Logic Inc, 4974 Kingsway Ave Suite 668, CA |
| Abuse | abuse@sioru.com / https://www.it7.net/contact/ |

**Assessment:** IT7 Networks is a known bulletproof-adjacent hosting provider. No co-hosted domains found via reverse IP lookup — this server appears to be a dedicated mail relay for the fmtcapitaltc.com operation. Registered July 2023 and still operational March 2026.

---

## 2. 202.79.174.5 — CTG Server HK (Primary Scam Infrastructure)

### IP Geolocation / ASN
| Field | Value |
|-------|-------|
| Location | Tung Chung, Islands District, Hong Kong |
| ASN | AS152194 CTG Server Limited |
| Operator address | 202, 2/F Kam Sang Bldg, 257 Des Voeux Rd Central, HK |
| Also listed | 399 Chai Wan Road, Chai Wan, HK (RACKIP CONSULTANCY PTE. LTD., Singapore) |
| Abuse contact | cs.mail@ctgserver.com |

**Note:** CTG Server's own domain (ctgserver.com) is registered via **Porkbun LLC** — the same registrar used for 2139exchange.com and aztex.eu. This may be coincidental (Porkbun is popular) but worth noting. CTG Server runs 15+ T3 data centers; client portal at myctgs.com; Telegram: @CTGSeverBot.

### Open Ports (Shodan)
22 (SSH/OpenSSH 7.4), 80 (Nginx), 83, 443, **3306 (MySQL 8.0.24 — exposed to internet)**, 8080

### CVEs (selected critical)
MySQL 8.0.24 carries numerous unpatched CVEs (CVE-2024-20961, CVE-2023-22068, CVE-2025-32728, etc.) — indicates no patching discipline.

### All Domains Resolving to 202.79.174.5 (from crt.sh + DNS verification)

**Finance impersonation — US/EU brands:**
- `www.alliancebernsteinn.com` / `ww.alliancebernstseinn.com` (AllianceBernstein typosquat)
- `www.bankofamerilcasl.com` (Bank of America typosquat)
- `www.eatonvancci.com` (Eaton Vance typosquat)
- `www.wellingtonmanageementi.com` / `www.wellingtton.com` (Wellington Management)
- `warburgpiincusii.com` (Warburg Pincus typosquat)
- `www.pimco-tw.com` (PIMCO typosquat) — registered via Name SRS AB (Sweden), IANA ID 638

**Fake broker/fund platforms:**
- `alphaitx.com` — ACTIVE (202.79.174.5); created 2025-07-21; registrar Name SRS AB; NS: A10.SHARE-DNS.COM / B10.SHARE-DNS.NET
- `alphasll.com` — ACTIVE
- `asahisec.com` — ACTIVE; created 2025-09-17; registrar OwnRegistrar Inc; NS: A2.SHARE-DNS.COM
- `hmcapitalv.com` — ACTIVE; created 2025-07-10; registrar Name SRS AB; NS: A2.SHARE-DNS.COM
- `triainvestmentlitd.com` — ACTIVE; created 2025-09-29; registrar Gname.com; NS: A3.SHARE-DNS.COM
- `triainvestmentltc.com` — ACTIVE; created 2025-08-28; registrar Gname.com; NS: A2.SHARE-DNS.COM
- `stratiformsloogan.com` — created 2025-07-01; registrar Name SRS AB; NS: A9.SHARE-DNS.COM
- `stratiformspi.com` / `stratiformsps.com` — created 2025-08-26; registrar Gname.com
- `jpngrowthmarket.com` — created 2025-07-23; Name SRS AB; NS: A11.SHARE-DNS.COM
- `managementcapitalmad.com` — created 2025-08-29; Gname.com
- `bmtmax.com` / `bmtmaxx.com`, `dioep.com`, `sofiils.com`, `tactiib.com`, `tactiiv.com`, `tradiler.com`
- `rw-advisoiry.com`, `www.assetprivfyers.com`, `www.bettermeent-llc.com`

**Japanese FSA impersonation (.jp domains — ACTIVE on HK server):**
- `asahiesecco.jp`, `growthmarket.co.jp`, `www.growthmarket.co.jp`
- `fujieebco.jp`, `fujieemco.jp`, `fujieenco.jp`, `fujifecco.jp`, `fujixecco.jp`, `fujizecco.jp`
- `www.ssonysecoo.jp`

**Malaysian domains:**
- `www.goassetmanagemenntptelttd.my` / variants (multiple typosquats on Go Asset Management)
- `www.goassets-systeem.my` / `www.goassets-system.my`

**Custom TLD .qpon domains:**
- `fsaaiesr.qpon`, `fsaaijsr.qpon`, `fsaaivsr.qpon`, `fsaaixsr.qpon`, `fsazegsr.qpon`, `fsazegsrr.qpon` — all pointing to 202.79.174.5 (confirmed via Shodan hostname)

**Dorfman network (confirmed co-hosted):**
- `www.nanolite-foundationnlf.com` — **ACTIVE on 202.79.174.5** — confirms Dorfman's Nanolite Foundation is physically co-located with the fmtcapitaltc.com CRM management panel on the same HK server

**fmtcapitaltc.com management panel (per prior intel):**
- `broker.fmtcapitaltc.com` — ThinkPHP manager login (now on Cloudflare)
- `trader.fmtcapitaltc.com` — victim CRM (now on Cloudflare)

### Key Infrastructure Finding: SHARE-DNS.COM
All HK server domains share nameservers from the `SHARE-DNS.COM` / `SHARE-DNS.NET` family (A1–A12, B1–B12). This nameserver infrastructure is:
- Registered: 2022-06-30 via Gname.com Pte. Ltd. (Singapore)
- NS for share-dns.com itself: troy.ns.cloudflare.com / ulla.ns.cloudflare.com
- crt.sh shows certs issued: 2025-10-07, 2025-12-05, 2026-02-02
- **This is the single DNS management point for the entire HK CTG server operation**

The two registrars used for all HK-server domains are:
1. **Name SRS AB** (Sweden, IANA ID 638) — abuse@namesrs.com
2. **Gname.com Pte. Ltd.** (Singapore, IANA ID 1923) — complaint@gname.com

Both are reseller registrars commonly used for bulk/anonymous registration.

### 9k9m.com — 2139 Exchange Clone (Same Infrastructure Fingerprint)
- Registered via Gname.com; NS: A.SHARE-DNS.COM — same fingerprint as all HK server domains
- crt.sh: certs from 2022-10-31 through 2025-10-22 (including console, api, t subdomains)
- Now DEAD (DNS not resolving) — shut down after exposure
- Operated same pig-butchering scam as 2139exchange; Italian investigators identified it as a clone

---

## 3. fmtcapitaltc.com — Historical WHOIS and Certificate Analysis

### WHOIS
| Field | Value |
|-------|-------|
| Registrar | Hosting Concepts B.V. d/b/a Registrar.eu (OpenProvider, IANA ID 1647) |
| Created | 2025-08-26 |
| Expires | 2026-08-26 |
| Registrant State | **Wilayah Persekutuan Kuala Lumpur** |
| Registrant Country | **MY (Malaysia)** |
| Registrant name | REDACTED FOR PRIVACY |
| Nameservers | ace.ns.cloudflare.com / lina.ns.cloudflare.com |
| Status | clientTransferProhibited |

**No archive.org snapshots exist** — the site has never been crawled by the Wayback Machine, indicating it uses robots.txt exclusion or Cloudflare bot blocking.

### Certificate History (crt.sh)
| Date | Subject |
|------|---------|
| 2026-02-16 | broker.fmtcapitaltc.com |
| 2026-02-16 | trader.fmtcapitaltc.com |
| 2026-02-19 | *.fmtcapitaltc.com |
| 2026-02-26 | fmtcapitaltc.com, www.fmtcapitaltc.com |

**Assessment:** Domain registered August 2025; management panel (broker) and victim CRM (trader) certificates issued February 2026 — approximately 6 months between registration and operational deployment. The wildcard cert on 2026-02-19 suggests the operator obtained it just days after the individual subdomains were set up.

### Current DNS
- fmtcapitaltc.com, broker., trader., www. → Cloudflare (104.21.91.163 / 172.67.175.136)
- All traffic hidden behind Cloudflare; real origin IP unknown from passive sources

---

## 4. 2139exchange.com — Deep Dive

### WHOIS
| Field | Value |
|-------|-------|
| Registrar | Porkbun LLC (IANA ID 1861) |
| Created | 2024-07-08 |
| Expires | 2026-07-08 |
| Registrant | REDACTED |
| Nameservers | curitiba/fortaleza/maceio/salvador.ns.porkbun.com |
| Status | clientDeleteProhibited, clientTransferProhibited |

### Certificate History (crt.sh)
Subdomains issued in sequence (all 2025):
- 2025-11-01: portal.2139exchange.com
- 2025-11-02: hr.2139exchange.com
- 2025-11-09: sharepoint.2139exchange.com
- 2025-11-13: wwww.2139exchange.com
- 2025-11-30: www.sharepoint.2139exchange.com
- 2026-01-16: dev.2139exchange.com
- 2026-01-26: www.2139exchange.com
- 2026-01-30: intranet.2139exchange.com
- 2026-01-31: api.2139exchange.com
- **2026-03-19: 2139exchange.com** (main domain cert — most recent)

**Assessment:** The subdomain structure (hr, portal, sharepoint, intranet, dev) mirrors a corporate IT environment — this is deliberate deception to appear legitimate and mirrors the same aaPanel/BaoTa Chinese panel structure seen at aztex.eu (Nextcloud, Matrix, RDP). The March 2026 cert coincides with migration to VEESP after CONSOB action.

### Current Hosting
- 2139exchange.com → **185.22.174.75** (SIA VEESP, Riga, Latvia, AS42532)
- All subdomains are DEAD (DNS not resolving) — only main domain still live
- VEESP cert: 2026-03-19 (very recent, post-CONSOB blackout migration)

### Scale and Regulatory Actions
- **CONSOB Italy** blacklisted 2024-09-20; additional domain blackouts through October 2024
- Estimated **100,000+ victims globally**, at least **20,000 in Italy**
- Italy's worst-hit city: Lecce (Salento/Apulia region); individual losses up to €100,000
- On-chain analysis: **>$27 million** traced toward Binance; total estimate **$50–420 million** stolen
- Telegram channels used: "2139" and "Mega Investment" (Italian-language recruitment)
- Italian promoter persona: "Mentor Claus" (unverified real identity)
- Platform claimed false registration with ACRA (Singapore), SEC (US), FinCEN (US)
- All variant domains now dead: 2139.lol, 2139a.com, 2139.nl, 2139.one

### Linked Platforms
- **megat.vip** (Mega Investment Group) — confirmed linked via same Telegram channels
- **9k9m.com** — confirmed clone using identical SHARE-DNS infrastructure
- **"Dolphin" exchange** — also linked per prior intel

---

## 5. megat.vip / megaig.vip — Mega Investment Group

### megat.vip WHOIS
- WHOIS returns "No Data Found" — domain appears dropped or under registry lock
- Archive.org: last snapshot 2024-10-03 (available)
- crt.sh: certs from 2023-05-21 through 2024-10-23

### megaig.vip WHOIS (active domain)
| Field | Value |
|-------|-------|
| Registrar | Go Montenegro Domains LLC (IANA ID 1152), via goitalydomains.com |
| Created | 2023-05-08 |
| Expires | 2026-05-08 |
| Registrant | Domains By Proxy LLC (GoDaddy privacy), Arizona, US |
| Status | clientHold, clientDeleteProhibited, clientTransferProhibited, clientRenewProhibited, clientUpdateProhibited — **SUSPENDED** |

**Assessment:** megaig.vip is under registry hold (suspended). The use of GoDaddy privacy protection and an obscure Montenegro registrar is characteristic of the operation's registrar-hopping pattern.

### KEY FINDING: Contact Email
The archived megat.vip page (2024-10-03 snapshot) contains a Cloudflare-encoded email that decodes to:
**`admin@megaig.vip`**

This email appears three times on the page (likely in contact, footer, and mailto links). This is the primary operator contact for the Mega Investment Group platform.

### Fabricated Corporate Identity
From archive.org snapshot of megat.vip:
- Founder: **"Logan Smith"** (fictitious — stock photo used)
- Founded: 2015, Denver USA (false)
- Fake team members with stock photos: Adam Taylor (joined 2022), Aditsan Lewis, Conrad Wilson, Georgina Smith, Cecilia Rosa, Bena Rishi
- Claimed offices: Los Angeles, San Francisco, London, Paris, Mumbai, Hong Kong, Tokyo
- Claims total AUM of ~$98.2 billion as of September 2007 (lifted verbatim from a legitimate fund description)
- The description appears to be plagiarised from a legitimate asset manager's marketing materials

### Current Status
- megat.vip: DNS dead
- megaig.vip: DNS dead, registry suspended
- admin@megaig.vip: Only contact identifier obtained from public sources

---

## 6. aztex.eu + aztexchange.com

### aztex.eu WHOIS
- Registrar: **Porkbun LLC** (same as 2139exchange.com)
- Technical contact: support@porkbun.com
- Registrant: NOT DISCLOSED (EURid policy)
- Nameservers: Porkbun Brazilian nameservers

### aztex.eu Certificate History (crt.sh — complete timeline)
| Date | Subdomain |
|------|-----------|
| 2021-03-03 | cpanel, autodiscover, webdisk, webmail, cpcalendars, cpcontacts |
| 2021-09-16 | somegoodnews.aztex.eu, www.somegoodnews.aztex.eu |
| 2022-10-06 | twenty48.aztex.eu, www.aztex.eu |
| 2022-10-08 | owncloud.aztex.eu |
| 2023-03-09 | **route-finder.aztex.eu** |
| 2023-07-07 | **route-lister.aztex.eu** |
| 2023-10-18 | *.aztex.eu |
| 2025-07-22 | mail.aztex.eu |
| 2025-11-16 | nextcloud.aztex.eu, admin.nextcloud.aztex.eu |
| 2025-11-17 | ninjazz.aztex.eu |
| 2025-12-05 | jukem.aztex.eu |
| 2025-12-10 | matrix.aztex.eu |
| 2025-12-14 | rdp.aztex.eu |
| 2026-02-19 | aztex.eu, **bitwarden.aztex.eu** |

### KEY FINDING: Jonas Hagmar — aztex.eu Server Owner
The subdomain `ninjazz.aztex.eu` hosts a WebAssembly/WebGL/WebXR experiment. Its archived content (2025-02-14 snapshot) contains:

> **"Copyright 2022 Jonas Hagmar — [git repo](https://github.com/jhagmar/ninjazz)"**

GitHub API confirms:
- GitHub handle: **jhagmar**
- Full name: **Jonas Hagmar**
- Email (from git commits): **jonas.hagmar@gmail.com**
- Public repos include: ninjazz (WebAssembly demo), twenty48 (2048 game demo hosted on twenty48.aztex.eu), cryptkeyper, keynjector, alacritty-config, astronvim-customization
- LinkedIn: Jonas Hagmar — Research Engineer, Fraunhofer-Chalmers Centre, Göteborg, Sweden; also "Industrial Path Solutions - IPS"
- ResearchGate: Jonas B.A. Hagmar, Fraunhofer-Chalmers Centre, Göteborg

**Assessment:** Jonas Hagmar appears to be a legitimate Swedish software engineer and researcher who owns/operates the aztex.eu VPS. His personal projects (ninjazz, twenty48, owncloud, obsidian) are hosted alongside the AZTEX criminal exchange operation. This raises several possibilities:
1. Hagmar operates the criminal exchange as a side operation (unlikely given his professional profile)
2. Hagmar's server was compromised and used without his knowledge (possible)
3. "Barry" (the AZTEX operator identified via TalkTalk UK) rents hosting from Hagmar or uses his server legitimately for the exchange frontend while managing backend elsewhere

**The route-finder and route-lister tools (2023) are the most suspicious** — these coincide exactly with the BIPPAX active period and do not appear in Hagmar's GitHub repos. They may have been deployed by a separate operator ("Barry") who had access to the server.

Hagmar should be contacted by investigators as a witness/server owner who may have logs, not treated as a primary suspect without further evidence.

### aztex.eu Current Hosting (Contabo FR)
| Field | Value |
|-------|-------|
| IP | 194.60.201.83 |
| Provider | Contabo GmbH, Welfenstrasse 22, 81541 Munich, Germany |
| Abuse | abuse@contabo.de |
| Shodan hostname | mail.aztex.eu |
| Open ports | 22, 80, 143, 465, 587, 993, 3389 |
| Stack | Ubuntu Linux, Golang, Caddy web server, OpenSSH 9.6p1 |
| RDP | Port 3389 — Remote Desktop Protocol active |

**Note:** Port 3389 (RDP) is open — consistent with previous finding that the AZTEX operation uses RDP for remote administration.

### aztex.digital — NEWLY DISCOVERED DOMAIN
Found via Shodan hostname on Hetzner server 37.27.206.233: `not-front-contest.aztex.digital`

crt.sh for aztex.digital:
| Date | Subdomain |
|------|-----------|
| 2022-10-27 | www.aztex.digital |
| 2025-06-12 | not-front-contest.aztex.digital |
| 2025-06-14 | obsidian.aztex.digital |
| 2025-06-25 | project-omikami.aztex.digital |
| 2025-07-12 | slepsk.aztex.digital |
| 2025-11-13 | project-cheapeats.aztex.digital |
| 2025-12-01 | *.aztex.digital, aztex.digital |

WHOIS: .digital TLD — registry data not accessible via standard whois; RDAP returned error.

The subdomain names suggest development projects:
- `project-omikami` — possibly linked to Omikami crypto token (separate project)
- `project-cheapeats` — food/delivery app project
- `not-front-contest` — possibly a coding contest submission
- `slepsk` — unknown; could be a username or place name
- `obsidian` — likely Obsidian note-taking app instance

**Assessment:** aztex.digital appears to be the same operator as aztex.eu (Jonas Hagmar), running personal development projects. The `slepsk` subdomain is unidentified and warrants further investigation as a potential username.

### aztexchange.com
- Registrar: Realtime Register B.V. (IANA ID 839)
- Created: **2026-03-01** (very recently registered)
- Status: **clientHold** — SUSPENDED immediately after registration
- NS: NS1/NS2.SUSPENDED-DOMAIN.COM — registrar has suspended it
- crt.sh: wildcard cert issued 2026-03-01 (same day as registration)
- **Assessment:** This domain was registered, issued a wildcard TLS cert, and suspended almost immediately — likely within days. This suggests the registrar or an abuse reporter flagged it rapidly. The operator may have been attempting to create a new domain after aztex.eu came under scrutiny.

---

## 7. 37.27.206.233 — Hetzner HEL Server

| Field | Value |
|-------|-------|
| Provider | Hetzner Online GmbH, Helsinki, Finland (AS24940) |
| Abuse | abuse@hetzner.com |
| Hostname (Shodan) | not-front-contest.aztex.digital |
| Stack | Ubuntu Linux, MinIO (S3-compatible object storage, ports 9000/9001), Pure-FTPd (port 21), OpenSSH 9.6p1, Nginx-based load balancer |
| Open ports | 21, 22, 443, 887, 9000, 9001 |

**Port 887:** Non-standard port, purpose unknown from passive sources. Could be a custom API or management interface.

**MinIO on ports 9000/9001:** S3-compatible storage — may be used to store scam site assets, victim documents, or backups of the exchange database.

**crt.sh for 37.27.206.233:** Only one cert found: `37.27.206.233` issued 2026-01-26 (self-signed to IP address directly).

**Assessment:** This server is co-located with aztex.eu by the same operator (aztex.digital domain). It runs file storage (MinIO, FTP) which could serve as a staging environment or file drop for the operation. No exchange-specific domains currently resolve here.

---

## 8. Search Results — Scam Databases and Forums

### fmtcapitaltc.com
- No results found on Google, Bitcoin Talk, Reddit, DFPI crypto scam tracker, or any complaint database
- The domain has NO web presence indexed by search engines
- No archive.org snapshots exist
- Assessment: Very new operation (domain August 2025, certs February 2026), not yet widely reported

### 2139exchange.com
- **DFPI California:** Not listed in crypto scam tracker as of 2026-03-27
- **CONSOB Italy:** Blacklisted 2024-09-20; multiple additional domain blackouts through October 2024
- **Trustpilot:** Extensive complaints at 2139.com and 2139.ltd
- **BrokersView:** Marked SCAM; false regulatory claims documented
- **Scale:** 100,000+ global victims; 20,000+ in Italy; up to $420M total losses estimated; $27M+ traced on-chain toward Binance

### megat.vip
- brokerprofile.net: Reviewed and flagged as scam ("MEGA INVESTMENT GROUP — Avoid")
- Confirmed linked to 2139 exchange via same Telegram channels
- No entries in DFPI or IC3 databases found

### aztex.eu
- No results on Google/Bing for "aztex.eu" in scam/fraud context
- Trustpilot shows reviews for a completely unrelated "aztex.ee" (Estonian textile company)
- aztexchange.com was domain-suspended (clientHold) by Realtime Register — possibly following an abuse report

---

## 9. ThinkPHP Fingerprint Analysis

### fmtcapitaltc.com Stack
- Framework: ThinkPHP (Chinese PHP framework, heavily used in Chinese-developed exchange backends)
- PHP version: 7.4.33 (end of life, no security updates since November 2022)
- Server: Nginx (behind Cloudflare)

### Passive Findings
- **No archive.org snapshots** of broker.fmtcapitaltc.com or trader.fmtcapitaltc.com exist
- **HackerTarget hostsearch** confirms: broker.fmtcapitaltc.com → 104.21.91.163, trader.fmtcapitaltc.com → 172.67.175.136, www.fmtcapitaltc.com → 172.67.175.136 (all Cloudflare)
- No exposed ThinkPHP error pages found via passive sources

### ThinkPHP Codebase Significance
ThinkPHP-based exchange platforms are widely available on Chinese code-sharing platforms (Gitee, etc.) as "exchange source code" packages. The use of PHP 7.4.33 (EOL) and ThinkPHP strongly indicates Chinese developer origin or use of commercially available exchange source code packages. This is consistent with the aaPanel/BaoTa panel at 2139exchange.com (also Chinese-origin server management software).

---

## 10. Key Identifiers Summary

### Personal Identifiers Found

| Identity | Source | Confidence |
|----------|--------|------------|
| **Jonas Hagmar** — Swedish developer, Research Engineer at Fraunhofer-Chalmers Centre, Göteborg | aztex.eu server owner (ninjazz copyright + GitHub jhagmar) | HIGH — verified via GitHub API |
| **jonas.hagmar@gmail.com** | Git commits in jhagmar/ninjazz and jhagmar/twenty48 repos | HIGH — verified |
| **admin@megaig.vip** | Cloudflare-encoded email decoded from archived megat.vip | HIGH — verified via CF decode |
| **"Logan Smith"** — fictitious founder of Mega Investment Group | megat.vip archive | LOW — confirmed fake identity |
| **"Mentor Claus"** — Italian promoter persona for 2139 exchange | Italian press reports | LOW — persona only |
| AZTEX Barry, Southend-on-Sea, Essex SS1 | TalkTalk IP 79.78.160.133 + MikroTik router ports | MEDIUM — static residential/office IP |

### Infrastructure Clusters

**Cluster A — fmtcapitaltc.com / CTG HK Operation**
- fmtcapitaltc.com (Cloudflare, registrar Registrar.eu, country MY/Kuala Lumpur)
- mail-ussl.com → 67.216.195.233 (IT7 Networks LA, Hostinger registrar)
- 202.79.174.5 (CTG Server HK) — hosts ~50+ scam domains including Dorfman's Nanolite
- All CTG-server domains use SHARE-DNS.COM nameservers (Gname.com/Name SRS AB registrars)
- ThinkPHP / PHP 7.4.33 / aaPanel stack suggests Chinese developer origin

**Cluster B — 2139exchange.com / Mega Investment Group**
- 2139exchange.com → 185.22.174.75 (VEESP Latvia, Porkbun registrar)
- megat.vip / megaig.vip — suspended/dead; contact: admin@megaig.vip
- 2139exchange.com cert: 2026-03-19 (post-CONSOB migration to VEESP)
- All variant domains dead: 2139.lol, 2139a.com, 2139.nl, 2139.one
- Scale: $50–420M stolen; 100,000+ victims; CONSOB blacklisted

**Cluster C — AZTEX Operation**
- aztex.eu → 194.60.201.83 (Contabo FR, Porkbun registrar)
- aztex.digital → 37.27.206.233 (Hetzner HEL)
- aztexchange.com — registered 2026-03-01, immediately suspended
- TalkTalk UK IP 79.78.160.133 (Southend-on-Sea SS1, MikroTik router)
- Server owner likely: Jonas Hagmar (jonas.hagmar@gmail.com) — may be witness not perpetrator

**Cluster D — Dorfman Network (cross-cluster)**
- nanolite-foundationnlf.com hosted on CTG HK server alongside fmtcapitaltc management panel
- Confirms Dorfman's operation shares HK infrastructure with fmtcapitaltc operator

---

## 11. Registrar and Nameserver Patterns

| Registrar | IANA ID | Domains |
|-----------|---------|---------|
| Porkbun LLC | 1861 | 2139exchange.com, aztex.eu, ctgserver.com |
| Hostinger operations UAB | 1636 | mail-ussl.com |
| Registrar.eu (OpenProvider) | 1647 | fmtcapitaltc.com |
| Gname.com Pte. Ltd. | 1923 | 9k9m.com, triainvestmentltc.com, triainvestmentlitd.com, managementcapitalmad.com, stratiformspi.com, stratiformsps.com, share-dns.com |
| Name SRS AB | 638 | alphaitx.com, hmcapitalv.com, jpngrowthmarket.com, pimco-tw.com, stratiformsloogan.com |
| OwnRegistrar Inc. | 1250 | asahisec.com |
| Realtime Register B.V. | 839 | aztexchange.com (suspended) |
| Go Montenegro Domains LLC | 1152 | megaig.vip (suspended) |

---

## 12. Recommended Follow-Up Actions

1. **Jonas Hagmar contact:** Approach as a witness — he may have server access logs covering the route-finder/route-lister period (2023) that could identify the AZTEX operator who deployed those tools on his server. Contact via jonas.hagmar@gmail.com.

2. **admin@megaig.vip:** This is the only operator-linked email found. Attempt OSINT breach-database and HUMINT approaches. Check for this email in public data breach compilations.

3. **TalkTalk UK abuse report:** The Southend-on-Sea static IP 79.78.160.133 (AS13285 TalkTalk) with MikroTik router suggests a fixed business connection. UK law enforcement with a production order to TalkTalk could identify the subscriber at this address. Ports 8291/8728 (MikroTik Winbox/API) confirm this is a MikroTik-managed connection — not a datacenter.

4. **SHARE-DNS.COM investigation:** All HK-server domains use this custom nameserver. Gname.com (registrar of share-dns.com) should be compelled to identify the registrant and/or owner of this nameserver infrastructure.

5. **Contabo abuse report:** The aztex.eu mail server (194.60.201.83) at Contabo runs RDP (3389) and a full mail stack. Contabo (abuse@contabo.de) may have KYC data on the account holder.

6. **IT7 Networks / Cluster Logic:** abuse@sioru.com or https://www.it7.net/contact/ for the mail-ussl.com server (67.216.195.233). May have account/payment data for the fmtcapitaltc operator.

7. **CTG Server HK:** cs.mail@ctgserver.com — may have customer records for whoever rents the 202.79.174.5 server and the ~50 scam domains. Registered via Porkbun which has abuse@porkbun.com.

8. **Crypto on-chain:** Italian investigators traced $27M+ toward Binance. Binance SAR requests may have operator KYC if they used a Binance OTC desk.

---

*Sources: WHOIS/RDAP, crt.sh certificate transparency, Shodan InternetDB, HackerTarget, ipinfo.io, DNS (dig), archive.org, GitHub API, web search (Google, DuckDuckGo), decripto.org, brokersview.com/fastbull.com, brokerprofile.net, financemagnates.com — all passive/public sources. No unauthorized access attempted.*
