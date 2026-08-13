# UF-005 · Systematisk metadatahantering med graf som ingång

**Typfall:** [D · Generativt stöd i interna processer](typfall.md), i gränsytan mot [C](typfall.md)
**Spår:** Utforskande
**Steg:** Skiss
**Ägare:** — (frågan ägs inte av oss; se nedan)
**Uppdaterad:** 2026-08-13

> **Utforskande spår, och ett exempel.** Vi är med och utformar principer, koncept
> och arbetssätt för mer systematisk data- och metadatahantering inom GPM, men vi
> arbetar inte i de system där metadata lagras och används. Fallet finns här för att
> vi ska bygga egen kunskap om vad AI-stöd kräver på det här området — resultatet är
> ett underlag, inte ett förslag. Se
> [de två spåren](../00-oversikt/vision-och-mal.md#två-spår).

## Vad det handlar om

För att data ska gå att återanvända, spåra och kvalitetssäkra behöver metadata vara
strukturerad, aktuell och sammanhängande. Vår roll är principerna och koncepten:
vilka begrepp som ska finnas, hur de hänger ihop, vad som ska registreras var. Andra
grupper äger systemen och det löpande arbetet i dem.

Det som gör området intressant för labbet är att metadata är **starkt strukturerad**.
Det är ett av få ställen där man faktiskt kan mäta vad en graf tillför jämfört med
vanlig textsökning, i stället för att gissa.

## Vad vi redan vet

Området utforskades i en sprint inom ett EU-projekt tillsammans med andra
statistikbyråer, och dokumentationen är öppen:

- [Stockholm sprint 2026](https://github.com/AIML4OS/WP12/tree/main/stockholm_sprint_2026)
  — upplägg och resultat
- [User stories och pilotdokumentation för metadatagrafen](https://github.com/AIML4OS/WP12_MetadataGraph/tree/stockholmsprint/docs/sprint_documentation)

Det betyder att vi inte börjar från noll, och att vi kan jämföra med hur andra
statistikbyråer resonerat om samma frågor. Instansen finns dessutom uppe i samma
namnrymd som labbet och har en MCP-server — se
[metadatagrafen](../60-miljo/metadatagrafen.md).

Det gör fallet ovanligt billigt att arbeta vidare med. Det gör det också viktigt att
läsa in sig först: det vore slöseri att pröva om det som redan är prövat.

## Vad som gör det svårt

- **Flera aspekter i ett.** Att svara på frågor om vad som finns är en sak; att
  upptäcka luckor och motsägelser är en annan; att föreslå eller göra uppdateringar
  är en tredje. De kräver olika mycket styrning och är förmodligen olika
  användningsfall.
- **Samband, inte likhet.** "Vad påverkas om den här variabeln ändras?" är en
  grafråga. Vektorsökning svarar med det som *liknar*, vilket är fel svar.
- **Aktualitet.** Metadata som inte speglar verkligheten är sämre än ingen metadata,
  och avvikelsen upptäcks sällan av sig själv.
- **Gränsdragningen.** Vi utformar principer; andra arbetar i systemen. Ett stöd som
  gör något åt metadata rör deras arbete, inte vårt.

## Vad vi vill ta reda på

Formulerat som frågor vi kan besvara i labbet, inte som en lösning:

- Vad tillför en graf jämfört med hämtning över samma innehåll som text? Det här är
  det bästa tillfället vi har att mäta det.
- Klarar en agent att välja rätt källa när den har både grafen (domänminne) och
  [minnesbanken](../20-tekniker/minnesbank.md) (processminne)? Går det inte är det ett
  resultat värt att skriva ner.
- Vad kostar det att fråga? Grafen svarar med noder, inte med text — jämför
  tokenåtgången med att lägga motsvarande underlag i kontexten.
- Var går den praktiska gränsen mellan att *upptäcka* avvikelser och att *rätta* dem?
  Det är gränsen mellan nivå 3 och 4, och den är en mandatfråga snarare än en teknisk.

## Hur vi ser att det blev bra

Vi mäter inte verksamhetsnytta här — vi har ingen verksamhet att mäta på:

- Vi kan svara på graf kontra text med mätning bakom oss, inte med resonemang
- Vi kan beskriva vad ett stöd på nivå 3 skulle kräva av styrning och behörigheter
- Vi har något som går att lägga fram för dem som äger metadataarbetet, formulerat
  som observationer
- Vi kan relatera våra resultat till det som redan gjorts i sprinten, i stället för
  att upprepa det

## Underlaget

| | |
|---|---|
| Format | strukturerad metadata: begrepp, register, variabler och relationer |
| Ungefärlig mängd | pilotinstansens innehåll |
| Hur ofta det ändras | löpande i takt med verksamheten |
| Känslighet | innehållet i piloten är inte känsligt, men instansen ligger bakom inloggning och har en inbyggd AI-assistent kopplad till plattformens LLM-API |

Uppgifter till instansen kommer ur miljöns hemlighetshantering, aldrig ur repot.

## Vem bedömer svaret

Vi kan bedöma om ett svar om struktur och samband är rimligt. Vi kan **inte** bedöma
om innehållet speglar verksamhetens faktiska läge — det kan bara de som arbetar i
systemen. Det är en av anledningarna till att fallet ligger i det utforskande spåret.

## Vad som skulle behövas

- Inläsning av den öppna sprintdokumentationen innan något körs
- Åtkomst till pilotinstansens MCP-server, som redan finns i miljön
- Ett antal frågor med kända svar — inklusive några som text uppenbart inte klarar
- Kontakt med dem som äger metadataarbetet innan något visas upp

## Möjliga tekniker

| Teknik | Varför den skulle kunna passa | Provat? |
|---|---|---|
| [Grafminne](../20-tekniker/grafminne.md) | Samband är själva frågan här | — |
| [MCP](../20-tekniker/mcp.md) | Grafen exponerar redan verktyg — inget behöver byggas för att komma åt den | — |
| [RAG](../20-tekniker/rag-och-vektor.md) | Jämförelsepunkten. Utan den vet vi inte vad grafen tillför | — |
| [Agentupplägg](../20-tekniker/agentupplagg.md) | Flerstegsfrågor: hämta, jämföra, sammanställa | — |

## Öppna frågor

- Är det här ett användningsfall eller tre? Misstanken är tre, och att de bör delas
  innan något provas.
- Hur mycket av nyttan kräver att grafen är komplett? Ett ofullständigt domänminne
  som svarar självsäkert är en risk, inte ett stöd.
- Vad av det vi skulle vilja pröva är redan prövat i sprinten?
