# Telegram Groups OSINT — 2026-04-19

**Session account:** ID 7844921887  
**Groups analysed:** 23  
**Method:** Joined groups scanned via Telethon; blockchain data via Solana RPC

---

## Group Inventory

| # | Title | Telegram URL | Members | Relevance |
|---|-------|-------------|---------|-----------|
| 1 | NANOLITR CTO | t.me/NANOLITECTO1 | 3 | CONFIRMED — Nanolite pump.fun token |
| 2 | ʟᴏʀᴅʟᴇɢᴇɴᴅ ˣ Sir Nga Du / Aztex'Athansia | t.me/aplewk19 | 2 | NOT RELATED — gaming username |
| 3 | Бухгалтерия без головной боли | — | 662 | NOT RELATED — Russian accounting |
| 4 | nano Lite Training Center | — | 181 | POSSIBLE — name match only |
| 5 | БухгалтерНатива | — | 100 | NOT RELATED — Russian accounting |
| 6 | AZTEX FX | t.me/aztexfx | 192 | NOT RELATED — Indonesian forex channel |
| 7 | Ваш Бухгалтер | — | 122 | NOT RELATED |
| 8 | Global Macro Trends 015 | — | — | NOT RELATED |
| 9 | NANOLITESOL | — | 3 | POSSIBLE — name match |
| 10 | Бухгалтерия и бизнес | — | 264 | NOT RELATED |
| 11 | the_nanolite | — | 3 | POSSIBLE — name match |
| 12 | 吃瓜🍉 (Chinese) | — | 5 | UNKNOWN |
| 13 | 1:C Бухгалтерия и кд | — | 58 | NOT RELATED |
| 14 | 𝗔𝘇𝗧𝗲𝗫 𝐒𝐇𝐎𝐏 🛍️ | — | 3 | UNKNOWN — keyword hits on aztex |
| 15 | İdman (Azerbaijani) | — | 7 | NOT RELATED |
| 16 | MSG-2139Exchange-Support | t.me/msg0024 | 30 | **CONFIRMED SCAM — 2139Exchange ops** |
| 17 | 2139exchange New Somali | t.me/NewSomalimember | 23 | **CONFIRMED SCAM — victim recruitment** |
| 18 | Byxg 🔥🔥🔥🔥 | t.me/byxgg | 24 | **CONFIRMED SCAM — BYXG platform launch** |
| 19 | Bissnex | t.me/Djoum12 | 2 | Name match — French, likely unrelated |
| 20 | AzTextil | — | 78 | NOT RELATED — textile business |
| 21 | Nano Lite Computer | — | 2 | POSSIBLE — name match |
| 22 | Aztex Studio 🧡 | — | 8 | POSSIBLE — creative studio |
| 23 | Route Finder | t.me/bankingwithshayeri | 4 | Name match — banking education, unrelated |

---

## Confirmed Scam Groups

### 1. MSG-2139Exchange-Support (id=2124293363)
**URL:** https://t.me/msg0024  
**Description:** "Mega Team Support"  
**Activity:** May–June 2024 (14 messages, now dead/inactive)  

**Key messages:**
- Fake testimonial x4: *"The business model strategy of the MEGA Investment Team and The 2139 Exchange is highly effective. They emphasize ensuring investors enjoy the returns on their investments by encouraging timely withdrawals and maximizing profits."*
- MLM recruitment: *"Complete your 5 Persons now to qualify"* (Weekly bonus to Manager rank)
- OKX referral: `https://okx.com/join/78880763` — referral code **78880763** (KYC subpoena lead)
- Generic hype: "Clean win", "Let's Gooo", "Another very clear win"

**Intelligence value:** OKX referral code 78880763 is associated with a KYC'd OKX account. A legal request to OKX could identify the account holder.

---

### 2. 2139exchange New Somali (id=2200073606)
**URL:** https://t.me/NewSomalimember  
**Description:** "Soo dhawada" (Somali: "Welcome")  
**Members:** 23  

**Intelligence value:** Confirms the operation specifically targets Somali-speaking victims. Consistent with known recruitment pattern through diaspora communities. No message content retrieved (no keyword hits in 300-message window = likely image/video heavy).

