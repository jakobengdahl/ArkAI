# Agentupplägg

En agent är en LLM som får köra verktyg i en loop tills en uppgift är klar. Men
"agent" i praktiken är alltid ett **upplägg**: modellen plus en körmiljö som avgör
vad den kan göra, vad den minns, vem som når den och vad som händer när den har fel.

Modellen är sällan det som avgör om upplägget blir användbart. Det är det vi vill
kunna visa — och det syns tydligast om man kör flera olika upplägg mot samma uppgift.

## Vad som skiljer upplägg åt

Kolumnerna att jämföra efter — och samtidigt de frågor som avgör om något kan gå
mot produktion:

| Dimension | Varför det spelar roll |
|---|---|
| **Var den körs** | Din terminal, en server, någon annans moln. Avgör vad den får se. |
| **Hur du når den** | Terminal, editor, chattapp, webbgränssnitt, schemalagt. Avgör hur den används i praktiken. |
| **Vad den minns** | Inget mellan sessioner, en fil, en databas, en delad minnesbank. |
| **Vilka verktyg den har** | Skal, filsystem, MCP-servrar, API:er. Avgör vad den kan göra fel. |
| **Vem som godkänner** | Frågar den innan den agerar, eller kör den på? |
| **Modellberoende** | Låst till en leverantör, eller pekbar mot vilken OpenAI-kompatibel endpoint som helst? |

Den sista är särskilt relevant här: vi har
[plattformens egen inferens](../60-miljo/sspcloud-llm.md) att peka mot.

## Upplägg vi vill prova

Listan är avsiktligt bred. Poängen är inte att välja en vinnare utan att förstå vad
de olika ansatserna optimerar för.

### Redan i miljön

**opencode** och **Continue** är förinstallerade i Onyxias image och konfigureras
automatiskt om du slår på AI-assistenten vid start. Continue kommer dessutom med en
MCP-server. Se [../60-miljo/ai-verktyg-i-imagen.md](../60-miljo/ai-verktyg-i-imagen.md).

Börja här. Det är gratis att prova och ger en referenspunkt för resten.

### Hermes

[Hermes Agent](https://github.com/NousResearch) från Nous Research (MIT-licens,
släppt februari 2026) är ett självhostat agent-runtime med **persistent minne** och
självbyggda skills som uttalad huvudpoäng — agenten ska bli mer kapabel ju längre den
kör. Den stödjer många modellleverantörer, inklusive OpenAI-kompatibla endpoints.

Varför den är intressant för oss: minnet är själva produkten, inte en påbyggnad. Det
gör den till den bästa jämförelsepunkten vi har för vår egen
[minnesbank](minnesbank.md) — vad vinner man på ett automatiskt växande minne, och
vad förlorar man i granskningsbarhet?

**Frågan att besvara:** vad hamnar i minnet när ingen kurerar det, och håller det
över tid?

### OpenClaw

[OpenClaw](https://docs.openclaw.ai/) (ursprungligen Clawdbot, av Peter Steinberger,
omdöpt januari 2026) är en självhostad gateway som kopplar chattappar — Slack,
Teams, Telegram, Discord, Signal, Matrix med flera — till agenter som kan köra
kommandon, läsa filer och anropa verktyg.

Varför den är intressant för oss: den flyttar agenten dit folk redan är. Det är en
helt annan distributionsmodell än "ett verktyg man öppnar", och den gör frågorna om
behörigheter och godkännande väldigt konkreta — en agent i en gruppchatt agerar
inför publik.

**Frågan att besvara:** vad ändras när agenten når en via samma kanal som kollegor
gör? Blir den mer använd, och blir det tydligt nog vem som ansvarar för vad den gör?

### Chattbot med verktyg

Open WebUI med verktyg inkopplade. Inte en agent i strikt mening — människan driver
dialogen — men den mest realistiska formen för de flesta av våra användningsfall.
Se [chattbot-plus-verktyg.md](chattbot-plus-verktyg.md).

### Kodagenter

Claude Code, opencode med flera, körda mot en riktig kodbas. Se
[kodagenter.md](kodagenter.md).

## Hur vi jämför dem rättvist

Kör **samma uppgift** genom flera upplägg och skriv ett experiment per upplägg.
Uppgiften ska komma från
[10-anvandningsfall/](../10-anvandningsfall/), inte vara påhittad för tillfället —
annars mäter vi hur bra verktygen är på demos.

Notera för varje:

- Vad krävdes för att komma igång? (minuter, inte "det var enkelt")
- Vad kunde den göra som de andra inte kunde?
- Var gick den fel, och hur märktes det?
- Hur mycket av resultatet berodde på modellen kontra på upplägget?
- Skulle en kollega kunna använda den utan din hjälp?

Den sista frågan är den som oftast avgör om något kan gå vidare, och den ställs
sällan i tid.

## Säkerhet innan du kör igång något

Agenter som kör kommandon i en miljö med dina uppgifter i miljövariablerna är en
konkret risk, inte en teoretisk. I den här miljön ligger git-token, S3-uppgifter,
`VAULT_TOKEN` och LLM-nycklar i `env` och i hemkatalogen — se
[minnesbanken](../../minnesbank/verktyg/api-nycklar-i-hemkatalogen.md).

Innan du startar ett nytt agentupplägg:

- Kör det i labbmiljön, inte mot något som betyder något
- Ge det inte bredare åtkomst än uppgiften kräver
- Ta reda på var det skickar data. En självhostad gateway är inte automatiskt
  självhostad inferens — modellanropen kan gå någon annanstans
- Läs vad det skriver ner om dig, och var

Det här är inte försiktighetsprosa: det är precis de frågor som måste besvaras för
att något ska kunna gå från labb till skarpt läge, och de är billigast att besvara nu.
