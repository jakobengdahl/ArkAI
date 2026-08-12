# Beslutsguide: vilken teknik till vilket problem

Frågor att gå igenom när något nytt kommer upp. Ordningen är inte slumpmässig — de
tidiga frågorna avgör mer än de sena, och de hoppas oftast över.

Guiden ersätter inte att prova. Den ska förhindra att man provar fel sak i tre veckor.

## 1. Vad är svårigheten, egentligen?

Inte "vad är uppgiften" — vad gör den svår? Svaret styr allt som kommer sedan.

| Svårigheten är | Titta på |
|---|---|
| **Volym** — mycket av något enkelt | [Chattbot + verktyg](../20-tekniker/chattbot-plus-verktyg.md), agentupplägg |
| **Letande** — svaret finns men är svårt att hitta | [RAG](../20-tekniker/rag-och-vektor.md) |
| **Konsistens** — olika personer gör olika | [Skills](../20-tekniker/skills.md) |
| **Kunskapsöverföring** — sitter i huvudet på några | [Minnesbank](../20-tekniker/minnesbank.md) |
| **Samband** — "vad påverkas om vi ändrar X?" | [Grafminne](../20-tekniker/grafminne.md) |
| **Att göra, inte bara veta** | [MCP](../20-tekniker/mcp.md) + agent |
| **Att komma överens** | Ingen. Det är inte ett AI-problem. |

De flesta fall har flera svårigheter. Skriv ner dem alla, och var tydlig med vilken
du faktiskt adresserar — annars kommer resultatet att bedömas mot en förväntning du
inte lovat.

## 2. Kan den som gör jobbet bedöma svaret?

**Nej** → stanna. Det här är inte en teknikfråga än. Ett svar som inte kan bedömas
måste först göras granskningsbart — med källhänvisningar, med mellansteg som syns,
med möjlighet att kontrollera stickprov. Utan det flyttar vi arbete och lägger till
en risk.

**Ja, men det tar tid** → källhänvisning är ett krav, inte en förbättring.

**Ja, snabbt** → gå vidare.

Den här frågan sorterar bort fler idéer än någon annan, och den ställs nästan alltid
för sent.

## 3. Vad händer när svaret är fel?

| Konsekvens | Vad det innebär |
|---|---|
| Någon blir irriterad | Bra kandidat att börja med |
| Någon gör ett extra moment | Går bra, men mät hur ofta |
| Ett beslut blir fel | Krävs mänskligt godkännande i varje steg |
| Går ut till någon utanför | Inte i labbet. Gå via ordinarie ordning |

Börja med det som får gå fel. Det är inte en försiktighetsprincip — det är det som
gör att man vågar iterera snabbt nog för att lära sig något.

## 4. Var får underlaget behandlas?

Avgör om det överhuvudtaget går att prova, och var. I labbet:
[plattformens LLM-inferens](../60-miljo/sspcloud-llm.md) är utgångspunkten.

Vet du inte — ta reda på det innan du börjar, inte efter. Att behöva kasta ett
experiment för att materialet inte fick vara där är en dyr lärdom.

## 5. Finns det något att mäta mot?

Utan en uppsättning fall med kända svar går det inte att veta om en ändring hjälpte.
Man hamnar i att skruva på inställningar utifrån känsla, vilket är det vanligaste
sättet att lägga mycket tid utan att bli bättre.

Det behöver inte vara stort. Tio fall med kända svar är oändligt mer värt än noll.

Finns det inget: **börja där**. Att ta fram utvärderingsfallen är ofta det mest
värdefulla arbetet i hela ansatsen, och det är arbete som håller även om tekniken byts.

## 6. Vem äger det om det fungerar?

Ingen → det blir en PoC. Det är helt okej, men säg det högt från början.

Någon → skriv upp namnet i användningsfallet. Se
[mognadstrappan](../00-oversikt/mognadstrappa.md).

Den vanligaste orsaken till att en fungerande pilot blir liggande är inte teknisk —
det är att ingen ägde frågan om vad som skulle hända sedan.

## Genvägar som brukar hålla

Tumregler, inte sanningar. Pröva dem.

- **Börja alltid med chattbot + verktyg.** Enklare att gå från chattbot till agent än
  tvärtom, och man lär sig vad uppgiften faktiskt kräver.
- **Bygg inte grafen först.** Bygg textminnet, se var det tar slut, och låt gränsen
  visa vilka relationer som behövs.
- **Utvärderingsfallen före finjusteringen.** Alltid.
- **En teknik i taget.** Två samtidigt gör det omöjligt att veta vilken som hjälpte.
- **Om ett skript räcker, kör skriptet.** Determinism är en funktion, inte en
  begränsning.

## Efter beslutet

Skriv ett experiment. Även när svaret blev "vi provar inte" — och särskilt då, för
skälet är värt att kunna gå tillbaka till. Se
[30-experiment/](../30-experiment/).
