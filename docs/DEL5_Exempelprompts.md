# DEL 5 – Exempelprompts

## Färdiga prompts du kan använda med OpenClaw

---

## Inledning

Den här delen innehåller färdiga prompts för olika ändamål. Varje prompt är designad för att:
- vara säker
- förhindra exekvering av extern kod
- ge dig maximal nytta
- följa de säkerhetsregler vi gått igenom

---

## 5.1 System Setup-prompts

### Prompt: Första konfigurationen

```
Konfigurera OpenClaw för första gången.

Krav:
1. Skapa en konfigurationsfil med följande inställningar:
   - Gateway-läge: local
   - Loggning: aktiverad, fil
   - Timeout för sessioner: 30 minuter
   - Max tokens per svar: 4000
   
2. Ange vilka mappar som ska användas för:
   - Workspace (dina filer)
   - Loggar
   - Temporära filer
   
3. Förklara varje inställning och varför den är viktig.

4. Visa hur du startar och stoppar tjänsten.

Formatera svaret som en steg-för-steg-guide.
```

### Prompt: Miljövariabler

```
Jag behöver konfigurera säker hantering av API-nycklar för OpenClaw.

Hjälp mig att:
1. Skapa en .env-fil med följande variabler:
   - OPENAI_API_KEY
   - ANTHROPIC_API_KEY
   - WHATSAPP_TOKEN
   
2. Förklara hur jag läser in dessa i OpenClaw.

3. Ge tips på hur man håller nycklarna säkra.

4. Vad ska jag INTE göra med API-nycklar?
```

### Prompt: Loggrotation

```
Konfigurera loggrotation för OpenClaw.

Uppgifter:
1. Var lagras loggarna som standard?
2. Hur stor kan loggfilen bli utan rotation?
3. Skapa en konfiguration för:
   - Max filstorlek: 10 MB
   - Behåll: 5 gamla filer
   - Komprimera: ja
   
4. Visa hur man kontrollerar att rotation fungerar.
```

---

## 5.2 Säkerhetsprompts

### Prompt: Säkerhetsaudit

```
Gör en säkerhetsgenomgång av min OpenClaw-installation.

Kontrollera och rapportera:
1. Vilka tjänster är aktiva?
2. Vilka portar är öppna?
3. Finns det API-nycklar som exponeras?
4. Hur ser behörigheterna ut för ~/.openclaw/?
5. Finns det varningsmeddelanden i loggarna?

Ge en sammanfattning med:
- Risk nivå för varje fynd
- Åtgärdsförslag för varje problem
- Prioriteringsordning
```

### Prompt: Brandväggskonfiguration

```
Förklara hur man konfigurerar macOS brandvägg för OpenClaw.

Frågor:
1. Hur aktiverar jag brandväggen?
2. Vilka regler behövs för OpenClaw?
3. Vad är stealth mode och bör jag aktivera det?
4. Hur blockerar jag all inkommande trafik utom från specifika IP?

Ge kommandon jag kan köra (efter att du granskat dem).
```

### Prompt: Tailscale-installation

```
Förklara hur jag sätter upp Tailscale för säker fjärråtkomst till min OpenClaw-maskin.

Steg jag behöver:
1. Varför är Tailscale bättre än port forwarding?
2. Hur installerar jag Tailscale på Mac Mini?
3. Hur ansluter jag min andra enhet?
4. Hur når jag OpenClaw via Tailscale?

Avsluta med säkerhetschecklistan för Tailscale.
```

---

## 5.3 Trading-prompts

### Prompt: Marknadsanalys

```
Gör en teknisk analys av Bitcoin (BTC) mot svenska kronor (SEK).

Inkludera:
1. Nuvarande pris och rörelse senaste 24 timmarna
2. Trend: är vi i en upp-, ned- eller sidledes trend?
3. Stöd: identifiera minst 2 stödnivåer
4. Motstånd: identifiera minst 2 motståndsnivåer
5. Volym: är volymen ökande eller minskande?
6. RSI: vad visar den (överköpt/översåld)?
7. Sammanfattning med riskbedömning

Använd öppna källor (inga betaltjänster).
```