---

### 3. Byxg 🔥🔥🔥🔥 (id=1724631775)
**URL:** https://t.me/byxgg  
**Members:** 24  
**Activity:** March 2023 (launch announcement)

**Key message (Arabic):**
> "تم إطلاق المنصة الجديدة رسميًا... اسم المنصة: BYXG ✅ إعادة الشحن والسحب على الفور، دون أي قيود ✅ لدى BYXG 3 طرق للاستثمار ✅ 0.4٪ ربح كل 3 ساعات"

Translation: "New platform officially launched... Platform name: BYXG ✅ Instant deposits and withdrawals ✅ 3 investment methods ✅ 0.4% profit every 3 hours, max daily profit..."

**Intelligence value:** Confirms BYXG was launched March 2023, Arabic-language, and uses the same 3-hour cycle / percentage profit model as documented in other BYXG intel. Pre-dates the AZTEX/BIPPAX 2023 active period.

---

## NANOLITE Solana Token — NANOLITR CTO Group

### Group Info
**URL:** https://t.me/NANOLITECTO1  
**Members:** 3 (very small — operators only)  
**Description:** "Let's run this back guys — https://t.me/+KrQ3uckiS25iMTQ6" (private invite)  
**Activity:** September–October 2025 (72 keyword hits)

### Token Contract
| Field | Value |
|-------|-------|
| **Contract** | `GNHyhJ4qsNGKdHukUFQZnGAz5TMJjoYd6RWGUVXY6wuM` |
| **Symbol** | NANO |
| **Platform** | Solana — pump.fun → PumpSwap AMM |
| **Launched** | 2025-09-01 |
| **Last active** | 2026-04-02 |
| **Total supply** | ~999 billion (6 decimals) |
| **Mint authority** | REVOKED |
| **Liquidity pool** | `EGLuXiEALbLtBaibYXyMX88EuxSGP3ZguSspyJrtQcgJ` (PumpSwap) |

### Alert Bots
Two Telegram bots posted buy alerts in the group:
- **ID 5976408419** — posted Solscan-format buy alerts
- **ID 5434266369** — posted DEX bot-format buy alerts

Both bots track the same wallets and post simultaneous alerts — likely Maestro/BonkBot style trading bots.

### Key Buyer Wallets (38+ unique addresses observed)
These wallets were the buyers shown in the Telegram buy alerts. The three repeat buyers (likely operator/insider accounts) are now empty/closed — drained after the pump:

| Wallet | Status | Notes |
|--------|--------|-------|
| `GYgvpLpfaD72CtCftiZzAmcDCtEVoxkWTFsSSaickJUX` | Empty/closed | Most frequent buyer |
| `G9WNoUxfRwBN93NNDorvirRWWiSFAUurU5oHYTjb89Kq` | Empty/closed | Second most frequent |
| `GL3wnv4qzMaU9NHqTVFdQdSmpGG2LpM8aXNMMoJmz7UX` | Unknown | Third repeat buyer |

