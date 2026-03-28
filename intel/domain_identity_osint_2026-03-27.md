# Domain Identity OSINT — 2026-03-27
*Passive OSINT only. All data from public sources: WHOIS, DNS, crt.sh, ARIN.*

---

## TOP IDENTITY LEADS

### 1. rw-advisoiry.com — Google Site Verification Token (HIGH PRIORITY)
- **TXT record:** `google-site-verification=oSrrYkACtk3M2QyHUk1u1VlM5qiB5zq7quVYBxF2kto`
- **Significance:** The operator added this token to verify ownership in Google Search Console. A subpoena to Google for which account verified this token would yield a real identity (Google account name, recovery email, IP logs).
- **Domain status:** Currently not resolving (no A record found) — dormant/abandoned
- **Domain:** Typosquat of RW Baird (real financial firm)

### 2. ssonysecyco.jp — Non-Redacted Registrant Name (HIGH PRIORITY)
- **Registrant Name:** **tian cixue** (Chinese personal name — not a company)
- **Registrar:** Web Commerce Communications Limited (WebNIC, Malaysia) — IANA 460
- **Address given:** 3-9-3 Nishishinjuku, Shinjuku-ku, Tokyo, 1600023
- **Phone:** +603.89966788 (Malaysia country code — address likely false)
- **Created:** 2025-09-04 | Expires: 2026-09-30 | Status: Active
- **Note:** Only non-privacy-protected human name found across all criminal domains in this network. Tokyo address with Malaysian phone is inconsistent.
- **Domain:** Typosquat of Sony Securities Japan

### 3. fujieebco.jp — Same Registrar, SHARE-DNS Infrastructure
- **Registrant:** Web Commerce Communications Limited (corporate cover, no personal name)
- **NS:** a12.share-dns.com / b12.share-dns.net
- **Created:** 2025-08-20 | Expires: 2026-08-31 | Status: Active
- **Note:** Registered ~2 weeks before ssonysecyco.jp via same WebNIC account
- **Domain:** Typosquat of Fujie & Co. (Japanese securities firm)

---

## INFRASTRUCTURE IDENTITY LINKS

### betaglobalmanagements.com — BIPPAX / Beta Global Finance
- **SOA:** `ns1.servikus.com. noc.servikus.com.` (Servikus LLC hosting confirmed)
- **SPF IPs:**
  - `23.138.140.66` → Servikus LLC (ARIN SL-2224)
  - `173.208.178.96` → WholeSale Internet / NOCIX (PTR: `173-208-178-96-s10.servikus.net`)
  - `173.208.178.66` → Same NOCIX block, Servikus-resold
- **MX → 173.208.178.96** (Servikus mail relay)
- **crt.sh:** Cert issued for `www.betaglobalmanagements.com.pipgainers.com` — proves pipgainers.com is the cPanel server hosting this domain

### pipgainers.com — Shared Servikus Server (HIGH VALUE)
- **SOA:** `ns1.servikus.com. noc.servikus.com.` (identical to betaglobalmanagements.com — same account)
- **First cert:** 2025-04-22 | **Total certs:** 174 as of 2026-03-27 — very active
- **Co-hosted domains** (crt.sh SAN enumeration — 26+ domains, same Servikus cPanel account):
  - `elevateglobalmarkets.com` (cert 2026-03-24 — most recently active)
  - `econtrader.net`, `managementofficial.com`, `toppairassets.com` (cert 2026-03-21)
  - `swiftcouriercompany.net`, `statetitleescrowservicesinc.com` (fake courier/escrow)
  - `pioneerfinancescu.com`, `pdbfinances.com`, `acseinvestmentsllc.com`
  - `colerealestategroupsllc.com`, `homeescrowservicellc.com`
  - `muskfoundationpartners.org` (fake Elon Musk foundation)
  - `ap3investmentsllc.com`, `regionalsaving.com`, `profitpeakcapital.com`
  - `protradeoptions.org`, `toptiercapital.live`, `topexpertspro.live`
  - `rubiescu.com`, `bluemach.engineering`, `colerealestategroupsllc.co`
  - `slrfinancesllc.com`, `anthemtitlesettlementscompanyllc.com`, `jonesinvestmentscompany.com`
  - `protradeoptions.live`, `votalityfx.com` (FX scam, alt IP 185.53.179.136)
  - `betaglobalmanagements.com` (BIPPAX) — proven via `www.betaglobalmanagements.com.pipgainers.com` SAN
