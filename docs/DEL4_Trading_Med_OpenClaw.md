# DEL 4 – Trading med OpenClaw

## En nybörjarguide för att bygga trading-system med AI

---

## Inledning

Trading handlar om att köpa och sälja tillgångar (aktier, krypto, valutor) för att tjäna pengar. Med OpenClaw kan du bygga kraftfulla trading-system som analyserar marknader och hjälper dig fatta beslut. Den här delen förklarar hur du kommer igång på ett säkert sätt.

---

## 4.1 Varför använda AI för trading?

### Traditionell trading vs AI-assisterad

| Aspekt | Traditionell | AI-assisterad |
|--------|-------------|---------------|
| Analys | Manuell | Automatiserad |
| Hastighet | Långsam | Snabb |
| Data | Begränsad | Massiv |
| Emotion | Påverkar | Objektiv |

### Vad OpenClaw kan hjälpa med

OpenClaw kan:
- Analysera marknadsdata
- Söka efter mönster
- Skapa strategier
- Skriva backtestningskod
- Analysera risker
- Dokumentera beslut

**Men:** OpenClaw handlar INTE åt dig – det ger råd och analyser.

---

## 4.2 Trading-utvecklingsfaser

### Fas 1: Backtesting (Testa på historisk data)

**Vad det är:**
Du testar strategi på g enammal data för att se hur den hade presterat.

**Varför det är viktigt:**
Innan du risikerar pengar vill du veta om strategin ens fungerar historiskt.

**Hur OpenClaw hjälper:**
- Beskriv din strategi
- OpenClaw kan skriva backtestningskod
- Analysera resultat

### Fas 2: Paper Trading (Låtsaspengar)

**Vad det är:**
Du "handlar" med falska pengar i realtid.

**Varför det är viktigt:**
Du får verifiera att strategin fungerar i verkligheten, inte bara historiskt.

**Hur det fungerar:**
- Många mäklare erbjuder "sandbox" eller "paper trading"
- Du får falskt konto med riktiga marknadspriser
- Inga riktiga pengar riskeras

### Fas 3: Live Trading (Riktiga pengar)

**Vad det är:**
Du handlar med riktiga pengar.

**⚠️ VARNING:**
- Börja smått
- Ha strikta riskregler
- Övervaka konstant i början

---

## 4.3 Kom igång – Steg för steg

### Steg 1: Välj en marknad

| Marknad | Svårighet | Tillgänglighet |
|---------|-----------|-----------------|
| Aktier | Medium | Hög |
| Krypto | Låg | Mycket hög |
| Valutor (Forex) | Medium | Hög |
| Råvaror | Hög | Medium |

**Rekommendation för nybörjare:** Börja med krypto (Bitcoin/Ethereum) på grund av:
- Låg inträdesbarriär
- 24/7 marknad
- Massor av data
- Sandbox-testning tillgänglig

### Steg 2: Välj en broker/API

| Broker | Sandbox | API | Land |
|--------|---------|-----|------|
| **Alpaca** | ✅ Ja | REST | USA |
| **Interactive Brokers** | ✅ Ja | API | Global |
| **Binance** | ✅ Ja | REST | Global |
| **Kraken** | ❌ Nej | API | Global |

**Rekommendation:** Alpaca (enkel API, bra dokumentation)

### Steg 3: Samla data

Innan du handlar behöver du data. OpenClaw kan hjälpa till med:

```python
# Exempel: Hämta aktiedata (PSEUDOKOD – inte för körning)
import requests

# Hämta Bitcoin-priser
response = requests.get("https://api.coingecko.com/api/v3/coins/bitcoin/market_chart?vs_currency=sek&days=365")
data = response.json()
prices = data['prices']
```

### Steg 4: Definiera en strategi

En trading-strategi behöver:

| Komponent | Beskrivning |
|-----------|-------------|
| **Entry** | När ska du köpa? |
| **Exit** | När ska du sälja (vinst/förlust)? |
| **Risk** | Hur mycket per trade? |

**Exempel: Glidande medelvärden (SMA Crossover)**

```
ENTRY: Köp när kort SMA korsar över lång SMA
EXIT: Sälj när kort SMA korsar under lång SMA
RISK: Max 2% av konto per trade
```

---

## 4.4 Riskhantering – DEN VIKTIGASTE DELEN

### Varför riskhantering?

Utan riskhantering kommer du förlora allt. Det är inte "om" utan "när".

### Grundläggande regler

| Regler | Värde |
|--------|--------|
| **Max risk per trade** | 2% av konto |
| **Max total risk** | 6% av konto |
| **Risk/Reward minimum** | 1:2 |
| **Max drawdown** | 20% |

### Positionsstorlek – Hur mycket ska du köpa?

Formel:

```
position_size = (konto × risk_per_trade) / stop_loss
```

**Exempel:**

- Konto: 10 000 kr
- Risk per trade: 2% = 200 kr
- Stop-loss: 5%

```
position_size = 10000 × 0.02 / 0.05 = 4 000 kr
```

Du köper för 4 000 kr. Om priset faller 5% och du säljer, förlorar du 200 kr (2% av konto).

### Stop-loss – Automatisk保

**Vad är stop-loss?**
Ett pris där du automatiskt säljer för att begränsa förlusten.

