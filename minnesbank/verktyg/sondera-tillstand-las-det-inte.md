---
namn: sondera-tillstand-las-det-inte
beskrivning: Statusfiler ljuger efter en poddomstart — sondera lås, port och hälsokontroll varje gång i stället för att lita på det som skrevs sist.
typ: verktyg
uppdaterad: 2026-08-13
---

Vad som är installerat och vad som kör ska **sonderas vid varje avläsning**, inte
läsas ur en statusfil. En podd startas om ofta i den här miljön: processerna dör
medan filerna ligger kvar, och en statusfil som säger "kör" blir då fel utan att
någon skrivit fel.

**Varför:** labbpanelen visade först status ur `~/work/.labb/status/*.json`. Efter
en omstart påstod den att Open WebUI körde, och "öppna"-knappen ledde till ett
fel som var svårare att förstå än frånvaron av knapp. Ordningen som fungerar:
håller någon låset (`flock -n`) → *arbetar*; svarar hälsokontrollen eller porten →
*kör*; lyckas `finns`-kommandot → *installerad*; annars *saknas*.

**Så använder du det:** `labb.status()` i `verktyg/labb.py`. Statusfilen finns
kvar men används bara till exitkod och loggsökväg. Låset är också det som gör att
en installation startad i terminalen låser knappen i panelen — samma lås, samma
väg in via `verktyg/kor.sh`.

Relaterat: [[startskript-far-inte-blockera]]
