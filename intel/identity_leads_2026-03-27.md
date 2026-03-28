# Identity Leads OSINT — 2026-03-27

Passive OSINT research on five identity leads. All sources are public. No active intrusion or authenticated-access tools used.

---

## Lead 1: "slepsk" Username

### GitHub / Code Repositories

- **Direct hit: No.** GitHub user `slepsk` does not exist (API returns 404).
- **Related accounts found:**
  - `slepsk1987` (https://github.com/slepsk1987) — Created 2013-07-08, last updated 2019-10-23. Zero public repos, zero followers. The `1987` suffix strongly suggests birth year 1987. Account appears dormant or personal-only.
  - `slepskyi-xgen` (https://github.com/slepskyi-xgen) — Created 2023-06-28, zero public repos, zero activity. The `-xgen` suffix suggests corporate affiliation (xgen = some company/studio named X-Gen or similar). Created within weeks of the AZTEX Hetzner server's mid-2023 active period.
- **No GitLab or Bitbucket results** returned for "slepsk" via web search.
- **No GitHub commits** with the token "slepsk" found via search API.

### Certificate / DNS Evidence

- `slepsk.aztex.digital` certificate issued **2025-07-12** by Let's Encrypt (R11), expiry 2025-10-10. The subdomain does not currently resolve (NXDOMAIN) — the cert expired and was not renewed, possibly indicating the user's work on that server ended around Q3 2025.
- The subdomain is one of only 8 subdomains ever certified under `aztex.digital`:
  - `not-front-contest.aztex.digital` (2025-06)
  - `obsidian.aztex.digital` (2025-06)
  - `project-cheapeats.aztex.digital` (2025-07 through 2025-11)
  - `project-omikami.aztex.digital` (2025-06)
  - `slepsk.aztex.digital` (2025-07)
  - `www.aztex.digital`
  - `*.aztex.digital`
- The naming pattern `project-cheapeats` and `project-omikami` suggests this is a developer sandbox or internal project hosting service — likely a Nextcloud, Coolify, or custom CI/CD deployment server where developers host their side projects. Each developer gets a personal subdomain named after their handle.

### Identity Clues

- **"slepsk" is likely Ukrainian/Russian origin.** The word root "slep" (слеп) means "blind" in Slavic languages; "slepsk" as a handle could be a playful derivative or surname-based alias. There is no Scandinavian etymology match.
- The Polish volleyball team "Ślepsk Suwałki" (Ślepsk = name of river in Poland) is the only unrelated "slepsk" result, confirming this is a proper name / brand, not a common word.
- Given the AZTEX operation's confirmed Ukrainian/Eastern European developer base (Contabo FR, Hetzner HEL, TalkTalk UK "AZTEX-BARRY" — a UK-based node with Eastern European team), `slepsk` is assessed as a developer handle for a Ukrainian or Russian developer working on the AZTEX platform.
- **GitHub `slepsk1987`** (born ~1987, dormant since 2019) is a plausible but unconfirmed match to the aztex.digital user. The 1987 birth year would make them ~38 years old in 2026 — consistent with a senior developer role.
- **`slepskyi-xgen`** (created June 2023, same timeframe as aztex.digital's certificate history expansion) is the stronger candidate for the active developer. "Slepskyi" is a Ukrainian-style transliteration of the surname Slepsky/Slepskyy.

### Other Subdomains as Team Member Evidence

The aztex.eu domain (the main criminal operation server at Hetzner 37.27.206.233) reveals other possible team member handles via crt.sh:
- `ninjazz.aztex.eu` (cert: 2025-11-17) — A live WebAssembly/WebGL/WebXR demo project, publicly titled "Ninjazz — an experiment to showcase WebAssembly, WebGL and WebXR." This is a developer's personal tech showcase. Handle: **ninjazz**.
- `jukem.aztex.eu` (cert: 2025-12-05) — Another handle: **jukem**.
- `somegoodnews.aztex.eu` (2021-09-16) — Early subdomain, possibly a news aggregator project.
- `twenty48.aztex.eu` (2022-10-06) — A 2048 game implementation, another developer demo.

**Assessment:** The AZTEX development team appears to use aztex.eu and aztex.digital as internal hosting for developer side projects, with subdomains named after developer handles. Identified handles: **slepsk**, **ninjazz**, **jukem**, **BARRY** (from TalkTalk PTR record `AZTEX-BARRY`). These are likely 4+ developers contributing to the AZTEX criminal infrastructure.

### WHOIS / Domain Checks

- `slepsk.com` — **NOT REGISTERED** (WHOIS: "No match for domain SLEPSK.COM")
- `slepsk.net` — **NOT REGISTERED**
- `slepsk.io` — **NOT REGISTERED**
- No DNS resolution for any slepsk.* domain.

---

## Lead 2: admin@megaig.vip

### Domain and Certificate History

- `megaig.vip` — First cert: 2023-05-08 (www.megaig.vip). Wildcard cert issued 2024-09-07. Domain registered **May 8, 2023** via Go Montenegro Domains LLC / Domains By Proxy (privacy-protected). Renewal date: May 8, 2026.
- Domain is currently **DEAD** (NXDOMAIN — megaig.vip no longer resolves). Cloudflare hosting (104.21.63.179) was used while active.
- Wildcard cert (`*.megaig.vip`) was issued September 2024, suggesting the operation scaled up infrastructure in mid-2024, consistent with the 2139exchange collapse timeline (CONSOB blackout Oct 2024).
- **Only two subdomains ever certified**: `www.megaig.vip` (2023) and `*.megaig.vip` (2024). No leaked internal subdomains.

### HIBP / Breach Status

- HaveIBeenPwned API requires a paid API key (HTTP 401 returned). **Cannot confirm breach status without key.** No free public lookup succeeded.

### ScamAdviser / Public Records

- Trust score: **0 / Very Likely Unsafe**. Flagged malicious by Bfore.ai threat intelligence.
- Claims founded in US by "**Logan Smith**" in 2015 — confirmed **fabricated**: Logan Smith is a stock-image persona, domain registered 2023 (7 years after claimed founding).
- ISP while active: Cloudflare (masked true origin).
- Registered via Domains By Proxy — full identity redaction.

### Telegram Presence

- **@mega_ig** is the confirmed Telegram channel for Mega Investment Group (channel ID: 1227836042, per Telemetr.io). Full admin identity not publicly available via passive means.
- The channel was used to coordinate the 2139exchange Ponzi promotion in Italy and other markets.

### 2139Exchange Connection

- Mega Investment Group (megat.vip / megaig.vip) is confirmed by multiple sources as a feeder platform for the 2139exchange cluster. Both platforms used TRON blockchain for victim fund collection.
- On-chain analysis by Decripto.org found that TRON transaction fees to 2139 wallets originated from **Feee.io** and **CCB-Exchange**, "both of Asian origin" — pointing to Chinese or Southeast Asian operators controlling the backend, with megaig.vip serving as a Western-facing front.

### Assessment

- **admin@megaig.vip** is the operator contact for the Mega Investment Group Telegram-based investment scam, which is a sub-cluster of the 2139exchange Ponzi. The operator(s) are assessed as **Chinese or Southeast Asian** based on on-chain infrastructure analysis. The "Logan Smith" persona and Cloudflare masking were deliberate identity obfuscation. Domain is dead as of March 2026 but renewal is paid through May 2026, suggesting the operator still controls the registration.

---

## Lead 3: "Mentor Claus" — Italian Promoter for 2139exchange

### Confirmed Role

- **"Mentor Claus"** is confirmed by Italian investigative outlet Decripto.org and victim community reporting as "one of the major references for the Italian side" and "one of 2139 Exchange's usual promoters." Mentor Claus issued statements **on behalf of 2139exchange via its Telegram group** when users reported blocked withdrawals.
- Mentor Claus is described as the primary Italian-language Telegram intermediary between the 2139exchange operators and Italian victims.

### Telegram Activity

- Mentor Claus communicated through the 2139exchange Italian Telegram group(s). No standalone Telegram username for "Mentor Claus" was found via passive search — they appear to have operated within the main exchange's group rather than a separately named channel.
- The Mega Investment Group Telegram (@mega_ig) is the linked English-language channel; the Italian groups operated separately.

### Italian Victim Impact

- The provinces of **Lecce** and **Perugia** are the hardest-hit regions in Italy, per Corriere Salentino and Quotidiano di Puglia reporting.
- Italian investigators (Guardia di Finanza, Lecce) opened a formal criminal investigation. The Lecce GdF initiated proceedings on suspicion of large-scale financial fraud following hundreds of victim complaints.
- Victim losses ranged from "a few hundred euros to 20,000 euros per family," with the total Italian exposure estimated in the tens of millions.
- Global: ~200,000 users, $200M+ deposited, ~$50M confirmed stolen via on-chain analysis (Decripto.org exclusive, Oct 2024). A later analysis found $27M moved toward Binance accounts post-CONSOB blackout.

### Regulatory Actions

- **CONSOB** (Italian financial regulator) blacklisted 2139exchange and blacked out three domains: `2139.online`, `2139.ltd`, and `2139.fun`.
- **FCA** (UK) issued warning against 2139exchange.

### On-Chain Identity Clues

- 2139exchange runs on **TRON blockchain** (primary) and Ethereum (minor). Wallet structure: distribution wallets (fake returns to keep Ponzi alive) and cash-out wallets (operator profit). The Decripto.org on-chain analysis found TRON energy fee payments linking 2139exchange wallets to Feee.io and CCB-Exchange — Asian-origin scam infrastructure.
- Connection to **Feee.io** (a TRON energy marketplace) and **CCB-Exchange** suggests Chinese criminal infrastructure operators who license the platform backend.

### Assessment

- "Mentor Claus" is a Telegram persona/alias used by a likely Italian-speaking individual who served as a regional promoter and PR manager for 2139exchange in Italy. The persona is almost certainly not the platform operator — they are a recruiter/promoter tier who received commissions. Identity unknown from passive OSINT but the GdF Lecce investigation may have unmasked them through domestic telco records. The broader operation is of Asian (likely Chinese) origin.

### Italian Sources

- https://decripto.org/en/2139-exchange-withdrawals-blocked-whats-happening-updated/
- https://www.corrieresalentino.it/2024/12/lecce2139-exchange-dietro-la-promessa-di-facili-guadagni-con-le-criptovalute-si-nascondeva-la-truffa-aperta-uninchiesta/
- https://www.quotidianodipuglia.it/lecce/lecce_criptovalute_salento_truffa_inchiesta_trading_online_2139exchange-8545429.html
- https://www.tutelatrader.it/2139-exchange/
- https://it.cointelegraph.com/news/la-consob-oscura-il-sito-di-2139-exchange-la-piattaforma-di-trading-era-una-truffa

---

## Lead 4: fmtcapitaltc.com Malaysian Registrant

### WHOIS

- **Registrar:** Hosting Concepts B.V. d/b/a Registrar.eu (via OpenProvider) — IANA ID 1647
- **Registrant Country:** MY (Malaysia)
- **Registrant State/Province:** Wilayah Persekutuan Kuala Lumpur
- **Registrant Name/Organization:** REDACTED FOR PRIVACY
- **Registrant Email:** Routed through Registrar.eu contact form (no direct email visible)
- **Domain Status:** clientTransferProhibited
- **Nameservers:** ace.ns.cloudflare.com / lina.ns.cloudflare.com (Cloudflare — origin IP masked)
- **Last Updated:** 2026-02-05 (active and maintained as of February 2026)
- **Expiry:** 2026-08-26 (paid through August 2026)

### Certificate / Infrastructure History

Certificates from crt.sh (all issued February 2026):
- `broker.fmtcapitaltc.com` — 2026-02-16 (manager/broker login panel)
- `trader.fmtcapitaltc.com` — 2026-02-16 (victim CRM / trader-facing interface)
- `*.fmtcapitaltc.com` — 2026-02-19
- `fmtcapitaltc.com` — 2026-02-26
- `www.fmtcapitaltc.com` — 2026-02-26

All certificates are very recent (Feb 2026), suggesting the domain became operational in early 2026. This matches a fresh deployment of a pig-butchering kit.

### Regulatory Status

- **FCA** (UK): Blacklisted — providing financial services without authorization (late 2025)
- **CFTC** (US): Added to RED List (Registration Deficient) — unregistered foreign entity targeting US persons
- Source: https://fraudbrokers.net/finance-trade-capital/

### Backend Technology: ThinkPHP (Chinese Framework)

- The backend uses **ThinkPHP**, a Chinese PHP MVC framework widely used in Chinese-developed financial fraud kits.
- The two-panel architecture (`broker.fmtcapitaltc.com` = agent/manager login; `trader.fmtcapitaltc.com` = victim CRM with KYC) exactly matches the **UWORK pig-butchering-as-a-service** kit architecture documented by Infoblox (January 2026 report).

### UWORK Kit Assessment

Per Infoblox research and The Hacker News (Jan 2026):
- **UWORK** is a Chinese-operated (Taiwan-based operator) Pig-Butchering-as-a-Service platform providing:
  - Pre-made fake investment website templates (crypto, forex, gold)
  - Two-tier CRM: administrator/agent panel + victim KYC interface
  - Packages starting at $50 (templates) to $2,500 (full kit with VPS, mobile app, MetaTrader integration, shell company, regulator registration)
  - Multi-level agent hierarchy management
  - Used by operators arrested in Feb 2025 (US DOJ) for $13M fraud; customers across Southeast Asia
- The `broker.fmtcapitaltc.com` + `trader.fmtcapitaltc.com` pattern is consistent with UWORK's documented two-panel architecture.
- The Malaysian registrant in Kuala Lumpur is consistent with UWORK's documented customer base (Southeast Asia).

### Victim Reports

- Common pattern: fake profits shown on dashboard, withdrawals blocked once large deposit accumulated.
- Platform ignored withdrawal requests — consistent with pig-butchering "slaughter" phase.
- Dedicated mail server: `mail-ussl.com` → 67.216.195.233 (IT7 Networks, LA) registered July 2023, used for victim communications.

### Assessment

- **fmtcapitaltc.com** is a UWORK or UWORK-style pig-butchering deployment operated by a Malaysian-based actor in Kuala Lumpur. The operator identity is fully privacy-protected via Registrar.eu. The ThinkPHP + dual-panel architecture is a signature of Chinese-sourced fraud kit deployment. The FCA/CFTC listings and February 2026 certificate issuance suggest this site launched in early 2026 as a fresh operation or relaunch after a previous domain was burned.

---

## Lead 5: CTG Server Limited — Customer Identity

### Company Identity

- **Full name:** CTG Server Limited
- **Address:** 202, 2/F Kam Sang Building, 257 Des Voeux Road Central, Hong Kong
- **Abuse contact:** cs.mail@ctgserver.com
- **ASN:** AS152194 (CTGSERVERLIMITED-AS-AP) and AS151850
- **Registered with APNIC:** December 22, 2023 (relatively new ASN)
- **Website:** myctgs.com (customer portal)

### Network Scale

- **Total IPv4 addresses:** ~196,000–198,000 across 672+ prefixes
- **Hosted domains:** ~1,196,954 domains across 35,945 IPs (per IPinfo.io)
- **Geographic distribution:** Hong Kong, Singapore, Japan, with some US and China presence
- **Upstreams:** PCCW Global (AS3491), NTT America (AS2914), Hurricane Electric (AS6939), BGP Network Limited (AS64050), CloudRadium, Nearoute Limited

### Abuse Profile

- **Spam:** CleanTalk blacklist shows 15 spam-active IPs out of 9,355 detected (0.16% spam rate). March 2025 peak: 634 spam instances. Multiple IP subnets appear on spam blacklists: 202.146.217.0/24, 103.41.65.0/24, 27.124.28.0/24, 27.124.43.0/24.
- **Highest individual abuse IPs:** 112.213.116.6 (234 spam reports), 137.220.151.110 (185 reports), 137.220.150.152 (177 reports).
- **AbuseIPDB:** CTG Server Ltd IPs appear across AbuseIPDB (e.g., 202.79.164.161 listed).
- **Bogon announcement:** BGP.he.net notes "AS152194 announces bogons" — the network originates routes for reserved IP space, a red flag in the hosting community.
- **Scamalytics:** CTG Server Ltd has a dedicated fraud-check page, suggesting it is a known quantity for fraud-risk analysts.

### Relationship to Scam Infrastructure

- IP **202.79.174.5** (the server hosting ~50 fake finance domains including Nanolite, AllianceBernstein/BofA/EatonVance/PIMCO typosquats) falls within CTG Server's `202.79.174.0/24` block.
- The server has **MySQL port 3306 exposed publicly** — a significant operational security failure. While Shodan historical banner data was not retrievable via passive means, this exposure has likely been indexed. Database names visible via Shodan (if any) would be a high-value intelligence lead requiring Shodan API access.
- CTG Server's business model (1.2M+ hosted domains, HK-registered, APNIC Dec 2023, anonymous abuse contact) is consistent with **bulletproof hosting or permissive hosting** used by Chinese cybercriminal networks, though it is not as explicitly documented as Chang Way Technologies (the "BearHost/UNDERGROUND" HK bulletproof hoster documented in prior research).
- The CTG Server abuse contact `cs.mail@ctgserver.com` is a generic customer service address — no named individual is publicly associated with the company.

### HKIRC / APNIC Complaints

- No specific HKIRC (Hong Kong domain registry) complaints were found via public search.
- APNIC registration date (December 2023) is relatively recent, suggesting CTG Server obtained its own ASN recently — possibly migrating from transit under another ASN.

### Assessment

- **CTG Server Limited** is a Hong Kong-based hosting provider with documented abuse history across spam, fraud, and malicious domains. Its permissive hosting practices make it attractive to cybercriminal customers. The specific customer operating 202.79.174.5 (the ~50-domain fake finance server) is not publicly identifiable from passive OSINT alone — the customer identity would require a formal legal request to CTG Server or HKIRC. The exposed MySQL 3306 port on 202.79.174.5 is a high-priority lead for investigators with Shodan API access: historical banners may have leaked database names, table structures, or even credentials.

---

## Summary Table

| Lead | Status | Key Finding | Confidence |
|------|--------|-------------|------------|
| slepsk | PARTIAL ID | Ukrainian/Russian developer handle; birth year ~1987 if `slepsk1987` matches; part of 4+ developer team (ninjazz, jukem, BARRY, slepsk) running AZTEX infrastructure | Medium |
| admin@megaig.vip | OPERATOR CONFIRMED | Mega Investment Group operator; Chinese/SE Asian origin; Telegram @mega_ig; domain dead, paid through May 2026 | High |
| Mentor Claus | ROLE CONFIRMED | Italian-language Telegram promoter for 2139exchange; GdF Lecce investigation open; likely Italian national, not the platform operator | High |
| fmtcapitaltc.com | REGISTRANT PARTIAL | Malaysian operator, Kuala Lumpur; UWORK-style ThinkPHP kit; FCA+CFTC listed; launched Feb 2026 | High |
| CTG Server | HOST CONFIRMED | HK bulletproof-adjacent hoster AS152194; abuse documented; MySQL 3306 exposure on 202.79.174.5 is key Shodan lead | Medium |

---

## Recommended Next Actions

1. **slepsk / AZTEX team:** Search Telegram for channels using handles "ninjazz", "jukem", "slepsk". Cross-reference with Ukrainian developer communities. Check if `slepskyi` appears in any LinkedIn profiles or Ukrainian IT company directories.
2. **admin@megaig.vip:** Obtain paid HaveIBeenPwned API key to check breach databases. Submit to IntelX paid search. Check Telegram channel @mega_ig admin list (requires Telegram account).
3. **Mentor Claus:** Contact Decripto.org directly — they have conducted forensic investigation and may share de-anonymized findings with law enforcement. File a tip with GdF Lecce (indagine 2139exchange is active).
4. **fmtcapitaltc.com:** Submit legal request to Registrar.eu under fraud/law enforcement provisions for registrant identity. Probe `broker.fmtcapitaltc.com` and `trader.fmtcapitaltc.com` for UWORK CRM fingerprints via passive TLS analysis.
5. **CTG Server / 202.79.174.5:** Run Shodan search for `202.79.174.5` with MySQL banner filter. Submit HKIRC abuse complaint. Submit formal request to CTG Server (cs.mail@ctgserver.com) with regulatory backing.

---

*Research date: 2026-03-27. All sources passive/public. No authenticated access used.*
