# All Scam Domains — Criminal Network
**Compiled: 2026-03-27**
**Sources:** layer1.html, infrastructure.html, the-two-scams.html, network_osint_2026-03-27.txt, kali_cli_osint_2026-03-27.txt, osint_verification.md, project_osint_findings_2026_03.md, MEMORY.md intel summaries, and all Titan OSINT reports listed

---

## Group A — BIPPAX / BISSNEX / deptoy.co Network (Layer 2/3 — Western-facing)

| Domain | Impersonates / Role | IP | ASN / Host | Status | Notes |
|--------|--------------------|----|------------|--------|-------|
| deptoy.co | Fake cryptocurrency exchange — BIPPAX white-label deployment | (none) | DEAD — NXDOMAIN | Dead | Victim scam platform; BIPPAX-185 branding; JS shared codebase with bissnex.com; expired/dropped Mar 2026. dig returns no A record. |
| bissnex.com | Fake crypto exchange (DacmCrypto branding in Wayback) | (none) | DEAD — NXDOMAIN | Dead | Wayback Oct 2024 shows title "DacmCrypto" + link to dacm-crypto.top; byte.bissnex.com TLS active Dec 2024 + Mar 2025; now NXDOMAIN |
| dacm-crypto.top | Downstream crypto front linked from bissnex.com | 94.26.255.20 | AS204720 JSC Selectel, Saint Petersburg, Russia (fastfox.pro) | Live (as of Mar 2026) | nginx 1.28.2 + PHP 8.2.29; Russian server. Linked via bissnex.com JS download link |
| byxgexchange.com | BYXG Cryptocurrency Group — Dorfman exchange brand | (none) | Expired / WHOIS "no match" | Dead | Timeline domain; no live A record as of Mar 2026 |
| byxgcoins.com | BYXG Cryptocurrency Group — Dorfman coin brand | (none) | Expired / WHOIS "no match" | Dead | Timeline domain; no live A record as of Mar 2026 |
| bippaxcoins.com | BIPPAX coin variant | (none) | Unknown | Unknown | Linked to BYXG/BIPPAX cluster |
| mdutton.com | DUTT Cryptocurrency Exchange — Dorfman's live exchange platform | 172.67.185.221 / 104.21.68.36 | AS13335 Cloudflare (Gname.com registrar) | Live | Cloudflare-proxied; Google Trust Services TLS Feb 2026; last-modified Mar 2026; Gname.com registrar same as SHARE-DNS |
| cappofx.com | Cappo FX — Dorfman-linked FX broker front | 104.21.54.94 / 172.67.137.186 | AS13335 Cloudflare (GoDaddy registrar) | Live | Cloudflare-proxied; GoDaddy secureserver.net MX |
| betaglobalmanagements.com | Beta Global Finance — Dorfman front site / press | Unknown | Unknown | Unknown | Front site; original platform was 4tx9h.com (deleted) |
| 4tx9h.com | Beta Global Finance platform (original) | N/A | Deleted | Dead | Dorfman's Beta Global Finance internal platform; now deleted |
| nanolite-foundationnlf.com | Nanolite Foundation — HTTrack clone of hvcapital.com | 202.79.174.5 | AS152194 CTG Server Limited, Tung Chung, HK | Live | BaFin warned 22 Aug 2025; Dorfman Colorado nonprofit; NameSilo registrar; DNSOWL nameservers; React stack; hardcoded Storyblok token stolen from HV Capital |
| elwallets.com | Unknown / likely wallet phishing | 104.21.91.144 / 172.67.222.23 | AS13335 Cloudflare | Live | Cloudflare-proxied; resolved in network scan |
| mumuex.org | Unknown exchange front — parked | 103.224.212.214 | Trellian/Above.com parking (AU) | Parked | Galcomm/MOBIKAPP registrar; created 2025-04-29; NS: abovedomains.com |

---

## Group B — AZTEX Infrastructure (Layer 2 — European Operations)

