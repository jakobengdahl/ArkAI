---
namn: sspcloud-llm-inferens
beskrivning: SSP Cloud kör egen LLM-inferens på llm.lab.sspcloud.fr med OpenAI-kompatibelt API — hämta personlig nyckel i Open WebUI:s kontoinställningar.
typ: verktyg
uppdaterad: 2026-08-28
---

Plattformen tillhandahåller LLM-inferens med öppna modeller på
<https://llm.lab.sspcloud.fr>. Gränssnittet är Open WebUI, och API:et är därmed
OpenAI-kompatibelt med bas-URL `https://llm.lab.sspcloud.fr/api`.

Du hämtar en personlig API-nyckel i gränssnittet under **Settings → Account →
API keys**. Nyckeln fungerar både inifrån labbmiljön och externt.

**Varför:** det är lätt att anta att man måste ta in en extern leverantör för att
kunna experimentera med riktiga modellanrop. Det behövs inte, och att köra mot
plattformens inferens tar bort en hel del frågor kring vad som får skickas vart.

**Så använder du det:** peka vad som helst OpenAI-kompatibelt mot den — din egen
Open WebUI, ett Python-skript, en agent. Lista modellerna innan du hårdkodar ett
namn, utbudet ändras:

```bash
curl -s https://llm.lab.sspcloud.fr/api/models \
  -H "Authorization: Bearer $SSPCLOUD_LLM_API_KEY" | jq -r '.data[].id'
```

Utbudet omfattar **både chatt- och embeddingmodeller**: `/embeddings` svarar med
vektorer för den modell vars namn innehåller `embedding`. Det betyder att hämtning
mot eget material — RAG — går att köra helt på plattformen, utan extern leverantör.
Verifierat 2026-08-28 med 4096 dimensioner, både direkt och genom Eneo.

Se [docs/60-miljo/sspcloud-llm.md](../../docs/60-miljo/sspcloud-llm.md).

Relaterat: [[api-nycklar-i-hemkatalogen]], [[onyxia-behorigheter-satts-vid-start]]
