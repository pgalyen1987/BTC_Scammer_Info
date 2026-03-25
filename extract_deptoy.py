#!/usr/bin/env python3
"""
Deep extraction of all intelligence from deptoy.co source code.
"""
import re, json

JS = "/home/me/deptoy/static/js/app.66bc9f716f39a8a33c06.js"
with open(JS, "r", errors="ignore") as f:
    src = f.read()

print(f"Source size: {len(src):,} bytes\n")
results = {}

# ── 1. Email addresses ────────────────────────────────────────────────────────
emails = list(set(re.findall(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}', src)))
# filter out obvious false positives (webpack noise)
emails = [e for e in emails if not e.endswith('.js') and not e.endswith('.css')
          and 'sentry' not in e.lower() and 'webpack' not in e.lower()
          and len(e) > 6]
results['emails'] = emails
print("=" * 60)
print(f"EMAILS ({len(emails)})")
print("=" * 60)
for e in sorted(emails):
    print(f"  {e}")

# ── 2. Phone numbers ──────────────────────────────────────────────────────────
# International format and Chinese mobile
phones = list(set(re.findall(
    r'(?:(?:\+|00)[1-9]\d{6,14}|1[3-9]\d{9}|\b\d{11}\b)', src
)))
# Filter noise - only keep plausible phone numbers
phones = [p for p in phones if len(p) >= 10 and not p.startswith('0000')
          and not re.match(r'^1[0-9]{10}$', p) or p.startswith('+')]
results['phones'] = phones[:30]
print("\n" + "=" * 60)
print(f"PHONE NUMBERS (sample)")
print("=" * 60)
for p in sorted(set(phones))[:20]:
    print(f"  {p}")

# ── 3. All API endpoints ──────────────────────────────────────────────────────
endpoints = list(set(re.findall(r'["\']/(uc/dapp/[^"\'?#\s]{3,})["\']', src)))
endpoints += list(set(re.findall(r'["\'](/api/[^"\'?#\s]{3,})["\']', src)))
endpoints = sorted(set(endpoints))
results['endpoints'] = endpoints
print("\n" + "=" * 60)
print(f"API ENDPOINTS ({len(endpoints)})")
print("=" * 60)
for e in endpoints:
    print(f"  {e}")

# ── 4. All domains and URLs ───────────────────────────────────────────────────
domains = list(set(re.findall(
    r'https?://([a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', src
)))
domains = [d for d in domains if 'cdn' not in d and 'webpack' not in d
           and 'unpkg' not in d and 'polyfill' not in d]
results['domains'] = domains
print("\n" + "=" * 60)
print(f"DOMAINS/URLS ({len(domains)})")
print("=" * 60)
for d in sorted(set(domains)):
    print(f"  {d}")

# ── 5. WeChat and social media IDs ────────────────────────────────────────────
wechat = list(set(re.findall(r'(?:wechat|weixin|wx|微信)[:\s="\'{]*([a-zA-Z0-9_-]{5,30})', src, re.IGNORECASE)))
results['wechat'] = wechat
print("\n" + "=" * 60)
print(f"WECHAT/SOCIAL IDs")
print("=" * 60)
for w in wechat:
    print(f"  {w}")

# ── 6. All hardcoded string values that look like credentials/keys ─────────────
# Look for patterns like apiKey, secret, token, key assignments
keys = re.findall(r'(?:apikey|api_key|secret|token|password|passwd|appid|appKey)\s*[:=]\s*["\']([^"\']{8,})["\']', src, re.IGNORECASE)
results['potential_keys'] = list(set(keys))[:20]
print("\n" + "=" * 60)
print(f"POTENTIAL KEYS/TOKENS")
print("=" * 60)
for k in list(set(keys))[:20]:
    print(f"  {k[:60]}")

# ── 7. IP addresses ───────────────────────────────────────────────────────────
ips = list(set(re.findall(r'\b(?:(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\.){3}(?:25[0-5]|2[0-4]\d|[01]?\d\d?)\b', src)))
ips = [ip for ip in ips if not ip.startswith('0.') and not ip.startswith('255.')
       and ip not in ('127.0.0.1', '0.0.0.0', '255.255.255.255')]
results['ips'] = ips
print("\n" + "=" * 60)
print(f"IP ADDRESSES ({len(ips)})")
print("=" * 60)
for ip in sorted(ips):
    print(f"  {ip}")

# ── 8. Chinese text extraction ────────────────────────────────────────────────
chinese_blocks = re.findall(r'[\u4e00-\u9fff]{4,}', src)
# Deduplicate and filter out very common UI strings
unique_zh = list(set(chinese_blocks))
# Look for names, IDs, contact info patterns
print("\n" + "=" * 60)
print(f"CHINESE TEXT BLOCKS ({len(unique_zh)} unique, showing notable ones)")
print("=" * 60)
# Filter for interesting ones (not pure UI labels)
interesting_zh = [z for z in unique_zh if len(z) > 8 or
                  any(c in z for c in ['联系', '客服', '微信', '邮件', '电话', '地址', '公司', '注册', '备案'])]
for z in sorted(interesting_zh)[:50]:
    print(f"  {z}")

# ── 9. Admin/internal routes ──────────────────────────────────────────────────
admin_routes = re.findall(r'["\']([^"\']*(?:admin|manage|backend|operator|staff|internal|dashboard|system|config)[^"\']*)["\']', src, re.IGNORECASE)
admin_routes = list(set([r for r in admin_routes if len(r) > 3 and '.' not in r[:3]]))
results['admin_routes'] = admin_routes
print("\n" + "=" * 60)
print(f"ADMIN/INTERNAL ROUTES ({len(admin_routes)})")
print("=" * 60)
for r in sorted(admin_routes)[:40]:
    print(f"  {r}")

# ── 10. User roles and permissions ─────────────────────────────────────────────
roles = re.findall(r'(?:role|permission|level|vip|grade|rank)\s*[=:]\s*["\']([^"\']{2,30})["\']', src, re.IGNORECASE)
roles += re.findall(r'["\'](?:role|userType|userLevel|vipLevel|memberType)["\']:\s*["\']?(\d+|[a-zA-Z_]+)["\']?', src)
roles = list(set(roles))
results['roles'] = roles
print("\n" + "=" * 60)
print(f"USER ROLES/LEVELS ({len(roles)})")
print("=" * 60)
for r in sorted(set(roles))[:30]:
    print(f"  {r}")

# ── 11. Payment methods and crypto ────────────────────────────────────────────
# Look for payment channel names, crypto symbols, and wallet patterns
payment = re.findall(r'(?:usdt|trc20|erc20|bep20|btc|eth|trx|payment|withdraw|deposit|recharge)["\s:=,]*([^"\'<>\s]{3,40})', src, re.IGNORECASE)
crypto_symbols = re.findall(r'\b(USDT|BTC|ETH|TRX|BNB|USDC|BUSD|SOL|XRP)\b', src)
results['crypto'] = list(set(crypto_symbols))
print("\n" + "=" * 60)
print(f"CRYPTO/PAYMENT SYMBOLS FOUND")
print("=" * 60)
for c in sorted(set(crypto_symbols)):
    print(f"  {c}")

# ── 12. App version and build info ─────────────────────────────────────────────
versions = re.findall(r'(?:version|ver|build|release)["\s:=]+["\']?([0-9]+\.[0-9]+[^"\'<>\s]*)["\']?', src, re.IGNORECASE)
results['versions'] = list(set(versions))[:10]
print("\n" + "=" * 60)
print(f"VERSION/BUILD INFO")
print("=" * 60)
for v in list(set(versions))[:10]:
    print(f"  {v}")

# ── 13. All unique string paths that look like route definitions ───────────────
routes = list(set(re.findall(r'path:\s*["\']([/][^"\']{2,60})["\']', src)))
results['routes'] = sorted(routes)
print("\n" + "=" * 60)
print(f"FRONTEND ROUTES ({len(routes)})")
print("=" * 60)
for r in sorted(routes):
    print(f"  {r}")

# ── 14. Look for Telegram, WhatsApp, LINE handles ─────────────────────────────
telegram = list(set(re.findall(r't\.me/([a-zA-Z0-9_]{5,32})', src)))
telegram += list(set(re.findall(r'telegram["\s:=]+["\']?(@?[a-zA-Z0-9_]{5,32})', src, re.IGNORECASE)))
whatsapp = list(set(re.findall(r'whatsapp[^"\']*["\']([+0-9]{8,20})["\']', src, re.IGNORECASE)))
results['telegram'] = list(set(telegram))
results['whatsapp'] = whatsapp
print("\n" + "=" * 60)
print(f"TELEGRAM HANDLES")
print("=" * 60)
for t in set(telegram):
    print(f"  {t}")
print(f"\nWHATSAPP NUMBERS")
for w in whatsapp:
    print(f"  {w}")

# ── 15. Google Analytics / tracking IDs ───────────────────────────────────────
ga = re.findall(r'(?:UA-|G-|GTM-)[A-Z0-9-]{5,15}', src)
results['analytics'] = list(set(ga))
print("\n" + "=" * 60)
print(f"ANALYTICS / TRACKING IDs")
print("=" * 60)
for g in set(ga):
    print(f"  {g}")

# ── 16. Look for any names (Chinese or English) in comments/strings ──────────
# Common Chinese name patterns
cn_names = re.findall(r'["\'](?:作者|author|开发者|developer|联系人)["\']?\s*[:=]\s*["\']([^"\']{2,20})["\']', src, re.IGNORECASE)
results['names'] = cn_names
print("\n" + "=" * 60)
print(f"DEVELOPER/AUTHOR NAMES")
print("=" * 60)
for n in cn_names:
    print(f"  {n}")

# ── 17. App ID / platform ID patterns ─────────────────────────────────────────
app_ids = re.findall(r'(?:appId|app_id|platformId|platform_id|siteId)\s*[:=]\s*["\']?([a-zA-Z0-9_-]{4,30})["\']?', src, re.IGNORECASE)
results['app_ids'] = list(set(app_ids))
print("\n" + "=" * 60)
print(f"APP/PLATFORM IDs")
print("=" * 60)
for a in set(app_ids):
    print(f"  {a}")

# ── 18. ICP / license numbers ─────────────────────────────────────────────────
icp = re.findall(r'(?:ICP|备案)[^\s"\'<>]{0,5}(\d{8,12})', src)
icp += re.findall(r'ICP备\S+号', src)
results['icp'] = list(set(icp))
print("\n" + "=" * 60)
print(f"ICP/LICENSE NUMBERS")
print("=" * 60)
for i in set(icp):
    print(f"  {i}")

# ── 19. Deep scan: extract all string literals > 20 chars that look interesting
interesting_strings = []
for match in re.finditer(r'["\']([^"\']{25,120})["\']', src):
    s = match.group(1)
    # Skip obvious code/css/base64 noise
    if re.search(r'[{}();]', s): continue
    if s.startswith('data:') or s.startswith('//') or 'webpack' in s.lower(): continue
    if re.match(r'^[a-f0-9]{32,}$', s): continue  # hex hashes
    if re.match(r'^[A-Za-z0-9+/]{40,}={0,2}$', s): continue  # base64
    # Keep strings with identifiable content
    if any(kw in s.lower() for kw in ['service', 'support', 'contact', 'customer', 'admin',
                                        'manage', 'register', 'login', 'withdraw', 'deposit',
                                        'profit', 'invest', 'trade', 'fund', 'account',
                                        'verify', 'kyc', 'audit', 'agent', 'partner', 'rebate',
                                        'commission', 'bonus', 'reward', 'referral', 'invite',
                                        'telegram', 'whatsapp', 'wechat', 'line', 'mail']):
        interesting_strings.append(s)

results['interesting_strings'] = list(set(interesting_strings))[:100]
print("\n" + "=" * 60)
print(f"INTERESTING STRING LITERALS ({len(set(interesting_strings))})")
print("=" * 60)
for s in sorted(set(interesting_strings))[:80]:
    print(f"  {s}")

# ── 20. Look for any hardcoded addresses in different formats ──────────────────
# TRC20/ETH addresses
tron_addrs = list(set(re.findall(r'\bT[A-Za-z0-9]{33}\b', src)))
eth_addrs = list(set(re.findall(r'\b0x[a-fA-F0-9]{40}\b', src)))
results['tron_addresses'] = tron_addrs
results['eth_addresses'] = eth_addrs
print("\n" + "=" * 60)
print(f"TRON ADDRESSES ({len(tron_addrs)})")
print("=" * 60)
for a in tron_addrs:
    print(f"  {a}")
print(f"\nETH ADDRESSES ({len(eth_addrs)})")
for a in eth_addrs[:20]:
    print(f"  {a}")

# ── 21. Extract all URL paths from API calls ────────────────────────────────────
all_paths = list(set(re.findall(r'["\']([/][a-z][a-z0-9/_-]{3,60})["\']', src)))
all_paths = [p for p in all_paths if not p.endswith('.js') and not p.endswith('.css')
             and not p.endswith('.png') and not p.endswith('.jpg')
             and not p.endswith('.woff') and not p.endswith('.ttf')]
results['all_api_paths'] = sorted(all_paths)
print("\n" + "=" * 60)
print(f"ALL URL PATHS ({len(all_paths)})")
print("=" * 60)
for p in sorted(all_paths):
    print(f"  {p}")

# Save
with open("deptoy_extracted.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n\nAll results saved to deptoy_extracted.json")
