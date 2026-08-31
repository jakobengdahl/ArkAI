# Labbpanelen

Panelen är repots dokumentation renderad, plus knappar för det som går att köra.
Den finns för att man inte ska behöva kunna VS Code, terminalen och Onyxia för att
komma igång — men den tar inte bort något av det. Allt panelen gör går att göra
från terminalen, med samma kommandon.

Öppna den i VS Code:

```
Ctrl+Shift+P → "Simple Browser: Show" → klistra in panelens URL
```

URL:en skrivs ut när panelen startar. Den ser ut som
`https://<din-vscode-url>/proxy/8082/`.

## Två regler som förklarar allt annat

**Markdown är master.** Panelen har inget eget innehåll. Den renderar `.md`-filerna
som ligger i repot, och samma filer går att läsa på GitHub. Hittar du ett fel i
panelen rättar du filen, inte panelen.

**Inga absoluta sökvägar.** All navigering sker via query-strängen (`?sida=…`) och
all CSS ligger inline i sidan. Det är därför panelen fungerar oförändrad både på
`127.0.0.1:8082` och bakom code-servers `/proxy/8082/` — till skillnad från
Open WebUI, som antar att den ligger i roten av ett värdnamn och därför kräver en
egen ingress. Se
[minnesbanken](../../minnesbank/verktyg/spa-fungerar-inte-bakom-sokvagsproxy.md).

Konsekvensen är praktisk: panelen behöver ingen portexponering och inget omstart av
tjänsten. Den binder till `127.0.0.1` och kan bara nås av den som har den här
VS Code-sessionen — vilket är hela behörighetsmodellen för något som kan starta
processer.

## Vad du kan göra i den

| I panelen | I terminalen |
|---|---|
| Läsa dokumentationen med navigering | `less docs/…` |
| Se vad som är installerat och vad som kör | `verktyg/kor.sh status` |
| Installera och starta en tjänst | `verktyg/kor.sh installera eneo` |
| Koppla in en tjänst i Eneo | `verktyg/kor.sh koppla_eneo metadatagraf` |
| Köra igång en hel uppsättning | `verktyg/kor.sh uppsattning eneo-plattform` |
| **Ta bort en tjänst ur namnrymden** | `verktyg/kor.sh avinstallera eneo` |
| Följa en installationslogg | `tail -f ~/work/.labb/logg/*.log` |
| Se vad som kör i namnrymden och vad det kostar | `python3 verktyg/labb.py namnrymd` |

Panelen anropar `verktyg/kor.sh`. Det är samma väg som terminalen använder, vilket
är avsiktligt: en installation du startade i terminalen låser knappen i panelen,
och tvärtom.

## Knapparna vet vad som redan pågår

Panelen gissar aldrig ett tillstånd — den sonderar det, varje gång sidan laddas:

| Vad panelen tittar på | Vad den drar för slutsats |
|---|---|
| Håller någon låset i `~/work/.labb/las/`? | **arbetar** — knappen blir "visa vad som händer" |
| Svarar hälsokontrollen eller porten? | **kör** — knappen blir "öppna" och "stoppa" |
| Lyckas `finns`-kommandot i manifestet? | **installerad** — knappen blir "starta" |
| Annars | **ej installerad** — knappen blir "installera" |

*Koppla in i Eneo* dyker upp bara när två saker gäller samtidigt: tjänsten har
`koppla_eneo` i manifestet, och Eneo svarar. Kopplingen skriver mot Eneos API, så
utan Eneo uppe hade knappen bara producerat ett fel i en logg.

Därför spelar det ingen roll att en pod-omstart dödar alla processer men lämnar
kvar filerna: panelen påstår inte att något kör bara för att det gjorde det förut.

Låsen är av två slag, vilket är lätt att göra fel. `kor.sh` tar ett **exklusivt**
lås medan den arbetar; panelens avläsning tar ett **delat**. Två avläsningar stör
alltså inte varandra, medan en verklig körning syns för båda.

