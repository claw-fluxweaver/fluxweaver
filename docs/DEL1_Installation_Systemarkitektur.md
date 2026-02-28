# DEL 1 – Installation & Systemarkitektur

## En nybörjarguide för att sätta upp OpenClaw på Mac Mini

---

## Inledning

Den här delen handlar om att förbereda din Mac Mini för att köra OpenClaw dygnet runt. Vi går igenom allt från vilken hårdvara du behöver till hur du ställer in så att maskinen startar automatiskt.

---

## 1.1 Varför en dedikerad Mac Mini?

En dedikerad maskin innebär att OpenClaw får alla resurser för sig själv. Ingen konkurrens om processor, minne eller nätverk. Dessutom är en Mac Mini tyst, strömsnål och har inbyggd hårdvarusäkerhet.

### Fördelar med dedikerad maskin:
- Stabil drift utan avbrott från andra program
- Enklare felsökning när bara en tjänst körs
- Bättre säkerhet – ingen personlig data på maskinen
- Lägre strömförbrukning (under 10W i vila)

---

## 1.2 Optimal hårdvara – Vad och Varför

### Vilken Mac Mini ska jag välja?

| Modell | Pris (ca) | Passar för | Mitt tips |
|--------|-----------|------------|----------|
| **Mac Mini M4 (2024)** | 7 000+ kr | Allmän drift | **BÄST** |
| Mac Mini M4 Pro | 14 000+ kr | Tung ML/AI | Overkill för de flesta |
| Mac Mini M2 (2023) | 5 000+ kr | Budget | Okej, men M4 är framtidssäker |

**Varför M4?** Den senaste generationen har:
- Bättre neural engine för AI-uppgifter
- Lägre strömförbrukning
- Modernare säkerhetsfunktioner
- Wi-Fi 6E och Bluetooth 5.3

### Hur mycket RAM behöver jag?

**Minimum: 16 GB**
Det räcker för:
- OpenClaw + grundläggande agenter
- Några webbläsarfönster för scraping
- Lätta ML-uppgifter

**Rekommenderat: 24-32 GB**
Detta passar om du vill:
- Köra flera agenter samtidigt
- Köra tyngre ML-modeller
- Ha utrymme för framtida expansion

**Varför inte 8 GB?**
OpenClaw och macOS behöver minst 8 GB bara för att fungera smidigt. Med 8 GB kommer du uppleva seghet och kan behöva stänga av tjänster för att göra andra saker.

### Hur stor SSD behöver jag?

**Minimum: 256 GB**
- macOS: ~45 GB
- OpenClaw: ~2 GB
- Loggfiler: ~10 GB/år
- Reserverat: ~20 GB

**Rekommenderat: 512 GB**
- Ger utrymme för temporära filer
- Rymmer backup utan att det blir trångt
- Bättre prestanda (större SSD = snabbare)

---

## 1.3 macOS-konfiguration – Varför och Hur

### Vilken macOS-version?

**Rekommendation: macOS 15 (Sequoia) eller senaste stable**

**Varför?**
- Nyare versioner har fler säkerhetsfunktioner
-apple uppdaterar regelbundet säkerhetshål
- Äldre versioner kan sakna stöd för nya funktioner

**Hur-uppdaterar-du?**
1. Klicka på Apple-ikonen > System Settings
2. Gå till General > Software Update
3. Ladda ner och installera uppdateringar

### Ska maskinen ha skärm?

**Korta svaret: Nej, den kan köras headless (utan skärm)**

Det finns två sätt att köra en server:

| Metod | Fördelar | Nackdelar |
|-------|----------|----------|
| **Headless** (utan skärm) | Tystare, billigare, säkrare | Svårare att felsöka |
| Med skärm | Enkel att använda | Dyrare, mer exponering |

**Min rekommendation:**
- Köp en billig skärm för konfigurationen
- Koppla in den om du behöver felsöka
- Kör maskinen headless resten av tiden

### Energiinställningar – Varför det är viktigt

En server som stänger av sig själv är värdelös. Här är vad du måste ställa in:

```bash
# Förhindra att datorn sover
sudo pmset -c sleep 0

# Förhindra att disken stängs av
sudo pmset -c disksleep 0

# Skärmen kan stängas av (sparar energi)
sudo pmset -c displaysleep 30
```

**Vad betyder inställningarna?**

| Parameter | Vad det gör | Varför |
|-----------|-------------|--------|
| `sleep 0` | Aldrig viloläge | Server ska alltid vara igång |
| `disksleep 0` | Aldrig stänga av disk | Snabbare åtkomst |
| `displaysleep` | Stäng skärm efter X min | Spara energi |

**Automatisk omstart:**
```bash
# Starta om vid krasch
sudo systemsetup -setrestartfreeze on
```