| Domain | Impersonates / Role | IP | ASN / Host | Status | Notes |
|--------|--------------------|----|------------|--------|-------|
| aztex.eu | AZTEX criminal operations hub — primary domain | 194.60.201.83 | AS51167 Contabo GmbH, Lauterbourg, France | Live | Porkbun nameservers (same 4-NS cluster as 2139exchange.com); SPF includes this IP; PTR: mail.aztex.eu; Pulsedive neutral |
| mail.aztex.eu | AZTEX self-hosted SMTP/IMAP mail server | 194.60.201.83 | AS51167 Contabo GmbH, France | Live | PTR confirmed; SMTP banner: 220-mail.aztex.eu ESMTP |
| bitwarden.aztex.eu | AZTEX shared Bitwarden/Vaultwarden password manager | 194.60.201.83 | AS51167 Contabo GmbH, France | Live | Last renewed 2026-02-19 (Bitwarden confirmed active) |
| vaultwarden.aztex.eu | AZTEX Vaultwarden (alt subdomain) | 194.60.201.83 | AS51167 Contabo GmbH, France | Live | Same server as bitwarden.aztex.eu |
| matrix.aztex.eu | AZTEX encrypted group messaging (Matrix protocol) | 194.60.201.83 | AS51167 Contabo GmbH, France | Live | Encrypted comms for criminal coordination |
| nextcloud.aztex.eu | AZTEX shared file storage | 194.60.201.83 | AS51167 Contabo GmbH, France | Live | Upgraded Nov/Dec 2025 |
| rdp.aztex.eu | AZTEX web-based RDP gateway | 194.60.201.83 | AS51167 Contabo GmbH, France | Live | RDP access to criminal servers |
| route-finder.aztex.eu | AZTEX custom money-mule routing tool | 194.60.201.83 | AS51167 Contabo GmbH, France | Live | Active during BIPPAX period (2023); custom criminal tooling |
| route-lister.aztex.eu | AZTEX custom money-mule routing tool (companion) | 194.60.201.83 | AS51167 Contabo GmbH, France | Live | Active 2023 alongside route-finder |
| jukem.aztex.eu | AZTEX — unknown app, actively maintained | 194.60.201.83 | AS51167 Contabo GmbH, France | Live | 10 CT certs, auto-renewed every 2 months through Dec 2025 |
| ninjazz.aztex.eu | AZTEX — unknown application | 194.60.201.83 | AS51167 Contabo GmbH, France | Unknown | Unknown purpose |
| somegoodnews.aztex.eu | AZTEX — unknown | 194.60.201.83 | AS51167 Contabo GmbH, France | Unknown | Unknown purpose |
| twenty48.aztex.eu | AZTEX dev/staging — 2048 game | 194.60.201.83 | AS51167 Contabo GmbH, France | Live | Likely test/development deployment |
| aztex.digital | AZTEX secondary domain | (none) | NXDOMAIN | Dead | No public A record as of 2026-03-27; subdomains include project-cheapeats, project-omikami (Solana memecoin), t-contest |
| t-contest.aztex.digital | AZTEX dev/staging | 37.27.206.233 | AS24940 Hetzner Online, Helsinki, Finland | Live | TLS cert; Redis + MinIO Console |

---

## Group C — 2139exchange.com Network (Same AZTEX Porkbun Account)

| Domain | Impersonates / Role | IP | ASN / Host | Status | Notes |
|--------|--------------------|----|------------|--------|-------|
| 2139exchange.com | Fake cryptocurrency exchange — "2139 Exchange" | 185.22.174.75 | AS42532 SIA VEESP, Riga, Latvia | Live | Porkbun NS — identical 4-NS cluster to aztex.eu = same operator; cert 2026-03-19 (actively maintained); aaPanel (Chinese BaoTa panel); CONSOB Italy blacklisted Oct 2024 |
| api.2139exchange.com | 2139exchange backend API | 185.22.174.75 | AS42532 SIA VEESP, Latvia | Live | Backend exchange API |
| m.2139exchange.com | 2139exchange mobile interface | 185.22.174.75 | AS42532 SIA VEESP, Latvia | Live | Mobile-optimized victim-facing portal |
| portal.2139exchange.com | 2139exchange user portal | 185.22.174.75 | AS42532 SIA VEESP, Latvia | Live | Victim account portal |
| intranet.2139exchange.com | 2139exchange internal management panel | 185.22.174.75 | AS42532 SIA VEESP, Latvia | Live | Internal staff/management access |
| hr.2139exchange.com | 2139exchange HR system | 185.22.174.75 | AS42532 SIA VEESP, Latvia | Live | Human Resources system for criminal operation |
| sharepoint.2139exchange.com | 2139exchange document storage | 185.22.174.75 | AS42532 SIA VEESP, Latvia | Live | Document/file sharing |
| dev.2139exchange.com | 2139exchange development instance | 185.22.174.75 | AS42532 SIA VEESP, Latvia | Live | Development/testing |
| megat.vip | Mega Investment Group — linked scam platform | (none) | NXDOMAIN | Dead | Associated with 2139exchange network; $50–70M total victims reported; no live A record |
| 2139.lol | 2139exchange domain variant | (none) | NXDOMAIN | Dead | Dead domain variant |
| 2139a.com | 2139exchange domain variant | (none) | NXDOMAIN | Dead | Dead domain variant |
| 2139.nl | 2139exchange domain variant | (none) | NXDOMAIN | Dead | Dead domain variant |
| 2139.one | 2139exchange domain variant | (none) | NXDOMAIN | Dead | Dead domain variant |

