# SHARE-DNS OSINT — 2026-03-27
*Passive OSINT on share-dns.com and share-dns.net. All data from public sources.*

---

## WHOIS / REGISTRATION

### share-dns.com
- **Registrar:** Gname.com Pte. Ltd. (IANA 1923)
- **Created:** 2022-06-30T05:37:26Z
- **Expires:** 2027-06-30T05:37:26Z
- **RDAP last update:** 2026-03-25T21:26:18Z (recently active)
- **NS:** troy.ns.cloudflare.com / ulla.ns.cloudflare.com
- **Status:** clientTransferProhibited
- **Registrant:** Privacy-protected (Gname.com)

### share-dns.net
- **Registrar:** Gname.com Pte. Ltd. (IANA 1923)
- **Created:** 2022-06-30T07:24:59Z (same day as .com, 2 hours later)
- **Expires:** 2027-06-30T07:24:59Z
- **NS:** anita.ns.cloudflare.com / brad.ns.cloudflare.com
- **Status:** clientTransferProhibited
- **Registrant:** Privacy-protected (Gname.com)

**Key fact:** Both domains were registered on the same day by the same registrar (Gname.com), which is also the registrar for the majority of criminal domains in this network.

---

## DNS INFRASTRUCTURE

### Nameserver IPs (all pairs a1–a15 / b1–b15)
All resolve to Cloudflare Anycast:
- `a*.share-dns.com` → 172.64.53.25 (Cloudflare)
- `b*.share-dns.net` → 172.64.52.239 (Cloudflare)

Additional subdomains observed pointing to 172.64.53.25:
- www, admin, cpanel, webmail, ns1, ns2, smtp, ftp, api, mail (share-dns.com side)

### Mail Server
- **mail.share-dns.net:** 35.215.163.95
- **PTR:** mail.share-dns.net
- **ASN:** AS15169 (Google LLC)
- **Location:** Hong Kong (Google Cloud)
- **SPF (share-dns.net):** `v=spf1 ip4:35.215.163.95 -all`
- **MX (share-dns.net):** mail.share-dns.net (priority 5)

### SSL Certificates
- **share-dns.com:** 28 certs logged, oldest 2022-07-04, newest 2026-02-02
  - Issuers: Google Trust Services (WE1/WR1), Let's Encrypt (E1), Sectigo
  - Coverage: *.share-dns.com + share-dns.com (wildcard only)
- **share-dns.net:** Continuous since June 2023; issuers: Let's Encrypt, Google Trust Services, Sectigo, Cloudflare

---

## SCALE DATA (from domainstate.com)

| NS Pair | Domains served |
|---------|---------------|
| a.share-dns.com / b.share-dns.net | 3,756,268 (share-dns.com total) |
| a.share-dns.net / b.share-dns.net | 3,685,235 (share-dns.net total) |
| Single pair b.share-dns.net | 284,334 |

**Context:** The vast majority of SHARE-DNS customers are legitimate businesses (Chinese pinyin domain names dominate). Criminal domains are a small but significant fraction. Criminal proportion is unknown without law enforcement data.

---

## THREAT INTELLIGENCE LINKS

### Palo Alto Unit 42 (2024)
- Named share-dns in context of malicious Olympic-themed gambling campaign
- Quote: *"All gambling domains are resolved by the same DNS hosting service (share-dns), suggesting a potential connection between the operators."*

### NetBeacon Institute (March 2025)
Gname.com Pte. Ltd. (registrar that owns share-dns.com/net) was named as a top-abused registrar:
- Held **9% of malicious phishing domains** while holding only **2% of all gTLD domains**
- Record high: 47,613 unique phishing domains in March 2025 (63% month-on-month increase)
- 87% classified as maliciously registered (not compromised)
- Also named: Dominet HK Limited (55% of phishing), WebNic.cc (6%, May 2025)

---

## GNAME.COM PTE. LTD. — COMPANY DETAILS

- **UEN:** 202013923E
- **Incorporated:** 2020-05-19 (Singapore)
- **Type:** Exempt Private Company Limited by Shares
- **Paid-up capital:** SGD 500,000
- **Registered address:** 8 Temasek Boulevard #21-01, Suntec Tower Three, Singapore 038988
- **Alt. address (opengovsg.com):** 6 Battery Road #29-02/03, Singapore 049909
- **Phone:** +65-65189986
- **Email:** service@gname.com / tech@gname.com / business@gname.com / complaint@gname.com
- **Public "leadership":** "Ms. Mandy" (Business Leader), "Mr. Johnson" (Marketing Director) — pseudonyms, no surnames
- **Officers/Directors/Shareholders:** 3 total (per ACRA records) — names not publicly visible; require paid ACRA database access or law enforcement ACRA subpoena
- **ICANN IANA ID:** 1923

### Registrar Relationship
Gname.com both:
1. Operates the SHARE-DNS nameserver infrastructure (registered under same company)
2. Registers the criminal domains that point to SHARE-DNS

This vertical integration (registrar + DNS provider) makes Gname.com a single point of contact for law enforcement seeking to disrupt this infrastructure via ICANN contractual compliance.

---

## PIPGAINERS.COM CLUSTER (co-hosted on Servikus via pipgainers.com)

Discovered through crt.sh analysis — all share a Servikus cPanel server account:
- **pipgainers.com** (account name / billing domain)
- **betaglobalmanagements.com** (BIPPAX / Beta Global Finance — confirmed via www.betaglobalmanagements.com.pipgainers.com cert SAN)
- **toptiercapital.live**
- **muskfoundationpartners.org** (fake Elon Musk foundation)
- **protradeoptions.org**
- **topexpertspro.live**
- **bluemach.engineering**
- **rubiescu.com**
- **colerealestategroupsllc.co**

All share SOA: `ns1.servikus.com. noc.servikus.com.`
pipgainers.com first cert: 2025-04-22 (174 certs total through 2026-03)

---

## MALWAREURL.COM DATA — a.share-dns.com

malwareurl.com tracks 50 recently reported malicious domains using `a.share-dns.com` as nameserver. Threat categories:
- **Android malware:** 33 domains (qdwlj*.top, qdhph*.top, qdmail*.top, qdcdn*.top pattern)
- **Trojan ConnectWise:** 5 domains (bc-support.icu, bc-support.top, bc-help.top, ticai20.com, qohelp.top)
- **Malicious domains:** 8 domains (escybermonday.com, concavix.com, wellnessguru.net, frblackfriday.com, scouttrends.com, infoquests.com, gohubb.com + related.* subdomains)
- **Scam:** 4 domains

**Significance:** SHARE-DNS is used by multiple unrelated threat actor groups (not just this pig-butchering network) — Android malware operators, ConnectWise RAT operators, and various scammers all use SHARE-DNS nameservers. This further supports the assessment that SHARE-DNS is a commercial service, not a dedicated criminal infrastructure provider.

---

*Compiled 2026-03-27. Passive OSINT only.*