### Prompt: Skapa strategi

```
Skapa en trading-strategi baserad på glidande medelvärden (Moving Averages).

Förklara:
1. Hur fungerar glidande medelvärden?
2. Vad är "golden cross" och "death cross"?
3. Definiera entry-villkor (när ska vi köpa?)
4. Definiera exit-villkor (när ska vi sälja?)
5. Ge pseudokod för strategin (inte körbar kod!)

Avsluta med:
- Fördelar med strategin
- Nackdelar/risk
- Marknader den passar bäst för
```

### Prompt: Positionsstorlek

```
Beräkna optimal positionsstorlek för en trade.

Info:
- Konto: 10 000 SEK
- Risk per trade: 2%
- Stop-loss: 5%

Frågor:
1. Vad blir positionsstorleken i kronor?
2. Vad blir risken i kronor om stop-loss triggas?
3. Om take-profit är 10%, vad blir risk/reward-förhållandet?
4. Är detta inom mina riskgränser?
5. Vad blir Kelly Criterion för denna setup?

Visa alla beräkningar steg för steg.
```

### Prompt: Backtesting

```
Jag vill backtesta en SMA Crossover-strategi på Bitcoin.

Antaganden:
- Kort SMA: 15 dagar
- Lång SMA: 30 dagar
- Startkapital: 10 000 SEK
- Period: senaste 365 dagar

Frågor:
1. Vilken data behöver jag samla in?
2. Hur ser logiken ut (pseudokod)?
3. Vilka mått ska jag analysera (win rate, drawdown, etc.)?
4. Vad är viktigt att titta på i resultaten?

Ge ett Python-script som exempel (pseudokod, jag kommer inte köra det).
```

### Prompt: Risk-analys

```
Innan jag gör en trade vill jag ha en riskanalys.

Min setup:
- Instrument: Bitcoin
- Riktning: Köp
- Entry: 500 000 SEK
- Stop-loss: 475 000 SEK
- Take-profit: 575 000 SEK

Frågor:
1. Vad är risken i kronor?
2. Vad är risken i procent?
3. Vad är risk/reward-förhållandet?
4. Är detta inom 2%-regeln?
5. Vilka faktorer kan göra att trade'n misslyckas?
6. Ska jag ta denna trade? (Ja/Nej med förklaring)
```

---

## 5.4 Performance Review-prompts

### Prompt: Analysera trading-resultat

```
Analysera mina trading-resultat för januari 2026.

Data:
- 15 trades totalt
- 9 vinnande (60%)
- 6 förlorande (40%)
- Total vinst: +4 500 SEK
- Största vinst: +1 200 SEK
- Största förlust: -800 SEK
- Genomsnittlig vinst: +500 SEK
- Genomsnittlig förlust: -400 SEK

Frågor:
1. Vad är min win rate?
2. Vad är min genomsnittliga risk/reward?
3. Hur stor är min max drawdown?
4. Är detta en lönsam strategi?
5. Vad kan jag förbättra?

Ge betyg och förbättringsförslag.
```

### Prompt: Portfolio-analys

```
Ge en översikt av min trading-portfölj.

Info:
- 3 olika strategier
- Strategi A: +12% (låg risk)
- Strategi B: +8% (medium risk)
- Strategi C: -3% (hög risk)
- Totalt kapital: 30 000 SEK

Frågor:
1. Hur borde jag fördela kapitalet mellan strategierna?
2. Vilken strategi presterar bäst relativt till risk?
3. Ska jag behålla, öka eller minska respektive strategi?
4. Vad är min totala riskexponering?

Ge en rekommenderad ombalansering.
```

---

## 5.5 Automation-prompts

