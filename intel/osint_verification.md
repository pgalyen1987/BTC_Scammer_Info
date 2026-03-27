# OSINT verification log (investigation data)

This file records what was **confirmed against primary public sources** versus what **failed lookup or needs manual confirmation**. Last pass: March 2026.

## Colorado Secretary of State (`sos.state.co.us`)

Business Entity Detail pages were pulled for master file IDs below (registered agent names verbatim from SOS HTML).

| Entity | Master file | Registered agent (SOS) | Notes |
|--------|-------------|------------------------|--------|
| DUTT Cryptocurrency Exchange Ltd | **20211357517** | **Colorado Registered Agents Inc** | Good Standing; formed 04/14/2021; principal 1800 Larimer St. **Not** Dorfman as RA — commercial registered agent. SOS summary “Form” shows **Corporation**; SEC Form D lists **LLC** — reconcile via charter/filings. |
| Nanolite Foundation | 20238080577 | DARRYL JOEL DORFMAN | Good Standing. |
| BYXG Cryptocurrency Group Ltd | 20231159680 | DARRYL JOEL DORFMAN | Delinquent (Jul 2024). |
| 2139 Com Exchange Ltd | 20241159995 | DARRYL JOEL DORFMAN | Delinquent; formed 02/06/2024. |
| Global One-Stop Trading Exchange | **20241029455** | DARRYL JOEL DORFMAN | Delinquent; formed 01/07/2024; **Nonprofit Corporation**; principal and RA **9888 W Belleview Ave, Denver, CO 80123**. |
| celestia | **20231449764** | DARRYL JOEL DORFMAN | Delinquent (Sep 2024); formed 04/26/2023; **Nonprofit Corporation**; principal and RA **9888 W Belleview Ave, Ste 2234, Denver, CO 80123**. Unrelated to Celestia (TIA) blockchain. |
| Cappo FX | 20231169570 | DARRYL JOEL DORFMAN | |
| K2 Exchange | 20241304682 | DARRYL JOEL DORFMAN | |
| USDcc | 20231183233 | DARRYL JOEL DORFMAN | |
| Winston Education Consulting Co., Ltd | 20228054956 | DARRY JOEL DORFMAN | Typo variant on file; Delinquent (Mar 2024). |
| Alexander & Company Ltd. | **20161759019** | **Alexander William Dorfman** | Delinquent (Apr 2018); formed 11/06/2016; **LLC**; principal and RA **3933 Promontory Court, Boulder, CO 80304**. Distinct RA from Darryl Joel Dorfman — possible relative. |
| Dorfman Family Foundation | **20131560423** | **Barry Dorfman** | Voluntarily dissolved (Jul 2015); formed 09/26/2013; **Nonprofit Corporation**; principal and RA **1225 17th Street, Suite 1900, Denver, CO 80202**. Distinct RA from Darryl Joel Dorfman — possible relative. |
| Super Profit 8 Financial Services Ltd. | 20241164417 | (prior notes: DARRYL DORFMAN) | Delinquent — detail page blocked by Cloudflare in one automated pass; re-check in browser. |

**Invalid / superseded ID:** `20211471867` was a typo; it does not resolve on SOS. Use **20211357517** for DUTT.

**Not found** (basic name search, Mar 2026): exact strings **SSW Management Institute**, **Beta Global Finance** — may be trade names, other states, or different legal names. Full **registered-agent** search requires CAPTCHA (Advanced Search).

## SEC EDGAR (director / issuer facts for DUTT)

- **Issuer:** DUTT Cryptocurrency Exchange Ltd  
- **CIK:** 0002093026  
- **EIN:** 394817522  
- **State of incorporation:** Colorado  
- **Entity type (Form D):** **Limited Liability Company**  
- **Director:** Darryl Joel Dorfman  
- **Principal address:** 1800 Larimer Street, Denver, CO 80202  

## BaFin (Nanolite)

- Official English consumer warning: **22 August 2025** (nanolite-foundationnlf.com and related).

## Canada — Corporations Canada (ISED)

**BISSNEX CRYPTO GROUP LIMITED**, **1231288-3**: dissolved **2025-07-25** (s. 212); director Jack Williams; name history Alpha → BIPPAX → BISSNEX.

## Domain follow-up (registrar / hosting targets)

| Pattern | Domains (investigation) | Lead |
|--------|-------------------------|------|
| DUTT | mdutton.com | Gname; AWS; Cloudflare |
| BYXG | byxgexchange.com, byxgcoins.com | Timeline domains; COM **WHOIS “no match”** Mar 2026 (likely expired) |
| Nanolite | nanolite-foundationnlf.com | NameSilo |
| 2139 Com | 2139exchange.com | Porkbun; same NS as aztex.eu |
| Cappo FX | cappofx.com | GoDaddy (long renewal) |
| Beta Global | 4tx9h.com (deleted), betaglobalmanagements.com | Front site / press |
| SSW | wealthcommunities.com (parked), DeviantArt sswmanagement | Contact email history |

**Do not assume** `k2exchange.com` (registered 2010, GoDaddy) equals the Colorado “K2 Exchange” entity without further tie-in — domain predates the shell by years.

## Sources that blocked automated verification

- **UK Companies House:** HTTP 403 in tooling.  
- **Colorado SOS:** rate limiting / Cloudflare challenge on some sequential requests.  
- **Advanced Search (registered agent by name):** requires CAPTCHA.

## Network sweep (2026-03-27)

Live `dig` / `traceroute` / `ipinfo.io` against investigation domains: **`intel/network_osint_2026-03-27.txt`**. Confirms **nanolite-foundationnlf.com** and **warburgpiincusii.com** both **A → 202.79.174.5** (CTG Server Limited, HK); **2139exchange.com** → **185.22.174.75** (VEESP, LV); **aztex.eu** → **194.60.201.83** (Contabo, FR). Several fronts are **Cloudflare-only** (no origin in A record).

## Action items

1. Subpoena **Colorado Registered Agents Inc** for DUTT service-of-process / forwarding records (complements FinCEN/SEC angles).  
2. Manual CAPTCHA search: all entities where **Darryl Joel Dorfman** is registered agent (may surface additional IDs).  
3. Re-check **FINTRAC** MSB **M20852872** via official channels if still cited in filings.
