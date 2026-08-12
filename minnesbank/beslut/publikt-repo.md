---
namn: publikt-repo
beskrivning: ArkAI är medvetet publikt — vi publicerar mönster och lärdomar, aldrig verksamhetens detaljer.
typ: beslut
uppdaterad: 2026-08-12
---

Repot ligger öppet på GitHub. Det är ett val, inte en slarvighet: ett öppet repo går
att dela med kollegor, andra myndigheter och leverantörer utan behörighetskrångel,
och det tvingar oss att formulera lärdomarna generellt — vilket gör dem mer användbara
även för oss själva.

Priset är att gränsen måste hållas hårt. Vi skriver om **mönster**: "ett register med
kvartalsvis uppdatering", inte namnet. Inga personer, inga system, inga riktiga data,
inga nycklar.

**Varför:** frågan kommer att komma upp vid varje nytt användningsfall. Det är
billigare att ha svarat på den en gång.

**Så använder du det:** läs [RIKTLINJER-INNEHALL.md](../../RIKTLINJER-INNEHALL.md)
innan du skriver första gången. Kör `./verktyg/kontrollera-innehall.sh` innan du
pushar. Behöver du skriva ner interna detaljer under arbetets gång — lägg dem i
`lokalt/`, som är gitignorerad, och lyft bara ut den generella slutsatsen.

Testet: skulle texten vara begriplig och användbar för en arkitekt på en helt annan
organisation? Om nej — den är fel formulerad, inte fel att publicera.

Relaterat: [[onyxia-token-i-remote-url]], [[dokumentera-negativa-resultat]]
