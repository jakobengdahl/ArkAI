# Tekniker

En sida per AI-teknik. Syftet är att kunna prata om byggstenarna var för sig i
stället för om "AI" som en klump — och att ha någonstans att samla vad vi faktiskt
sett dem klara.

Varje sida ska svara på: **vad är det, när passar det, när passar det inte, vad
kostar det, och vad har vi själva sett?**

Använd [MALL-teknik.md](MALL-teknik.md) för nya sidor.

## Sidorna

| Teknik | Kort |
|---|---|
| [chattbot-plus-verktyg.md](chattbot-plus-verktyg.md) | Chattbot som kan göra saker, inte bara svara |
| [mcp.md](mcp.md) | Model Context Protocol — standarden för att koppla in verktyg |
| [agentupplagg.md](agentupplagg.md) | Hermes, OpenClaw m.fl. — vad som skiljer agentupplägg åt |
| [kodagenter.md](kodagenter.md) | AI-agenter för utveckling |
| [skills.md](skills.md) | Instruktionspaket som laddas när de behövs |
| [minnesbank.md](minnesbank.md) | Kurerat, delat långtidsminne |
| [rag-och-vektor.md](rag-och-vektor.md) | Sök fram relevanta stycken och lägg i kontexten |
| [grafminne.md](grafminne.md) | Minne som noder och relationer |

## Hur de hänger ihop

Det är lätt att läsa listan som åtta konkurrerande alternativ. De är det inte —
de sitter på olika nivåer:

**MCP** är rör. Det är hur ett verktyg kopplas in, inte vad verktyget gör. Nästan
allt annat på listan kan levereras via MCP.

**Chattbot, agent och kodagent** är körmiljöer. Samma modell, samma verktyg, olika
sätt att driva arbetet framåt och olika sätt att nå det.

**RAG, minnesbank och grafminne** är sätt att få rätt saker in i kontexten. De löser
olika problem och används ofta tillsammans:

- RAG svarar på *"vad står det om X i våra dokument?"*
- Minnesbanken svarar på *"vad brukar vi göra i sådana här lägen?"*
- Grafen svarar på *"vad hänger ihop med det här?"*

Att blanda ihop de tre är den vanligaste orsaken till att en lösning känns nästan
rätt men inte blir användbar.

**Skills** är hur man paketerar arbetssätt så att de laddas när de behövs i stället
för att ligga och ta plats hela tiden.

## Innan du skriver en ny sida

Kolla om tekniken redan finns i miljön. Flera av dem gör det — se
[../60-miljo/ai-verktyg-i-imagen.md](../60-miljo/ai-verktyg-i-imagen.md) och
[../60-miljo/sspcloud-llm.md](../60-miljo/sspcloud-llm.md). Det är billigare att
beskriva något man kört än något man läst om.
