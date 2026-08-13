# Karta: typfall × byggstenar

Vilka byggstenar olika slags AI-användning brukar kräva.

**Det här är hypoteser, inte resultat.** Kartan är byggd av resonemang och av vad
andra rapporterar — inte av våra egna experiment. Den finns för att kunna välja vad
som är värt att pröva, och för att kunna säga "det här trodde vi" när ett experiment
visar något annat.

Bekräftade rader hör hemma i [matris.md](matris.md), och bara där. Håll isär dem: en
karta som smygförvandlas till en resultattabell är sämre än ingen karta.

- Typfallen A–F: [../10-anvandningsfall/typfall.md](../10-anvandningsfall/typfall.md)
- Byggstenarna: [../20-tekniker/byggstenar.md](../20-tekniker/byggstenar.md)

## Kartan

**●** avgörande · **○** viktig · **·** sällan det som avgör

| Byggsten | A smal | B språkmodell | C generativt i prod. | D internt stöd | E externt |
|---|---|---|---|---|---|
| Modellval | ● egen, tolkbar | ● anpassad på egen text | ○ stor + smal i kombination | ○ kod- och skrivstöd | ● robusthet, kontroll |
| Applikations- och API-lager | ○ integration i kedjan | ○ | ○ både interaktivt och satsvis | ● där arbetet redan görs | ● autentisering, filtrering |
| Orkestrering | · | · | ● många steg att hålla ihop | ○ | ● |
| Kontext och minne | ○ kurerad träningsdata | ○ domänmaterial | ● hämtning mot metadata och dokumentation | ● egna riktlinjer och exempel | ○ endast validerade källor |
| Verktygslager | ○ anrop i pipeline | ○ | ● modellen måste kunna slå upp och räkna | ● utvecklingsmiljö, versionshantering | ○ hårt avgränsat |
| Utvärdering | ● facit finns, mät | ● facit finns, mät | ● flerskiktad, måste konstrueras | ○ nytta snarare än korrekthet | ● motståndstest |
| Mänsklig översyn | ○ stickprov | ○ stickprov | ● hög i början, avtar med tilliten | ○ granska det som används | ● eskaleringsvägar |
| Säkerhet och behörighet | ● mikrodata | ● känslig text | ● särskilt vid extern modell | ○ rollstyrd åtkomst | ● prompt injection |
| Driftmiljö | ○ nära befintliga system | ○ | ○ | ○ moln där materialet tillåter | ● hög kontroll |
| Livscykel och versionshantering | ● modell, data, kod | ● | ● modell, prompt, index, verktyg | ○ | ● snabb återställning |
| Agentupplägg | · senare, för omträning | · | ● naturlig passform | ○ kan växa dit | ○ komplext, hantera varsamt |

## Vad kartan säger, i klartext

**Utvärdering är den enda raden som är avgörande överallt.** Det är inte en
tillfällighet. Det som skiljer ett experiment från en åsikt är att det finns något
att mäta mot — och det är också den byggsten som oftast hoppas över, för den ger
ingen demo.

**A och B liknar varandra mer än de liknar C.** Steget från icke-generativ till
generativ är större än steget från smal till språkmodell. Antalet rörliga delar som
måste versionshanteras går från tre till bortåt sex, och facit försvinner.

**D är billigast att komma igång med och svårast att mäta.** Byggstenarna finns
redan — verktygen står i utvecklingsmiljön. Det som saknas är ett sätt att avgöra om
det faktiskt blev bättre. Det är därför D är rätt ställe att börja **och** ett
lömskt ställe att stanna: det går att hålla på länge utan att veta något.

**Kontext slår modell i C och D.** I båda fallen är den avgörande insatsen att göra
våra egna underlag — metadata, dokumentation, riktlinjer, exempel — användbara för
ett AI-stöd. Det arbetet är inte tekniskt, det är innehållsarbete, och det överlever
varje modellbyte. Det är den mest återanvändbara investering vi kan peka ut.

**Agentupplägg är sällan första steget.** Undantaget är C, där uppgifterna redan är
flerstegsuppgifter. Överallt annars är en agent ett sätt att göra tre problem till
ett — och man vet inte vilket av dem som gick sönder.

## Hur vi prövar kartan

Varje cell markerad **●** är en påstådd förutsättning, och därmed ett experiment som
går att formulera: *ta bort byggstenen och se om det slutar fungera*. Det är den
billigaste sortens prövning vi har, och den ger raka svar.

Konkret nästa steg som prövar flera celler samtidigt:

- Kör samma uppgift med och utan hämtning mot eget material (prövar "kontext slår
  modell" i D)
- Kör en flerstegsuppgift som chattbot respektive som agent (prövar raden
  agentupplägg)
- Kör en uppgift på en liten och en stor modell (prövar "modellval är sällan det
  som avgör" — och svarar samtidigt på en kostnads- och miljöfråga)

## Vad som skulle få oss att skriva om den

- Ett experiment där utvärdering visade sig gå att hoppa över utan att man tappade
  omdömet
- Ett fall i D där modellvalet visade sig avgöra mer än kontexten
- Att nivåstegen i [byggstenar.md](../20-tekniker/byggstenar.md) inte håller i
  verkliga samtal med verksamheten

Skriv om den när det händer. En karta som ingen ändrar är en karta ingen använder.