Full wallet list from buy alerts (38 addresses):
`13BGv7vPDgVUg8DfE9Qvu4mUCxafhwhnYffjLX4dnNRg`, `2tZAVdzgwjaGet99HDqwgqjUBPXMReV8wqk54pzQWVbr`, `2zDdDkB4FKL4reiyyuHNUpHiEoMfRcvRvEvo6jfo6yfh`, `3xg21Qyh2hZgQN4cGdmyydbscwEUVZfz4VkuoaxxDntc`, `4gWz6YCyWFyqiiBjUdGFuF4fgJ38pvyUHb8Kw8oHNyHB`, `54QjCSvUJArwT4NQL5BBW4USb2KU6cstygKo8oMu9mGB`, `5qGypTttz4Laxy5sUaJmK9uAPEjjsG3T3pFnZ3GZGia2`, `6YvFUejJpuwhBtWUmEeA68uXUkASFTVGDuFD3oybsdAY`, `7VSaH9sGaaKpyD7r1TsdrP1dcPjua6sFZhLpAZcEwi7P`, `7ozp41bisVQ47ADExB4Ckpd1qpdrELnAYYRxendosA2w`, `8qJroP9SDbm3J6EyDhvrgvmHMYthM2fZSZE6KoWdCgBQ`, `92zDx4Jr3nR4r8fcZ3WgYQDfQcq9rvY3houtgKsn7KY4`, `9EtkS1QTPkFkULMXpeeJ8jMmj1Y5w29b631WmYAttz3e`, `9okYr6koDTeKfgf2vhzz7rrsxni8s5kbXgb2aJgA1sPn`, `ABQ3uuB73sCwiLHz2yUUrN9AswtqjkY1KQJFiBpZULUX`, `AXESnyQpeQwDZHPcSh7AngQt1DjX7aWxpMq3W6Hxnosf`, `AkHseYMg2H2Rb9xuAn3FLK8W9rQbrGRNShksufnENupc`, `AnbfcGif5UL4Whzw4vVSvyE8JkjULqdeoCCwJ4pXxNz3`, `AzgLipdWkfRqNeuXyxQPdc88YcbdmYBMyhakFHLCXZPY`, `B849zvVu1q9fNEoUWbZZqoAPBf157XaWmMJBD2chjn7M`, `BZAqxbZ9196c8uVGRAJuYrrYkTkSwkykCNaFeougN265`, `CMungup5y4KwUiGb2QJtT24ZvBpwWz8a9B9LUzLbyPFs`, `CwUwMyceZmGrVuKiAUFKTCApjLuDkyo2o8U7ubXNwx1h`, `D5qceGc9ZHZ39GfCxhESwvyDhBvW42uxxmvyAVxQNTf8`, `D8F1owsUKGepi3514az6hrjHTghSuCdTJgCav129UbCX`, `DkLqsPAJkyA5vYHokkMEZoKffRH6V214dD8g85QfPbuP`, `FVrzkaaH7TKw5y6qwokjVYSewsU3GMXCq7SPctc2qev3`, `FYtW7YSkpeWbLugJ3dTYg34dEEuMJNhL91t8YWDjDM4T`, `G97pX2TWNC6yQwCCyFD1xMqu3hDrdfEtQnnkx2zKUedp`, `G9WNoUxfRwBN93NNDorvirRWWiSFAUurU5oHYTjb89Kq`, `GL3wnv4qzMaU9NHqTVFdQdSmpGG2LpM8aXNMMoJmz7UX`, `GYgvpLpfaD72CtCftiZzAmcDCtEVoxkWTFsSSaickJUX`, `Gg5ckCHwJejX6cbRSnDtQYfQ9xvbL6EW3gKeUeV9TeeV`, `HV1KXxWFaSeriyFvXyx48FqG9BoFbfinB8njCJonqP7K`, `JBqdRUCPYNUhQfc4CMzimw9Rha7qCgazNBoKZXqNPvRU`, `VbPCXTceE6fMTkzX7xjauUgZxj1u26JM1UZZFgvx81H`, `f2n8WTLx71HwPxtp28sZAkgtisBLkAV5HkxEKdiXbZq`

### Private Invite Link
`https://t.me/+sylQcINZ-0BiZGI6` — inner circle group linked from NANOLITR CTO description

### Assessment
The NANOLITE/NANO Solana token appears to be a secondary operation run by some of the same operators — a pump.fun memecoin launched September 2025 with coordinated buy alerts to create artificial volume/price action. The "CTO" (community takeover) framing is a common pump.fun meta — operators claim they've taken over a dead token and use buy bots to manufacture momentum. The connection to the Nanolite fraud brand (used as the fake investment platform) is the name overlap; whether it's the same individuals or copycat branding requires further investigation.

---

## Action Items / Subpoena Leads

| Target | Platform | Legal Basis |
|--------|----------|-------------|
| OKX referral 78880763 | OKX exchange | Wire fraud — account used to route scam victims |
| pump.fun NANO token deployer | Solana blockchain / pump.fun | Fraud — false promotion |
| t.me/+sylQcINZ-0BiZGI6 | Telegram | Private scam coordination group |
| t.me/NewSomalimember | Telegram | Victim recruitment channel |
| t.me/msg0024 | Telegram | Scam support channel |