---

## Group D — CTG Server HK (202.79.174.5) — Japanese FSA Fakes (.qpon + .jp)

| Domain | Impersonates / Role | IP | ASN / Host | Status | Notes |
|--------|--------------------|----|------------|--------|-------|
| fsazegsrr.qpon | Japanese FSA 金融庁 (Financial Services Agency) fake | 202.79.174.5 | AS152194 CTG Server Limited, Tung Chung, HK | Live (last seen 2025-12-23) | Active TLS cert CN; served on port 83; .qpon TLD used to mimic fsa.go.jp URLs; fake regulatory approval pages shown to Japanese victims |
| fsaaiesr.qpon | Japanese FSA 金融庁 fake | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-12-22) | Same .qpon FSA fake cluster |
| fsaaivsr.qpon | Japanese FSA 金融庁 fake | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-12-19) | Same .qpon FSA fake cluster |
| fsaaijsr.qpon | Japanese FSA 金融庁 fake | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-12-19) | Same .qpon FSA fake cluster |
| fsaaixsr.qpon | Japanese FSA 金融庁 fake | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-12-19) | Same .qpon FSA fake cluster |
| fsaaegir.jp | Japanese FSA 金融庁 fake (.jp) | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-09-01) | WebNIC registrar; .jp FSA impersonation |
| tradiler.com | Japanese FSA 金融庁 fake / trader variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-27) | SHARE-DNS A5/B5; Gname.com registrar |
| xopazs.com | Japanese FSA 金融庁 fake / unknown redirect | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-11-10) | SHARE-DNS; Gname.com registrar |

---

## Group E — CTG Server HK (202.79.174.5) — Japanese Securities Typosquats

| Domain | Impersonates / Role | IP | ASN / Host | Status | Notes |
|--------|--------------------|----|------------|--------|-------|
| ssonysecyco.jp | Sony Securities (ソニー証券) typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-09-04) | WebNIC / FSFSFSDSDFSFS registrant; SHARE-DNS |
| ssonysecoo.jp | Sony Securities (SBI 証券) typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-10-23) | WebNIC / FSFSFSDSDFSFS registrant; SHARE-DNS A6/B6; created 2025-08-30 |
| asahisec.com | Asahi Securities (朝日証券) typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-27) | WebNIC registrar; SHARE-DNS |
| asahisecco.jp | Asahi Securities (朝日証券) typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-09-02) | WebNIC registrar; SHARE-DNS |
| asahiesecco.jp | Asahi Securities (朝日証券) typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen per layer1) | WebNIC / Web Commerce Comm. Ltd; SHARE-DNS A10/B10; created 2025-08-18 |
| asahiqsecco.jp | Asahi Securities typosquat variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-08-31) | WebNIC registrar; SHARE-DNS |
| fujieebco.jp | Fuji Securities / Fujitsu financial variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-27) | WebNIC / Web Commerce Comm. Ltd; SHARE-DNS A12/B12; created 2025-08-20 |
| fujieemco.jp | Fuji Securities variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-27) | WebNIC / Web Commerce Comm. Ltd; SHARE-DNS A2/B2; created 2025-08-20 |
| fujieenco.jp | Fuji Securities variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-27) | WebNIC / Web Commerce Comm. Ltd; SHARE-DNS; created 2025-08-20 |
| fujizecco.jp | Fuji Securities variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-27) | WebNIC / Web Commerce Comm. Ltd; SHARE-DNS A8/B8; created 2025-08-20 |
| fujixecco.jp | Fuji Securities variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-27) | WebNIC / Web Commerce Comm. Ltd; SHARE-DNS; created 2025-08-20 |
| fujifecco.jp | Fuji Securities variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-27) | WebNIC / Web Commerce Comm. Ltd; SHARE-DNS; created 2025-08-20 |
| fujieevco.jp | Fuji Securities variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-09-01) | WebNIC registrar; SHARE-DNS |
| growthmarket.co.jp | Japan growth market impersonation | (none) | Suspended/Deleted 2026-02-01 | Dead | Deleted/suspended; previously on this server |

