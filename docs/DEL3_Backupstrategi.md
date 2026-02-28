# DEL 3 – Backupstrategi

## En nybörjarguide för att skydda din data

---

## Inledning

Hardware kan gå sönder. Misstag händer. Katastrofer inträffar. Utan backup är allt ditt arbete förlorat för alltid. Den här delen förklarar hur du skyddar dig.

---

## 3.1 Varför backup är så viktigt

### Vad händer utan backup?

| Scenario | Konsekvens |
|----------|------------|
| Hårddisk kraschar | Allt borta |
| Ransomware | Allt krypterat |
| Misstag | Raderad fil = borta för alltid |
| Stöld | Ingen data kvar |
| Naturkatastrof | Allt förstört |

### Den smärtsamma sanningen

De flesta som förlorar data trodde "det händer inte mig".

Tills det händer.

---

## 3.2 3-2-1-backupregeln

Den enklaste och mest effektiva strategin:

| Del | Betydelse | Exempel |
|-----|-----------|---------|
| **3** | Tre kopior av data | Original + 2 backuper |
| **2** | Två olika mediatyper | Disk + Moln |
| **1** | En kopia offsite | På annan plats |

### Praktiskt för OpenClaw:

```
┌─────────────────┐
│  Original-data  │  ← Din Mac Mini
│  (OpenClaw)    │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐ ┌───────┐
│ Lokal │ │ Extern│
│backup │ │ disk  │
└───┬───┘ └───┬───┘
    │         │
    └────┬────┘
         ▼
   ┌──────────┐
   │  Moln    │
   │ (offsite)│
   └──────────┘
```

---

## 3.3 Time Machine – macOS inbyggda backup

### Vad är Time Machine?

Time Machine är macOS egen backup-lösning. Den:
- Sparar varje versions av dina filer
- Gör det automatiskt
- Kan återställa precis vad som helst

### Varför Time Machine?

| Fördel | Nackdel |
|--------|----------|
| Inbyggd (gratis) | Kräver extern disk |
| Automatisk | Kan inte användas för server |
| Versionshistorik | Begränsad till Mac |

### Konfigurera Time Machine

**Steg 1: Anslut extern disk**

Köp en extern SSD på minst 256 GB. Anslut till Mac Mini.

**Steg 2: Aktivera Time Machine**

```bash
# Via System Settings:
# System Settings > General > Time Machine > On
```

**Steg 3: Välj backup-disk**

Välj din externa disk som backup-mål.

### Vad ska inkluderas?

```
✅ Inkludera:
├── ~/Library/Application Support/OpenClaw/
├── ~/.openclaw/config/
├── ~/.openclaw/workspace/
└── ~/Documents/ (om relevant)

❌ Exkludera:
├── ~/.openclaw/logs/       (kan återskapas)
├── ~/.openclaw/cache/       (onödigt)
└── ~/Library/Caches/       (temporärt)
```

### Exkludera mappar

```bash
# Exkludera onödiga mappar
sudo tmutil addexclusion ~/.openclaw/logs
sudo tmutil addexclusion ~/.openclaw/cache
sudo tmutil addexclusion ~/Library/Caches
```

---

## 3.4 Externa backuper – lokala och krypterade

### Varför extern disk?

Time Machine på extern disk ger:
- Fysisk separation (om Mac Mini stjäls/brinner)
- Snabb återställning
- Krypteringsalternativ

### Krypterad backup

**Varför kryptera?**
- Om disken stjäls är allt läsbart
- Med kryptering är allt obrukbart utan lösenord

**Skapa krypterad disk:**

1. Öppna Disk Utility
2. Format: APFS (Encrypted)
3. Ange lösenord
4. Spara återställingsnyckel

**Eller via terminal:**

```bash
# Skapa krypterad disk image
hdiutil create -size 50g -fs APFS -encryption AES-256 \
  -volname "OpenClawBackup" ~/OpenClawBackup.sparsebundle
```

---

## 3.5 Offsite backup – molnet

### Varför moln?

| Fördel | Nackdel |
|--------|---------|
| Åtkomst från överallt | Kostar pengar |
| Oberoende av plats | Kräver internet |
| Brand-/tjuvsäkert | Privatlivsaspekter |

### Alternativ för Mac

| Tjänst | Pris | Integrering |
|--------|------|-------------|
| **iCloud** | Från 12 kr/mån | Inbyggd |
| **Backblaze** | 70 kr/mån | Bra, billig |
| **BorgBase** | Friivol | Öppen källkod |
| **rsync.net** | Från $5/mån | Unix-vänligt |

### Använda Backblaze (exempel)

