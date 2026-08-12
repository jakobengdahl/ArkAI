# RAG och vektorsökning

Retrieval-Augmented Generation: sök fram relevanta textstycken ur en samling och lägg
dem i kontexten innan modellen svarar.

## Vad det löser

Modellen kan inte veta vad som står i våra dokument. Att klistra in allt går inte —
kontexten räcker inte till, och även om den gjorde det blir svaren sämre av att
dränkas i irrelevant text.

RAG hämtar de stycken som är relevanta för just den här frågan.

## Hur det fungerar

1. **Dela upp** dokumenten i stycken
2. **Bädda in** varje stycke som en vektor
3. **Lagra** vektorerna i ett index (Qdrant, Milvus, `pgvector` — alla finns i
   Onyxias katalog)
4. Vid en fråga: **bädda in frågan**, hämta de närmaste styckena, lägg i kontexten

Kvaliteten avgörs nästan helt av steg 1 och 4, som båda ser ut som
implementationsdetaljer:

**Uppdelningen.** Stycken som skär mitt i ett resonemang ger obrukbara träffar.
Stycken som är för stora dränker det relevanta. Det finns inget generellt rätt svar —
det beror på dokumenten.

**Sökningen.** Ren vektorsökning missar exakta termer — beteckningar, koder, namn.
Hybridsökning (vektor + lexikal) är nästan alltid bättre. Att lägga till en
omrankning ovanpå är ofta den enskilt största kvalitetshöjningen, och görs sällan.

## När det passar

- "Vad står det om X i våra dokument?"
- Stora dokumentsamlingar som ändras oberoende av oss
- Regelverk, handböcker, tidigare utredningar
- När källhänvisning är ett krav — RAG kan visa var svaret kom ifrån

Det sista är viktigare än det låter. Ett svar med en hänvisning går att kontrollera.
Ett svar utan går att tro på.

## När det inte passar

- **"Vad brukar vi göra?"** Det står inte i dokumenten. Det är
  [minnesbankens](minnesbank.md) område.
- **"Vad hänger ihop med det här?"** Likhet är inte samma sak som samband. Se
  [grafminne.md](grafminne.md).
- **Frågor som kräver att hela samlingen vägs samman.** "Hur många av våra
  beskrivningar nämner X?" är en databasfråga, inte en RAG-fråga. RAG hämtar de fem
  mest lika styckena — den räknar inte.
- **Små samlingar.** Under några hundra sidor: lägg in allt i kontexten och strunta i
  indexet.
- **Föränderligt innehåll utan reindexering.** Ett inaktuellt index svarar
  självsäkert fel.

## Vad det kostar

Uppsättningen är en eftermiddag. Att få den *bra* är veckor — och det arbetet är
nästan uteslutande utvärdering: bygga en uppsättning frågor med kända svar och mäta
om ändringar hjälper.

Utan den utvärderingen fastnar man i att skruva på inställningar utifrån känsla.
Det är det vanligaste sättet att lägga mycket tid på en RAG-lösning utan att göra den
bättre.

Löpande: indexet ska hållas färskt, embeddingmodellen ska inte bytas utan
omindexering, och tjänsten ska förvaltas.

## Testa i labbet

Enklaste vägen: ladda upp dokument i [Open WebUI](../60-miljo/openwebui.md), som har
RAG inbyggt. Det räcker för att känna på styrkorna och svagheterna.

Nästa steg är eget index i Qdrant från Onyxias katalog, där uppdelning och sökning
kan styras. Gör inte det steget förrän du har frågor att mäta mot.

## Vad vi har provat

| Experiment | Vad vi lärde oss |
|---|---|
| — | *(inget än)* |

## Vad vi ännu inte vet

- Hur bra fungerar embeddingmodellerna på svenska facktext? Det mesta är utvärderat
  på engelska.
- Klarar de vår terminologi, eller behövs anpassning?
- Hur ser en rimlig utvärderingsuppsättning ut för våra dokument — och vem tar fram
  de kända svaren?
- När är hybridsökning värd komplexiteten?

## Vidare läsning

- [minnesbank.md](minnesbank.md) — skillnaden mot RAG
- [grafminne.md](grafminne.md)