### Prompt: Daglig rutin

```
Skapa en daglig rutin för min trading med OpenClaw.

Schema:
- 07:00: Kolla öppna positioner
- 08:00: Marknadsöversikt
- 12:00: Lunch - kolla eventuella ändringar
- 16:00: Daglig sammanfattning
- 20:00: Kvällsgenomgång

För varje tidpunkt:
1. Vilka frågor ska jag ställa till OpenClaw?
2. Vilka beslut behöver fattas?
3. Vad ska dokumenteras?

Ge exempel på konkreta prompts för varje tillfälle.
```

### Prompt: Veckovis granskning

```
Skapa en veckovis granskningsrutin.

Inkludera:
1. Vilka mått ska jag följa upp?
2. Vilka frågor ska jag ställa till OpenClaw?
3. Vad ska dokumenteras för veckan?
4. Hur identifierar jag mönster i mina trades?
5. Vad ska in i vecko-rapporten?

Ge en mall jag kan använda.
```

---

## 5.6 Felhantering-prompts

### Prompt: Felsökning OpenClaw

```
OpenClaw svarar inte längre. Hjälp mig felsöka.

Steg jag tagit:
1. Försökte öppna gränssnittet -> Timeout
2. Kollar gateway-status -> ?

Frågor:
1. Vilka kommandon kan jag köra för att diagnostisera?
2. Hur ser jag om tjänsten körs?
3. Var finns loggarna?
4. Hur startar jag om tjänsten säkert?
5. Vad är vanliga orsaker till att OpenClaw slutar svara?

Ge steg-för-steg felsökningsguide.
```

### Prompt: Återställning

```
Min Mac Mini kraschade och jag behöver återställa OpenClaw.

Vad behöver jag göra:
1. Säkerhetskopiera viktig data innan jag börjar?
2. Vilka filer behövs för att återställa?
3. Hur installerar jag OpenClaw på nytt?
4. Hur återställer jag min konfiguration?
5. Hur verifierar jag att allt fungerar?

Ge en checklista för återställning.
```

---

## 5.7 Säkerhetsregler för prompts

### Viktigt att komma ihåg

Varje prompt ovan är designad för att:

| Princip | Beskrivning |
|--------|-------------|
| **Ingen exekvering** | Aldrig be om att köra kod |
| **Analysera** | Endast ge råd och analyser |
| **Dokumentera** | Allt ska dokumenteras |
| **Fråga först** | Vid tveksamhet, fråga användaren |

### Egenskaper hos säkra prompts

✅ **Gör:**
- Be om analyser och förklaringar
- Be om pseudokod (inte körbar)
- Be om steg-för-steg-guider
- Fråga innan viktiga beslut

❌ **Gör inte:**
- Be om att köra kommandon
- Be om att installera paket
- Ge kommandon som ska exekveras
- Anta att det är säkert

---

## 5.8 Sammanfattning

I den här delen har du färdiga prompts för:

✓ Systemkonfiguration  
✓ Säkerhetsgenomgång  
✓ Trading-analys  
✓ Strategiskapande  
✓ Riskhantering  
✓ Backtesting  
✓ Performance Review  
✓ Automation  
✓ Felhantering  

---

## Användningstips

1. **Anpassa** – Ändra parametrar efter dina behov
2. **Kombinera** – Vissa prompts fungerar bra ihop
3. **Iterera** – Förfina prompterna baserat på resultat
4. **Dokumentera** – Spara framgångsrika prompts

---

## Exempel: Kombinera prompts

```
Morgonrutin (kombination):
1. "Vad är priset på BTC/SEK just nu?"
2. "Vad visar teknisk analys för BTC idag?"
3. "Vilka positioner har jag just nu?"
4. "Finns det några triggers att titta på?"
```

---

*Slut på dokumentationen. Nu har du allt du behöver för att driftsätta och använda OpenClaw på ett säkert sätt!*