**Varför det är viktigt:**
- Tar bort emotioner
- Förhindrar stora förluster
- Sömnen blir bättre

---

## 4.5 Backtesting – Testa din strategi

### Vad är backtesting?

Du kör din strategi på historisk data för att se hur den hade presterat.

### Exempel: SMA Crossover

```python
# PSEUDOKOD – dokumentation, inte körbar kod

def sma_crossover_strategy(prices, short_period=15, long_period=30):
    """
    Köp när kort SMA > lång SMA
    Sälj när kort SMA < lång SMA
    """
    trades = []
    position = None
    
    for i in range(long_period, len(prices)):
        short_sma = calculate_sma(prices[:i], short_period)
        long_sma = calculate_sma(prices[:i], long_period)
        
        # Köp-signal
        if short_sma > long_sma and position is None:
            trades.append({'action': 'BUY', 'price': prices[i], 'day': i})
            position = 'long'
        
        # Sälj-signal
        elif short_sma < long_sma and position == 'long':
            trades.append({'action': 'SELL', 'price': prices[i], 'day': i})
            position = None
    
    return trades
```

### Analysera resultat

Efter backtesting, titta på:

| Mått | Vad det visar |
|------|---------------|
| **Total avkastning** | Hur mycket strategin tjänade |
| **Win rate** | % av trades som var vinst |
| **Genomsnittlig vinst/förlust** | Risk/reward |
| **Max drawdown** | Största dippen |
| **Antal trades** | Hur ofta det handlar |

---

## 4.6 OpenClaw-prompts för trading

### Prompt: Analysera marknaden

```
Analysera Bitcoin (BTC/SEK) just nu:

1. Vad är det nuvarande priset och hur har det sett ut de senaste dagarna?
2. Vilken trend rör vi oss i (upp, ned, sidledes)?
3. Finns det några tydliga stöd- eller motståndsnivåer?
4. Vad säger volymen – är det köparna eller säljarna som dominerar?
5. Finns det några viktiga nyheter som påverkar marknaden?

Avsluta med en kort sammanfattning och riskbedömning.
```

### Prompt: Skapa strategi

```
Skapa en trading-strategi baserad på RSI (Relative Strength Index).

Inkludera:
1. Förklaring av hur RSI fungerar
2. Entry-villkor (när ska vi köpa?)
3. Exit-villkor (när ska vi sälja?)
4. Riskhantering (stop-loss, positionsstorlek)
5. Fördelar och nackdelar med strategin

Ge pseudokod (inte körbar kod) för att illustrera logiken.
```

### Prompt: Risk-analys

```
Innan jag gör en trade på Bitcoin vill jag ha en riskanalys:

Konto: 10 000 SEK
Planerad position: Köp för 5 000 SEK
Entry-pris: 500 000 SEK
Stop-loss: 475 000 SEK (5% ned)
Take-profit: 575 000 SEK (15% upp)

Besvara:
1. Vad är risken i kronor och procent?
2. Vad är risk/reward-förhållandet?
3. Är detta inom mina riskgränser (2% per trade)?
4. Vad kan gå fel?
5. Ska jag göra denna trade?
```

---

## 4.7 Säkerhet vid trading

### ⚠️ VARNINGAR

1. **Aldrig handla med pengar du inte har råd att förlora**
2. **Backtesta ALLTID innan live trading**
3. **Börja med liten position**
4. **Ha alltid stop-loss**
5. **Dokumentera allt**

### Säkerhet för API-nycklar

```bash
# ALDRI i kod!
API_KEY = "sk-live-123456789"

# Använd miljövariabler
export BINANCE_API_KEY="din-nyckel"
export BINANCE_SECRET="din-hemlighet"
```

### Isolera trading-konto

Skapa ett separat konto för trading:
- Separat från main-konto
- Begränsad insättning
- Aktivera 2FA

---

## 4.8 Sammanfattning

I den här delen har du lärt dig:

✓ Varför AI kan hjälpa med trading  
✓ De fyra faserna (backtest → paper → sandbox → live)  
✓ Grundläggande strategi-koncept  
✓ Vikten av riskhantering  
✓ Hur man beräknar positionsstorlek  
✓ Backtesting-grunder  
✓ Säkerhetsregler för trading  

---

## Checklista för trading

- [ ] Välj marknad (krypto/aktier)
- [ ] Skapa sandbox-konto
- [ ] Definiera strategi
- [ ] Backtesta strategin
- [ ] Sätt riskgränser
- [ ] Testa med paper trading
- [ ] Börja med liten position
- [ ] Dokumentera allt

---

## Vanliga frågor

**F: Kan OpenClaw handla automatiskt?**
S: OpenClaw kan ge rekommendationer men bör inte köras automatiskt utan övervakning. Det är en assistent, inte enautomatisk trader.

**F: Hur mycket pengar behöver jag?**
S: Börja med det minsta möjliga. Det viktiga är att lära sig, inte att tjäna pengar direkt.

**F: Vilken tidsram ska jag handla på?**
S: Nybörjare: Dagshandel är svårt. Börja med veckor eller månader (swing trading).

**F: Vad är det vanligaste felet?**
S: Att hoppa över riskhantering och börja med för stora positioner direkt.

---

*Nästa del: DEL 5 – Exempelprompts*
