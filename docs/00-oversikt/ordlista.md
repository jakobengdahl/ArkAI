# Ordlista

Termer vi använder i repot, förklarade som de betyder *här*. Många av dem används
slarvigt i branschen; poängen med listan är att vi ska mena samma sak.

Vi behåller engelska termer som är etablerade. Att översätta *prompt* till
"instruktionstext" hjälper ingen som ska läsa dokumentationen till ett verktyg.

---

### Agent
En LLM som får köra verktyg i en loop tills en uppgift är klar, i stället för att
svara en gång. Skillnaden mot en chattbot är inte modellen — det är att agenten själv
bestämmer nästa steg och kan göra saker: läsa filer, köra kommandon, anropa API:er.

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

### Grafminne
Minne lagrat som noder och relationer i stället för som textstycken. Låter oss ställa
frågor som "vad hänger ihop med det här?" — vilket vektorsökning är dålig på.
Se [20-tekniker/grafminne.md](../20-tekniker/grafminne.md).

### Hallucination
Modellen producerar något som låter rimligt men inte stämmer. Minskar med bra kontext,
försvinner inte. Måste hanteras i arbetsflödet, inte bara i prompten.

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

### Skill
Ett paket med instruktioner (och ofta hjälpfiler eller skript) som ett AI-verktyg
laddar in när uppgiften kräver det. Skillnaden mot en lång systemprompt är att skills
laddas selektivt — de kostar ingen kontext förrän de behövs.
Se [20-tekniker/skills.md](../20-tekniker/skills.md).

### Subagent
En agent som en annan agent startar för en avgränsad deluppgift, med egen kontext.
Används för att hålla huvudagentens kontext ren eller för att jobba parallellt.

### Token
Modellens textenhet, ungefär ett halvt ord på svenska. Priser och gränser räknas i
tokens. Svenska text kräver fler tokens än engelsk för samma innehåll.

### Verktyg (tool)
En funktion modellen kan anropa: söka, läsa, skriva, beräkna, anropa ett API. Det som
gör skillnaden mellan att en modell *berättar* hur något görs och att den *gör* det.

### Vektordatabas
Databas för embeddings, optimerad för "hitta det som liknar det här". Qdrant, Milvus,
`pgvector`. Kan startas från Onyxias katalog.