Ett delat lås utesluter ändå ett exklusivt under de mikrosekunder avläsningen
tar. Därför väntar `kor.sh` i två sekunder på låset i stället för att ge upp
direkt — annars kunde en sidladdning i olyckligt ögonblick få en installation
att svara "något körs redan".

## Vad panelen litar på

Manifestet är körbar kod. `finns`-kommandot körs varje gång en sida renderas, och
`installera`/`starta`/`stoppa` körs när du trycker på en knapp. Den som kan ändra
`verktyg/labb.toml` kan alltså köra kommandon i din miljö — och startskriptet
hämtar dessutom repots `main` direkt från GitHub.

Det är avsiktligt och ofrånkomligt för ett labb som ska kunna installera saker,
men det betyder att **`main` i det här repot är betrodd kod**. Granska ändringar i
`verktyg/` som om de gällde ett skript du kör som dig själv, för det är vad de är.
`.env` och annat som `.gitignore` täcker går däremot inte att läsa genom panelen.

## Lägga till en tjänst

Allt panelen vet står i [`verktyg/labb.toml`](../../verktyg/labb.toml). Lägg till
en tjänst där — inte i koden:

```toml
[tjanst.mittverktyg]
namn = "Mitt verktyg"
beskrivning = "En rad om vad det är bra för."
dok = "docs/20-tekniker/min-teknik.md"
typ = "lokal"            # lokal = process här, fjarr = kör någon annanstans,
                         # verktyg = stdio, startas av klienten
steg = "begaran"         # auto = installeras vid uppstart
port = 8085
finns = "command -v mittverktyg"
installera = "verktyg/installera/mittverktyg.sh"
starta = "verktyg/starta-mittverktyg.sh --bakgrund"
stoppa = "verktyg/starta-mittverktyg.sh --stoppa"
avinstallera = "verktyg/ta-bort-mittverktyg.sh"   # frivilligt, se nedan
koppla_eneo = "verktyg/koppla-mcp-till-eneo.py mittverktyg --skriv"  # frivilligt
halsa = "http://127.0.0.1:8085/health"

[tjanst.mittverktyg.byggstenar]
verktygslagret = { lage = "inbyggd", not = "En rad om vad just den här byggstenen blir här." }
sakerhet-och-behorighet = { lage = "saknas", not = "Och en ärlig rad om vad som inte finns." }
```

**Byggstenarna är det som gör korten jämförbara.** Ett verktyg beskriver sig alltid
med sitt eget produktspråk; `[tjanst.<id>.byggstenar]` översätter det till den
gemensamma kartan i [byggstenar.md](../20-tekniker/byggstenar.md), så att två
verktyg går att läsa på samma rader. Id:na kommer från `[[byggsten]]` högst upp i
manifestet, och lägena är:

| Läge | Betyder |
|---|---|
| `inbyggd` | ingår, och går inte att koppla bort |
| `konfig` | ingår, men måste ställas in innan den gör någon nytta |
| `tillval` | ingår inte från början, går att lägga till |
| `begransad` | finns delvis — läs noten innan du räknar med den |
| `saknas` | finns inte, och det är en känd lucka |

Skriv noten så att den säger något man inte redan gissar. "Ingen behörighetsmodell"
är en not; "säkerhet saknas" är en tom ruta.

En **uppsättning** är flera tjänster som ska fungera ihop. De körs bara från
terminalen — panelens ingång är verktyget och dess knappar:

```toml
[uppsattning.mitt-experiment]
namn = "Mitt experiment"
beskrivning = "Vad kombinationen är till för."
tjanster = ["eneo", "mittverktyg"]
dok = "docs/30-experiment/EXP-00N-mitt-experiment.md"
```

Uppsättningen installerar det som saknas, startar i ordning och kör sist
`koppla_eneo` för varje tjänst som har det — förutsatt att Eneo är med och svarar.

## Att ta något ur bruk

`avvecklas = true` gör att en tjänst inte längre installeras automatiskt och inte
visas bland verktygen. Skript, manifestrad och dokumentation ligger kvar, och
`verktyg/kor.sh starta <id>` fungerar som förut.