Detta gör att macOS startar om automatiskt om den fryser. Utan detta måste du fysiskt trycka på strömknappen om något går fel.

---

## 1.4 Användarhantering – Säkerhet först

### Varför en separat användare?

Om du kör OpenClaw under ditt vanliga konto (som har admin-rättigheter) och någon kan komma in i systemet, får de full kontroll. Med ett begränsat konto är skadan mindre.

### Så här skapar du en dedikerad användare

**Via System Settings (enklare):**

1. Öppna System Settings > Users & Groups
2. Klicka på låset och ange ditt lösenord
3. Klicka på "+" för att skapa ny användare
4. Fyll i:
   - New Account: Standard User
   - Full Name: OpenClaw Service
   - Account Name: openclaw
5. Skapa ett starkt lösenord

**Vad du ska undvika:**
- ❌ Admin-rättigheter
- ❌ iCloud-anslutning
- ❌ Autentisering med Apple ID
- ❌ Delad inloggning

### Varför ingen admin?

Admin-konto kan:
- Installera program
- Ändra systemfiler
- Släppa in andra användare

Ett vanligt konto kan:
- Köra program (som OpenClaw)
- Läsa filer det har tillgång till
- Inte förstöra systemet

---

## 1.5 Autostart – Så att OpenClaw alltid körs

### Varför behövs autostart?

Om maskinen startar om eller OpenClaw kraschar, vill du att det startar automatiskt. Annars måste du logga in och starta det manuellt – varje dag.

### LaunchAgents vs LaunchDaemons

macOS har två sätt att starta program automatiskt:

| Typ | Kör som | När | Bäst för |
|-----|---------|-----|----------|
| **LaunchAgent** | Din användare | Efter inloggning | Program som du vill ska köras |
| **LaunchDaemon** | root (admin) | Vid boot | Systemtjänster |

**Vi använder LaunchAgent** eftersom:
- Körs som "openclaw"-användaren (säkrare)
- Startar när användaren loggar in
- Enklare att konfigurera

### Så här skapar du en LaunchAgent

**Steg 1: Skapa mappen om den inte finns**
```bash
mkdir -p ~/Library/LaunchAgents
```

**Steg 2: Skapa plist-filen**

Skapa en fil `~/Library/LaunchAgents/com.openclaw.agent.plist` med följande innehåll:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.openclaw.agent</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/local/bin/openclaw</string>
        <string>gateway</string>
        <string>start</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <dict>
        <key>SuccessfulExit</key>
        <false/>
    </dict>
    <key>StandardOutPath</key>
    <string>/Users/openclaw/.openclaw/logs/openclaw.log</string>
    <key>StandardErrorPath</key>
    <string>/Users/openclaw/.openclaw/logs/error.log</string>
</dict>
</plist>
```

**Vad gör varje del?**

| Tag | Funktion |
|-----|----------|
| `Label` | Unikt namn på tjänsten |
| `ProgramArguments` | Kommandot som ska köras |
| `RunAtLoad` | Starta när filen laddas |
| `KeepAlive` | Starta om om det avslutas |
| `StandardOutPath` | Var loggar ska sparas |

**Steg 3: Ladda tjänsten**

```bash
# Ladda (aktivera)
launchctl load ~/Library/LaunchAgents/com.openclaw.agent.plist

# Starta nu
launchctl start com.openclaw.agent

# Kolla status
launchctl list | grep openclaw
```

### Vad händer nu?

1. **Vid varje omstart:** OpenClaw startar automatiskt
2. **Vid krasch:** OpenClaw startar om inom 60 sekunder
3. **Loggar:** Du kan se vad som händer i loggfilerna

---

## 1.6 Sammanfattning

I den här delen har du lärt dig:

✓ Vilken hårdvara som passar (Mac Mini M4, 16-32 GB RAM, 256+ GB SSD)  
✓ Hur man konfigurerar macOS för 24/7-drift  
✓ Varför och hur man skapar en separat användare  
✓ Hur man får OpenClaw att starta automatiskt  

Nästa del handlar om säkerhet – hur du skyddar din installation från obehörig åtkomst.

---

## Vanliga frågor

**F: Måste jag köpa ny hårdvara?**
S: Nej, en äldre Mac Mini (M1/M2) fungerar också. M4 är bara det bästa valet.

**F: Kan jag köra OpenClaw på min vanliga Mac?**
S: Ja, men det rekommenderas inte eftersom det innebär säkerhetsrisker.

**F: Vad kostar det att köra dygnet runt?**
S: Cirka 10-15 kr/månad i el (vid 1 kWh ≈ 1,5 kr).

---

*Nästa del: DEL 2 – Säkerhet – hur du skyddar din installation*