1. Ladda ner Backblaze för Mac
2. Installera och konfigurera
3. Välj mappar att backs uppa
4. Låt det köra automatiskt

---

## 3.6 Vad ska backas upp för OpenClaw?

### Kritiskt (måste backas)

| Mapp | Innehåll |
|------|----------|
| `~/.openclaw/config/` | Konfiguration, API-nycklar |
| `~/.openclaw/workspace/` | Dina agenter, minnen |
| `~/Library/Application Support/OpenClaw/` | Inställningar |

### Mindre kritiskt (kan återskapas)

| Mapp | Kommentar |
|------|-----------|
| `~/.openclaw/logs/` | Kan återskapas |
| `~/.openclaw/cache/` | Onödigt |
| `~/Library/Caches/` | Onödigt |

---

## 3.7 Testa återställning – VIKTIGT

### Varför testa?

En backup som inte fungerar är värdelös. Du måste veta att den faktiskt fungerar.

### Hur ofta testa?

- **Månadsvis:** Fullständig återställning
- **Efter ändringar:** Testa specifika filer
- **Årligen:** Fullständig katastrofåterställning

### Enkelt test: Återställ en fil

1. Ta bort en fil (som du kan återskapa)
2. Gå till Time Machine
3. Hitta filen
4. Återställ den
5. Verifiera att allt stämmer

### Avancerat test: Återställ till ny maskin

1. Formatera en extern disk
2. Installera macOS
3. Återställ från Time Machine
4. Verifiera att OpenClaw fungerar

---

## 3.8 Automatisk verifiering

### Script för att verifiera backup

Skapa ett enkelt script som körs regelbundet:

```bash
#!/bin/bash
# backup_check.sh - Körs varje vecka

BACKUP_PATH="/Volumes/Time Machine Backups"
LOG_FILE="$HOME/.openclaw/logs/backup_check.log"

echo "=== Backup Check $(date) ===" >> $LOG_FILE

# Kolla om backup-disk är ansluten
if [ -d "$BACKUP_PATH" ]; then
    echo "✓ Backup disk connected" >> $LOG_FILE
    
    # Kolla senaste backup
    LAST_BACKUP=$(tmutil latestbackup)
    echo "✓ Latest backup: $LAST_BACKUP" >> $LOG_FILE
else
    echo "⚠ WARNING: Backup disk NOT connected!" >> $LOG_FILE
fi
```

### Schemalägg med cron

```bash
# Lägg till i crontab (kör varje söndag kl 03:00)
0 3 * * 0 ~/bin/backup_check.sh
```

---

## 3.9 Sammanfattning

I den här delen har du lärt dig:

✓ Varför backup är livsviktigt  
✓ 3-2-1-regeln – tre kopior, två medier, en offsite  
✓ Time Machine – macOS inbyggda lösning  
✓ Externa krypterade backuper  
✓ Offsite backup (moln)  
✓ Vad som ska backas för OpenClaw  
✓ Viktigheten av att testa återställning  
✓ Automatisk verifiering  

---

## Checklista för backup

- [ ] Externa disk inköpt och ansluten
- [ ] Time Machine konfigurerad
- [ ] Korrekta mappar inkluderade/exkluderade
- [ ] Krypterad disk aktiverad
- [ ] Molnbackup konfigurerad (rekommenderat)
- [ ] Första testet gjort
- [ ] Automatisk verifiering schemalagd

---

## Vanliga frågor

**F: Kan jag använda samma disk för Time Machine och annat?**
S: Ja, men det rekommenderas inte. Om disken fylls kan backupen pausas.

**F: Hur lång tid tar första backupen?**
S: Beror på mängden data. Första backupen kan ta timmar.

**F: Måste jag betala för molnbackup?**
S: Nej, men gratisalternativ har begränsningar. Backblaze är billigt (~$7/mån).

**F: Vad händer om jag byter Mac?**
S: Time Machine fungerar mellan Mac-datorer. Starta från din nya Mac och välj "Återställ från Time Machine".

---

## Riktlinjer för OpenClaw-specifika scenarier

### Scenario: Hårddisk kraschar

1. Byt ut hårddisken
2. Installera macOS
3. Återställ från Time Machine
4. Installera OpenClaw på nytt
5.Verifiera konfiguration

### Scenario: Ransomware

1. Koppla bort allt nätverk
2. Identifiera och ta bort skadlig kod
3. Formatera och installera om
4. Återställ från ren backup (före attacken)
5. Förbättra säkerheten

### Scenario: Stöld

1. Använd "Find My" om aktiverat
2. Spärra Mac via iCloud
3. Återställ till ny maskin från molnbackup
4. Ändra alla lösenord

---

*Nästa del: DEL 4 – Trading med OpenClaw*
