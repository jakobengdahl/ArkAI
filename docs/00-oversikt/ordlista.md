# Ordlista

Termer vi använder i repot, förklarade som de betyder *här*. Många av dem används
slarvigt i branschen; poängen med listan är att vi ska mena samma sak.

Vi behåller engelska termer som är etablerade. Att översätta *prompt* till
"instruktionstext" hjälper ingen som ska läsa dokumentationen till ett verktyg.

Några av termerna kommer från styrningen snarare än från tekniken. De står med för
att de behövs när ett förslag ska bedömas — se
[forutsattningar.md](forutsattningar.md).

---

### Agent
En LLM som får köra verktyg i en loop tills en uppgift är klar, i stället för att
svara en gång. Skillnaden mot en chattbot är inte modellen — det är att agenten själv
bestämmer nästa steg och kan göra saker: läsa filer, köra kommandon, anropa API:er.

Flera agenter som samarbetar, där en fördelar deluppgifter och väger ihop resultaten,
kallas ett multiagentupplägg. Ökar det man kan göra och det som kan gå fel i ungefär
samma takt.

### AI-system
I EU:s AI-förordning: ett maskinbaserat system som fungerar med varierande grad av
autonomi, kan uppvisa anpassningsförmåga efter införande, och som utifrån indata
härleder hur utdata — förutsägelser, innehåll, rekommendationer eller beslut — ska
genereras.

Definitionen är bred med avsikt. Den avgör vad som omfattas av regelverket, och den
träffar betydligt mer än det man till vardags kallar AI.

### Bred AI och smal AI
**Smal AI** är utformad och optimerad för en avgränsad uppgift — en modell tränad på
eget material för klassificering eller kodning. **Bred AI** fungerar i många
sammanhang; stora språkmodeller är det typiska exemplet.

Distinktionen används i svensk offentlig sektor och är användbar i riskbedömningar:
en smal, egentränad modell och en bred, inköpt modell ställer helt olika frågor om
insyn, data och kontroll. ("Bred AI" är inte samma sak som superintelligens — det
skiljer sig från hur *generell AI* ibland används i debatten.)

### Byggsten
En av de delar en AI-lösning består av: modell, applikationslager, verktyg, kontext,
utvärdering, översyn, drift. Modellen är en av dem, och sällan den som avgör om
lösningen blir användbar.
Se [20-tekniker/byggstenar.md](../20-tekniker/byggstenar.md).

### Chattbot
Gränssnitt där en människa ställer frågor och får svar. Kan ha verktyg, men människan
driver dialogen framåt. En agent driver sig själv.

### Context / kontextfönster
Allt modellen "ser" när den svarar: systemprompt, historik, uppladdade dokument,
verktygsresultat. Ändligt. Det mesta som går fel i praktiken handlar om att fel saker
hamnar i kontexten, eller att rätt saker inte gör det.

### Context engineering
Arbetet med att få rätt information in i kontexten vid rätt tillfälle. Har till stor
del ersatt "prompt engineering" som det som faktiskt avgör kvaliteten.

### Embedding
En text omvandlad till en vektor av tal, så att texter som betyder ungefär samma sak
hamnar nära varandra. Grunden för semantisk sökning.

### Finjustering (fine-tuning)
Att träna vidare på en färdig modell med eget material så att den blir bättre på en
viss sorts uppgift. Realistiskt för små och medelstora modeller; för de största sker
anpassningen i praktiken genom kontext i stället, eftersom omträning inte är
görbar. Lättviktiga varianter som LoRA sänker tröskeln men tar inte bort den.

### Grafminne
Minne lagrat som noder och relationer i stället för som textstycken. Låter oss ställa
frågor som "vad hänger ihop med det här?" — vilket vektorsökning är dålig på.
Se [20-tekniker/grafminne.md](../20-tekniker/grafminne.md).

### Grundmodell, open-weight
En **grundmodell** är en stor modell tränad på mycket material, avsedd att användas
som bas för många olika tillämpningar.

**Open-weight** betyder att vikterna är tillgängliga — inte att modellen är
open-source. Träningsdata och träningsprocess är oftast fortfarande stängda. Det är
en viktig skillnad när insyn är ett krav: en öppen modell ger sällan samma insyn i
processen som en smal modell tränad på eget, dokumenterat material.

### Hallucination
Modellen producerar något som låter rimligt men inte stämmer. Minskar med bra kontext,
försvinner inte. Måste hanteras i arbetsflödet, inte bara i prompten.

### Human-in-the-loop, mänsklig översyn
Var människan sitter i förhållande till systemet. Tre lägen som är värda att hålla
isär, för de ställer olika krav:

- **in-the-loop** — människan granskar eller godkänner innan resultatet går vidare
- **on-the-loop** — människan övervakar och kan ingripa när något avviker
- **over-the-loop** — styrning på en högre nivå: vem som ansvarar för användningen
  som helhet

Nivån är en konstruktionsfråga per användningsfall, inte ett generellt läge. Att ta
bort människan ur kritiska steg ökar risken för automationsbias — att förslag godkänns
allt mer okritiskt ju oftare de visat sig rätt.

### Informationsklassning
Bedömningen av hur känslig en viss information är, som styr var och hur den får
behandlas. Avgör i praktiken vilken miljö och vilken tjänst som får användas — ofta
innan tekniska frågor blir relevanta.
Se [forutsattningar.md](forutsattningar.md).

### LLM
Large Language Model. Själva modellen. En LLM är inte en produkt — det som gör den
användbar är allt runtomkring.

