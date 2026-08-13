---
namn: startskript-far-inte-blockera
beskrivning: Onyxias init-skript fördröjer när tjänsten blir tillgänglig — lägg bara sekundsnabba saker där och kör installationer i en synlig VS Code-terminal i stället.
typ: verktyg
uppdaterad: 2026-08-13
---

Init-skriptet i Onyxias startformulär (`init.personalInit`) körs innan tjänsten
blir tillgänglig. Allt du lägger där är väntetid framför en tom skärm. **Lägg bara
sådant som tar sekunder** — kataloger, konfigurationsfiler, starta en lätt
bakgrundsprocess. Installationer hör hemma efteråt.

**Varför:** grundinstallationen av labbet tar ~1 minut och Open WebUI ~4 minuter.
Läggs det i init-skriptet blir varje uppstart fem minuter av ingenting, och
misslyckas något syns det bara i en logg ingen läser.

**Så använder du det:** låt init-skriptet skriva `.vscode/tasks.json` i den mapp
VS Code öppnar (`$WORKSPACE_DIR`, inte repot) med en task som har
`"runOptions": {"runOn": "folderOpen"}`. Då öppnas ett synligt terminalfönster när
VS Code startar, och installationen körs där — läsbar, avbrytbar och utan att
blockera något. Två tasks med samma `presentation.group` hamnar sida vid sida.

Sätt `"task.allowAutomaticTasks": "on"` i code-servers användarinställningar
(`~/.local/share/code-server/User/settings.json`) så slipper användaren en fråga
första gången.

Se `verktyg/onyxia-init.sh` och `verktyg/labb-start.sh`.

Relaterat: [[onyxia-behorigheter-satts-vid-start]], [[installera-i-hemkatalogen-inte-med-apt]]
