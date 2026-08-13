---
namn: installera-i-hemkatalogen-inte-med-apt
beskrivning: Node och gh finns som tarball och kan läggas i ~/.local — då överlever de poddomstarter och kräver ingen sudo, till skillnad från apt-installationer.
typ: verktyg
uppdaterad: 2026-08-13
---

Installera verktyg under `~/.local`, inte med `apt`. Både Node och GitHub CLI
distribueras som tarball och behöver varken paketkälla eller `sudo`:

```bash
curl -fsSL https://nodejs.org/dist/latest-v24.x/node-v*-linux-x64.tar.xz \
  | tar -xJ -C ~/.local/node --strip-components=1
```

**Varför:** `apt`-installationer ligger under `/usr` och försvinner varje gång
podden startas om, vilket gjorde "installera om verktygen" till ett återkommande
moment. `~/.local` ligger på den persistenta volymen. Efter bytet tar
grundinstallationen sekunder i stället för minuter vid andra uppstarten, och
skriptet behöver ingen `sudo` alls.

**Så använder du det:** `verktyg/installera/bas.sh`. Kör om det när du vill — det
hoppar över det som redan finns. Undantaget är `ss` och `lsof`, som bara finns via
apt; sondera portar med `bash -c "exec 3<>/dev/tcp/127.0.0.1/8081"` i stället.

Relaterat: [[startskript-far-inte-blockera]]