### MCP (Model Context Protocol)
Ett öppet protokoll för att koppla verktyg och datakällor till AI-appar. En MCP-server
exponerar funktioner; en MCP-klient (Claude Code, Open WebUI, en egen app) kan anropa
dem. Poängen är standardisering: skriv verktyget en gång, använd det från flera
klienter. Se [20-tekniker/mcp.md](../20-tekniker/mcp.md).

### Minnesbank
Strukturerad, beständig kunskap som läggs in i kontexten i kommande sessioner.
Skiljer sig från RAG genom att innehållet är *skrivet för att läsas av en modell* och
kurerat, inte bara indexerade dokument.
Se [20-tekniker/minnesbank.md](../20-tekniker/minnesbank.md).

### ML-Ops
Arbetssätt och teknik för att hantera modellers livscykel: data, träning,
driftsättning, övervakning, omträning. Etablerat inom maskininlärning. Något
motsvarande, lika välavgränsat, finns ännu inte för statistikproduktion som helhet —
men mycket av tänkesättet går att låna, och delar av det (versionshantering,
dokumentation, kvalitetskontroller) känns igen från arbetssätt som redan finns.

För generativ AI räcker det inte att versionshantera modellen. Prompter, hämtnings-
index, verktyg och konfiguration påverkar utfallet lika mycket.

### Orkestrering
Lagret som håller ihop flera steg: vilken prompt, vilket verktyg, i vilken ordning,
vad som förs vidare till nästa steg. Det som gör skillnad mellan ett anrop och ett
arbetsflöde — och det som gör flerstegslösningar möjliga att felsöka.

### PoC / pilot / produktion
- **PoC** — visar att något är möjligt. Får gå sönder. Ingen användare.
- **Pilot** — riktiga användare, avgränsat, med uttalat slutdatum och ägare.
- **Produktion** — någon förlitar sig på det. Förvaltning, support, drift, budget.

Se [00-oversikt/mognadstrappa.md](mognadstrappa.md).

### Prompt
Instruktionen till modellen. Systemprompt = de stående instruktionerna;
användarprompt = det som ställs just nu.

### RAG (Retrieval-Augmented Generation)
Sök fram relevanta textstycken ur en samling och lägg dem i kontexten innan modellen
svarar. Bra för "vad står det om X i våra dokument". Sämre för "vad brukar vi göra i
sådana här lägen" — det är minnesbankens område.

### Risknivå
AI-förordningens indelning: oacceptabel, hög, begränsad, minimal risk. Bedömningen
görs utifrån hur systemet **används**, inte bara hur det är byggt — samma teknik kan
hamna på olika nivåer i olika sammanhang.
Se [forutsattningar.md](forutsattningar.md).

### Skill
Ett paket med instruktioner (och ofta hjälpfiler eller skript) som ett AI-verktyg
laddar in när uppgiften kräver det. Skillnaden mot en lång systemprompt är att skills
laddas selektivt — de kostar ingen kontext förrän de behövs.
Se [20-tekniker/skills.md](../20-tekniker/skills.md).

### Skyddsräcke (guardrail)
Kontroll som begränsar vad som får gå in i eller ut ur en modell: filtrering av
känsliga indata, kontroll av utdata, avgränsning av vilka verktyg som får anropas.
Ett skyddsräcke är en komponent, inte en instruktion i prompten.

### Spårbarhet och reproducerbarhet
**Spårbarhet** är att kunna svara på "vad hände i det här enskilda fallet?" i
efterhand. **Reproducerbarhet** är att kunna få samma resultat igen.

Med generativ AI räcker det inte att spara modellversionen. Utfallet beror på
kombinationen av modell, prompt, hämtad kontext, verktyg och efterbehandling — och
på när och hur en människa gick in. Ju mer sammansatt lösningen är, desto tidigare
måste spårbarheten byggas in. Den går inte att lägga till i efterhand, och det är
alltid i efterhand frågan kommer.

### Subagent
En agent som en annan agent startar för en avgränsad deluppgift, med egen kontext.
Används för att hålla huvudagentens kontext ren eller för att jobba parallellt.

### Token
Modellens textenhet, ungefär ett halvt ord på svenska. Priser och gränser räknas i
tokens. Svenska text kräver fler tokens än engelsk för samma innehåll.

### Typfall
Vilket slags AI-användning något är — var i verksamheten den sitter och vilken sorts
lösning det rör sig om. Säger mer om vad som krävs i utvärdering, översyn och
styrning än beskrivningen av uppgiften gör.
Se [10-anvandningsfall/typfall.md](../10-anvandningsfall/typfall.md).

### Utvärderingsuppsättning (eval)
En samling fall med kända eller bedömda svar som en lösning mäts mot. Utan en sådan
går det inte att veta om en ändring hjälpte, och man hamnar i att skruva på
inställningar utifrån känsla.

För uppgifter utan facit får utvärderingen konstrueras: scenarier, robusthetstest,
känslighetsanalys för prompt och kontext, strukturerad expertgranskning. Det är
arbete, och det underskattas nästan alltid.

### Verktyg (tool)
En funktion modellen kan anropa: söka, läsa, skriva, beräkna, anropa ett API. Det som
gör skillnaden mellan att en modell *berättar* hur något görs och att den *gör* det.

### Vektordatabas
Databas för embeddings, optimerad för "hitta det som liknar det här". Qdrant, Milvus,
`pgvector`. Kan startas från Onyxias katalog.
