---
namn: exponerad-port-kraver-inloggning
beskrivning: En exponerad port är ett publikt värdnamn — och Open WebUI slår bara på inloggning för värdet True, inget annat.
typ: verktyg
uppdaterad: 2026-08-13
---

Exponerar du en port i Onyxia ligger tjänsten på ett publikt värdnamn, inte bara
nåbar för dig. Open WebUI läser dessutom `WEBUI_AUTH` som sann **bara när strängen
är `true`** — `1`, `yes` och tomma värden stänger av inloggningen trots att de ser
påslagna ut. En chatt utan inloggning är kopplad till din API-nyckel.

**Varför:** när Open WebUI byttes till `--host 0.0.0.0` för att ingressen skulle
fungera blev standardläget en oskyddad chatt på ett publikt värdnamn, och enda
skyddet var en mening i dokumentationen om att sätta `WEBUI_AUTH=True` i en `.env`
som inte finns i en färsk miljö. Rättningen — att slå på inloggning automatiskt —
gick i sin tur att gå förbi med ett värde som `1`.

**Så använder du det:** `verktyg/starta-openwebui.sh` sonderar ingressen för porten
och vägrar starta på annat än `True` i det läget (`TILLAT_OSKYDDAD=ja` överstyr
medvetet). Startar du något **annat** som lyssnar på en exponerad port: kontrollera
autentiseringen först, och kontrollera hur den tjänsten tolkar sitt eget
inställningsvärde — tumregeln är att bara den exakta strängen leverantören
dokumenterar räknas.

Relaterat: [[spa-fungerar-inte-bakom-sokvagsproxy]], [[api-nycklar-i-hemkatalogen]],
[[sondera-tillstand-las-det-inte]]