- **Significance:** All 26+ scam operations share one Servikus cPanel account; WHOIS privacy-redacted on all but same registrar (Registrar.eu) and same nameservers (ns1–4.servikus.com)

### dacm-crypto.top — Russian Infrastructure
- **SOA nameserver:** `isp4.ru.fastfox.pro` → resolves to `94.26.255.20` (Selectel.ru, Russia)
- **Web IP:** `94.26.255.20` → Selectel Network (abuse: abuse@selectel.ru)
- **SPF mail IP:** `95.213.216.170` → Selectel Network (St. Petersburg)
- **Mail IP:** `94.26.255.20` (same as web — single server)
- **fastfox.pro:** `185.137.235.134` → also Selectel.ru
- **WHOIS registrant country:** CI (Côte d'Ivoire) — likely spoofed
- **Registrar:** Atak Domain Bilgi Teknolojileri Inc. (Turkey)
- **Created:** 2025-10-27 | certs renewed: 2025-12-27, 2026-02-26
- **Assessment:** Russian-operated, Turkish-registered, fake African country — multi-layer jurisdiction confusion

---

## WHOIS SUMMARY BY DOMAIN

| Domain | Registrar | Created | NS / Hosting | Notes |
|--------|-----------|---------|-----|-------|
| cappofx.com | GoDaddy (Domains By Proxy) | 2023-02-17 | Cloudflare | Elastic Email SPF (bulk mail); GoDaddy privacy |
| mumuex.org | Galcomm | 2025-04-29 | abovedomains.com | Parked; IP 103.224.212.214 (Trellian AU) |
| chieftoptrading.com | Name SRS AB (Sweden) | 2025-07-09 | SHARE-DNS (a9/b9) | clientHold — suspended |
| adamsstreetpartnersi.com | Gname.com | 2025-07-06 | SHARE-DNS (a/b) | clientHold — suspended |
| triainvestmentltc.com | Gname.com | 2025-08-28 | SHARE-DNS | Active |
| pimco-tw.com | Name SRS AB | 2025-08-01 | SHARE-DNS (a7/b7) | Active |
| alphaitx.com | Name SRS AB | 2025-07-21 | SHARE-DNS | Active |
| welliingttons.com | Metaregistrar | 2025-11-14 | unknown | Active |
| fujieebco.jp | WebNIC | 2025-08-20 | SHARE-DNS (a12/b12) | Active |
| ssonysecyco.jp | WebNIC | 2025-09-04 | none (blank NS) | Active but no A record |
| dacm-crypto.top | Atak Domain (Turkey) | 2025-10-27 | fastfox.pro / Selectel RU | Russian hosting |
| byxgexchange.com | — | expired | — | No WHOIS match — dropped |
| byxgcoins.com | — | expired | — | No WHOIS match — dropped |
| bippaxcoins.com | — | expired | — | No WHOIS match — dropped |
| userhelpsdesk.com | — | expired | — | No WHOIS match — dropped |
| aztexchange.com | Realtime Register (NL) | 2025? | unknown | Updated 2026-03-03, still active |
| 2139a.com | — | expired | — | No WHOIS match — dropped |
| 2139.nl | Key-Systems GmbH (DE) | 2025-09-17 | parklogic.com | Parked domain |
| share-dns.com | Gname.com | 2022-06-30 | Cloudflare | Expires 2027; updated 2026-03-25 |
| share-dns.net | Gname.com | 2022-06-30 | Cloudflare | Expires 2027 |

---

## DNS / SPF FINGERPRINTS (High-value)

### aztex.eu — Contabo FR confirmed
- **SPF:** `v=spf1 ip4:194.60.201.83 ip6:2a02:c207:2298:2627::1/64 include:_spf.porkbun.com -all`
- Confirms 194.60.201.83 is authorized mail sender for aztex.eu

### 2139exchange.com
- **SOA:** `curitiba.ns.porkbun.com` (Porkbun registrar, same as aztex.eu — confirms same operator)

### cappofx.com
- **SPF:** `v=spf1 a mx include:_spf.elasticemail.com ~all`
- **MX:** secureserver.net (GoDaddy)
- Elastic Email = bulk commercial email — used for mass victim outreach

### SHARE-DNS cluster (alliancebernsteinn.com, eatonvancci.com, pimco-tw.com, wellingtton.com, etc.)
- **SOA admin:** master.share-dns.com (all SHARE-DNS operated)
- SOA serials in 1750000000–1766000000 range = mid-2025 registration batch

---

## SERVIKUS LLC — HOSTING PROVIDER FOR BIPPAX/PIPGAINERS GROUP

ARIN RDAP record (handle: SL-2224):
- **Address:** 99 Wall Street #5005, New York, NY 10005 (virtual office address)
- **Phone:** +1-914-705-7374 (Westchester area code)
- **Tech/Abuse:** arin@servikus.com / abuse@servikus.com
- **Domain:** servikus.com — NameSilo registrar, created 2010-07-07
- **Confirmed clients:** betaglobalmanagements.com, pipgainers.com + cluster

---

## GNAME.COM PTE. LTD. — REGISTRAR CONTEXT

- **UEN:** 202013923E (Singapore, incorporated 2020-05-19)
- **Address:** 8 Temasek Boulevard #21-04 Suntec Tower Three, Singapore 038988
- **Public leadership:** "Ms. Mandy" (Business Leader), "Mr. Johnson" (Marketing Director) — no full names published
- **NetBeacon Institute (March 2025):** Named as top-abused registrar — 9% of malicious phishing domains while holding only 2% of all gTLD domains
- **Abuse contact:** complaint@gname.com / +65.65189986
- **Note:** zys@gname.com is an old Gname registrar abuse contact email associated with ~104,554 domains (entire customer base, not specifically criminal)

## WEB COMMERCE COMMUNICATIONS (WEBNIC.CC) — IANA 460

- **Registrar for:** ssonysecyco.jp, fujieebco.jp
- **NetBeacon (May 2025):** 6% of malicious phishing while <1% of market share
- **HQ:** Malaysia (Kuala Lumpur area, +603 country code)

---

## SHARE-DNS INFRASTRUCTURE FACTS

- **share-dns.com + share-dns.net:** Both registered Gname.com, same day (2022-06-30), expire 2027-06-30
- **RDAP last update:** 2026-03-25 (actively maintained)
- **mail.share-dns.net:** 35.215.163.95 → Google Cloud AS15169, Hong Kong
- **SPF (share-dns.net):** `v=spf1 ip4:35.215.163.95 -all`
- **All NS pairs (a1–a15 / b1–b15):** Cloudflare Anycast (172.64.53.25 / 172.64.52.239)
- **Palo Alto Unit 42:** share-dns named in 2024 report on Olympic-themed gambling campaign — "All gambling domains are resolved by the same DNS hosting service (share-dns), suggesting a potential connection between the operators."
- **Cert history:** Continuous from 2022-07-04 through 2026-02-02; Google Trust Services, Let's Encrypt, Sectigo

---

## DMARC / EMAIL ENFORCEMENT

| Domain | DMARC | Risk |
|--------|-------|------|
| betaglobalmanagements.com | `p=none` | Reporting only — spoofing possible |
| cappofx.com | none | No DMARC — spoofing possible |
| dacm-crypto.top | none | No DMARC |
| aztex.eu | SPF `-all` | Hard fail for unauthorized senders |

---

## ADDITIONAL GEOGRAPHIC LEADS

### goassetmanagementptelttd.my and goassets-systeem.my — Taiwan Registrant
- **Registrant Country: TW (Taiwan)** — the only unredacted geographic field in their Malaysian (.my) WHOIS
- Both domains carry `.my` TLD (Malaysia) but operator registered from Taiwan
- Consistent with Chinese/Taiwanese origin of the Malaysian-branded investment scam cluster
- Source: RDAP partial data (full record not retrievable — RDAP endpoint returned error)

### aztexchange.com — Rapid Suspension
- **Created:** 2026-03-01 via Realtime Register B.V. (Netherlands)
- **Last updated:** 2026-03-03 (placed on clientHold)
- **Status:** clientHold — domain suspended within days of registration
- Suggests the registrar or abuse team acted quickly after reports

---

## DEAD DOMAINS (dropped/expired)

No WHOIS match in Verisign registry as of 2026-03-28:
`byxgexchange.com, byxgcoins.com, bippaxcoins.com, userhelpsdesk.com, 2139a.com, 2139.lol`

Active but with no DNS/content: `ssonysecyco.jp` (NS blank), `mumuex.org` (parked)

---

*Compiled 2026-03-27 from passive OSINT. No active scanning performed.*