---

## Group F — CTG Server HK (202.79.174.5) — International Finance Typosquats

| Domain | Impersonates / Role | IP | ASN / Host | Status | Notes |
|--------|--------------------|----|------------|--------|-------|
| fmtcapitaltc.com | Fake MT5 broker "FMT Capital LLC" — UWORK PBaaS kit | 104.21.91.163 / 172.67.175.136 (Cloudflare-proxied; origin on CTG) | AS13335 Cloudflare (Registrar.eu registrar, MY registrant) | Live | FCA Warning + CFTC Red List; ThinkPHP backend; broker.fmtcapitaltc.com admin (Chinese login); trader.fmtcapitaltc.com victim CRM (8 languages); created 2025-08-26 |
| broker.fmtcapitaltc.com | Admin/manager panel for fmtcapitaltc.com scam | 104.21.91.163 / 172.67.175.136 | AS13335 Cloudflare | Live | Chinese-language manager-login; ThinkPHP; PHP 7.4.33 |
| trader.fmtcapitaltc.com | Victim CRM / trading portal for fmtcapitaltc.com | 104.21.91.163 / 172.67.175.136 | AS13335 Cloudflare | Live | 8 languages including Arabic; KYC upload; UWORK kit |
| alliancebernsteinn.com | AllianceBernstein ($700B AUM) typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-01-24) | Gname.com registrar; SHARE-DNS A/B root pair; registered 2025-07 to 2025-10 |
| alliancebernstseinn.com | AllianceBernstein typosquat variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-24) | Gname.com registrar; SHARE-DNS; 3× AB variants total |
| warburgpiincusii.com | Warburg Pincus ($83B PE) typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-17; DNS confirmed live 2026-03-27) | Gname.com registrar; SHARE-DNS A11/B11; created 2025-12-18; confirmed via dig 2026-03-27 |
| welliingttons.com | Wellington Management ($1.2T) typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-11-18) | Gname.com registrar; SHARE-DNS |
| wellingtonmanaagementi.com | Wellington Management typosquat variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-09-05) | Gname.com registrar; SHARE-DNS |
| wellingtonmanageementi.com | Wellington Management typosquat variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen per layer1) | Gname.com registrar; SHARE-DNS A5/B5; created 2025-08-17 |
| wellingtton.com | Wellington Management typosquat variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen per layer1) | Gname.com registrar; SHARE-DNS A4/B4; created 2025-09-25 |
| gssachssvip.com | Goldman Sachs typosquat | 202.79.174.5 (NXDOMAIN 2026-03-27) | AS152194 CTG Server Limited, HK | Likely dead / moved | Last seen Shodan 2025-12-10; no A record in live dig |
| bankofamerilcasl.com | Bank of America ($3.3T) typosquat | 202.79.174.5 (NXDOMAIN 2026-03-27) | AS152194 CTG Server Limited, HK (Gname.com) | Likely dead / moved | Gname.com registrar; SHARE-DNS A/B root; no live A record 2026-03-27 |
| eatonvancci.com | Eaton Vance / Morgan Stanley IM ($500B AUM) typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | Gname.com registrar; SHARE-DNS A/B root |
| pimco-tw.com | PIMCO Taiwan ($1.8T AUM) typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | Gname.com registrar; SHARE-DNS A/B root |
| adamsstreetpartnersi.com | Adams Street Partners typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-09-16) | SHARE-DNS |
| triainvestmentltc.com | Tria Inversiones España typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-11-18) | SHARE-DNS |
| triainvestmentlitd.com | Tria Investment variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS |
| rw-advisoiry.com | Timothy Investment (TW) / RW Advisors typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-13) | SHARE-DNS |
| sofji.com | SoFi fintech typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-09-17) | SHARE-DNS |
| sofjit.com | SoFi typosquat variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-10-05) | SHARE-DNS |
| sofijii.com | SoFi typosquat variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-10-09) | SHARE-DNS |
| sofils.com | SoFi Invest typosquat | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-10-15) | SHARE-DNS A5/B5 |
| sofiils.com | SoFi typosquat variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS A5/B5 |
| jpngrowthmarket.com | GM Capital Management fake | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2026-02-27) | SHARE-DNS |
| atptechh.com | Gsmkt MAX Capital Mgmt | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (last seen 2025-09-04) | SHARE-DNS |
| atptech.vip | ATP Tech — geo-blocked (403) | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live / geo-blocked (last seen 2026-02-27) | SHARE-DNS; 403 Forbidden to non-permitted IPs |
| chieftoptrading.com | CHIEF INV 致富國際 | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS |
| bmtmax.com | BMT Capital fake | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live / geo-blocked (last seen 2026-02-27) | SHARE-DNS A5/B5; 403 Forbidden |
| bmtmaxx.com | BMT Capital variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live / geo-blocked (last seen 2026-02-27) | SHARE-DNS A5/B5; 403 Forbidden |
| dioep.com | Unknown — geo-blocked | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live / geo-blocked (last seen 2026-02-27) | SHARE-DNS; 403 Forbidden |
| stratiformspi.com | Stratiform investment front | 202.79.174.5 (NXDOMAIN 2026-03-27) | AS152194 CTG Server Limited, HK | Likely dead / moved | SHARE-DNS A5/B5; created 2025-08-26; no A record in live dig |
| stratiformsps.com | Stratiform investment variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS A5/B5 |
| stratiformsloogan.com | Stratiform — EXPOSED ADMIN PANEL | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | admin.stratiformsloogan.com exposed on public reverse IP lookup |
| hmcapitalv.com | HM Capital fake | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS A5/B5 |
| tactiib.com | Tactile/Tactic investment variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS A5/B5 |
| tactiiv.com | Tactile/Tactic investment variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS A5/B5 |
| managementcapitalmad.com | Capital management impersonation | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS A7/B7; created 2025-08-29 |
| bettermeent-llc.com | Betterment / Better.com impersonation | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS |
| assetprivfyers.com | Asset management impersonation | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS |
| assetpvfyers.com | Asset management variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS |
| alphaitx.com | Alpha Investment impersonation | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS A/B root |
| alphasll.com | Alpha Investment variant | 202.79.174.5 | AS152194 CTG Server Limited, HK | Live (per layer1) | SHARE-DNS A/B root |