Det finns för att en tjänst ska kunna tas ur bruk *stegvis*. Att radera allt på en
gång slänger både verktyget och skälen till att det fanns; att låta det ligga kvar
med en startknapp lockar nästa person att gå tillbaka. Open WebUI är det första
fallet — se [openwebui.md](openwebui.md).

## Dynamiska block i markdown

Panelen expanderar HTML-kommentarer när den renderar. På GitHub syns de inte alls,
vilket är poängen — markdownfilen förblir läsbar på båda ställena.

| Block | Vad det blir |
|---|---|
| `<!-- panel:verktyg -->` | Kort per verktyg: status, byggstenar och knappar |
| `<!-- panel:status -->` | Tabell över det som kör |
| `<!-- panel:miljo -->` | Verktyg, namnrymd, hur tjänsten startades |
| `<!-- panel:namnrymd -->` | Ingresser i namnrymden, som klickbara adresser |
| `<!-- panel:kvot -->` | Arbetslaster och volymer i namnrymden, med kvotförbrukning |

## Att ta bort något

Att stoppa och att ta bort är två olika saker, och skillnaden syns i panelen.
*Stoppa* släpper processer och skalar arbetslaster till noll; data ligger kvar.
*Ta bort* raderar.

En tjänst får en **Ta bort**-knapp bara om den har `avinstallera` i manifestet.
Knappen kör aldrig något direkt — den leder till en bekräftelsesida som visar
`avinstallera_varning` och utdata från `avinstallera_visa`, alltså vad som
faktiskt försvinner. Först där finns knappen som gör det.

```toml
avinstallera = "verktyg/ta-bort-mittverktyg.sh"
avinstallera_varning = "Databasen raderas — det går inte att ångra."
avinstallera_visa = "kubectl get all,pvc -l app.kubernetes.io/part-of=mittverktyg"
```

Det här finns för att tjänster som deployas i namnrymden — Eneo är den första —
**fortsätter köra när VS Code-tjänsten stoppas**. Utan en väg att ta bort dem fylls
namnrymden av installationer vars miljö inte längre finns. Blocket
`<!-- panel:kvot -->` på startsidan visar vad man har igång och hur mycket av
kvoten det tar. Se
[minnesbanken](../../minnesbank/verktyg/namnrymden-overlever-podden.md).

## Koppla in i Eneo

Eneo har inga verktyg och ingen modell från början — allt läggs upp per
organisation. `koppla_eneo` i manifestet är kommandot som gör det, och panelen
lägger en knapp på kortet:

```toml
[tjanst.metadatagraf]
koppla_eneo = "verktyg/koppla-mcp-till-eneo.py metadatagraf --skriv"
```

Eneos eget kort har samma nyckel, men pekar på modellkopplingen och byter etikett
med `koppla_eneo_knapp = "Koppla in modellerna"`.

Kommandot går genom samma `kor.sh`, tar samma lås och skriver samma sorts logg som
tjänsternas övriga handlingar. Det ska gå att köra om: efter ett nyckelbyte, efter
att en server startats om, eller efter att Eneo installerats på nytt.

## Starta och stoppa panelen

```bash
verktyg/starta-panelen.sh --bakgrund
verktyg/starta-panelen.sh --stoppa
verktyg/starta-panelen.sh              # förgrunden, eller följ loggen om den redan kör
```

Normalt behöver du inte göra något av det — panelen startas av
[startskriptet](starta-labbet.md) när tjänsten startar.

## Var saker ligger

Allt panelen skriver hamnar i `~/work/.labb/`, utanför repot:

```
~/work/.labb/
  miljo.toml        hur tjänsten startades: profil, tidpunkt, namnrymd
  mcp.json          delad MCP-konfiguration, genererad ur labb.toml
  logg/             en logg per tjänst och handling
                    panel-kor.log = panelens egen, för fel som inträffar
                    innan kor.sh hunnit skriva tjänstens logg
  las/              låsfiler — det är dessa som gör knapparna säkra
  status/           anteckning om senaste körningen
```

Att det ligger utanför repot är medvetet: ingenting som skrivs där kan råka
commitas, och `git clean` tar inte bort din installationshistorik.