---

## Group G — Malaysia (.my) Targeting Cluster

| Domain | Impersonates / Role | IP | ASN / Host | Status | Notes |
|--------|--------------------|----|------------|--------|-------|
| goassetmanagementptelttd.my | Go Asset Management Pte Ltd (legitimate MY fund manager) | (Cloudflare via SHARE-DNS) | Gname.com registrar | Unknown | SHARE-DNS; zys@gname.com abuse contact |
| goassetmanagemenntptelttd.my | Go Asset Management variant (double-n) | (Cloudflare via SHARE-DNS) | Gname.com registrar | Unknown | SHARE-DNS; zys@gname.com abuse contact |
| goassetmanagementpteltttd.my | Go Asset Management variant (triple-t) | (Cloudflare via SHARE-DNS) | Gname.com registrar | Unknown | SHARE-DNS; zys@gname.com abuse contact |
| goassetmanagementtptelttd.my | Go Asset Management variant (double-t) | (Cloudflare via SHARE-DNS) | Gname.com registrar | Unknown | SHARE-DNS; zys@gname.com abuse contact |
| goassets-systeem.my | Go Asset system variant | (Cloudflare via SHARE-DNS) | Gname.com registrar | Unknown | SHARE-DNS; zys@gname.com abuse contact |

---

## Group H — DNS / Mail Infrastructure (Not Victim-Facing Scam Sites)

| Domain | Impersonates / Role | IP | ASN / Host | Status | Notes |
|--------|--------------------|----|------------|--------|-------|
| share-dns.com | Criminal DNS infrastructure (nameserver root) | Cloudflare (172.64.53.25 proxy) | AS13335 Cloudflare / Gname.com registrar | Live | Registered 2022-06-30; ~800K+ malicious domains served; NS: troy/ulla.ns.cloudflare.com; 15+ numbered A/B pairs |
| share-dns.net | Criminal DNS infrastructure (nameserver root) | Cloudflare (172.64.53.25 proxy) | AS13335 Cloudflare / Gname.com registrar | Live | Registered 2022-06-30 (same day as .com); NS: anita/brad.ns.cloudflare.com; MX: mail.share-dns.net |
| mail-ussl.com | Dedicated SMTP server for fmtcapitaltc.com | 104.21.1.194 / 172.67.129.222 (Cloudflare); MX origin: 67.216.195.233 | MX origin: AS25820 IT7 Networks Inc, Los Angeles, CA | Live | Registered July 2023; MX: mx.mail-ussl.com → 67.216.195.233 (IT7 Networks LA); used by fmtcapitaltc.com SPF |
| ctgserver.com | CTG Server Limited — ISP marketing site | 172.67.73.150 / 104.26.0.20 / 104.26.1.20 | AS13335 Cloudflare / Porkbun registrar | Live | ISP's own marketing domain; MX: larksuite.com (Lark/ByteDance business suite); NOT a scam site itself — abuse contact for the HK server |

---

## Group I — AZTEX-Linked / Previously Investigated Infrastructure

| Domain | Impersonates / Role | IP | ASN / Host | Status | Notes |
|--------|--------------------|----|------------|--------|-------|
| aztexchange.com | AZTEX scam exchange — typosquat / brand | (none) | NS: ns1/ns2.suspended-domain.com | Suspended | Registered 2026-03-01 via Realtime Register; suspended by registrar 2026-03-03 (within 48hrs); Pulsedive risk = HIGH / Scam (general); no DNS records |
| userhelpsdesk.com | Fake helpdesk / support scam | (none) | NXDOMAIN | Dead | No A record in live scan; investigated as possible AZTEX-linked support front |
| userhelpsdesk.com (typo: userhelpsdesk) | Helpdesk typosquat variant | (none) | NXDOMAIN | Dead | "userhelpsdesk.com" (no 's' in "helps") — distinct from "userhelpdesk.com"; both NXDOMAIN |

---

## Summary Statistics

| Category | Count |
|----------|-------|
| CTG Server HK (202.79.174.5) — confirmed domains | 39 |
| AZTEX EU infrastructure domains/subdomains | ~15 |
| 2139exchange network (inc. variants + subdomains) | ~13 |
| BIPPAX/BISSNEX/deptoy.co cluster | ~8 |
| Dorfman-linked exchange/front domains | ~6 |
| Malaysia (.my) cluster | 5 |
| DNS/mail infrastructure | 4 |
| SHARE-DNS served (external estimate) | 800,000+ |
| **Total confirmed/documented IOC domains** | **~110** |

---

## Key Infrastructure IPs

| IP | Owner | Location | Domains / Role |
|----|-------|----------|----------------|
| 202.79.174.5 | AS152194 CTG Server Limited | Tung Chung, Hong Kong | ~39 scam domains; MySQL 3306+33060 exposed; last active 2026-03-23 |
| 185.22.174.75 | AS42532 SIA VEESP | Riga, Latvia | 2139exchange.com + all subdomains |
| 194.60.201.83 | AS51167 Contabo GmbH | Lauterbourg, France | aztex.eu + all subdomains; PTR: mail.aztex.eu |
| 37.27.206.233 | AS24940 Hetzner Online | Helsinki, Finland | AZTEX dev/staging (t-contest.aztex.digital) |
| 79.78.160.133 | AS13285 TalkTalk | England, UK | Residential — RDP cert CN "AZTEX-BARRY" (named operator) |
| 67.216.195.233 | AS25820 IT7 Networks Inc | Los Angeles, CA | MX: mx.mail-ussl.com — fmtcapitaltc.com SMTP |
| 94.26.255.20 | AS204720 JSC Selectel (fastfox.pro) | Saint Petersburg, Russia | dacm-crypto.top server |
| 172.64.53.25 | AS13335 Cloudflare | Anycast | SHARE-DNS.COM/NET backend proxy |

---

## Notes on Methodology

- Status "Live" = confirmed with A record resolving to non-Cloudflare IP or confirmed Cloudflare-proxied with HTTP 200 response, within the scan window cited.
- Status "Dead" = NXDOMAIN or explicit WHOIS "domain not found" confirmed 2026-03-27.
- Status "Unknown" = domain registered and DNS nameservers present but no active content confirmed in this session.
- "Last seen" dates from urlscan.io passive DNS scans (Sep 2025 – Mar 2026) as recorded in layer1.html.
- CTG Server (AS152194) is the ISP/network owner at 202.79.174.5; the actual scam operator is an unknown CTG customer. CTG Server is not established as a knowing participant.
- alliancebernsteinn.com has 3 confirmed variants total; wellingtton/wellingtonmanageementi/wellingtonmanaagementi are 3 Wellington variants.
- The 39 CTG server domains figure is from urlscan.io passive DNS (Sep 2025–Mar 2026); additional domains may exist on other CTG Server IPs not yet identified.
