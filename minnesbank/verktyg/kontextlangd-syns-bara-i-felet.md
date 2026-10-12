---
namn: kontextlangd-syns-bara-i-felet
beskrivning: Plattformens /models säger inget om kontextfönstret — fråga efter för många tokens så står gränsen i felmeddelandet.
typ: verktyg
uppdaterad: 2026-10-12
---

SSP Clouds modellista (`/api/models`) anger inte hur långt kontextfönster en modell
har. Bakom den sitter LiteLLM och vLLM, och de avvisar en fråga med för hög
`max_tokens` med gränsen i klartext: `max_tokens=… cannot be greater than
max_model_len=131072`. För embedding blir det `maximum context length is 40960
tokens` om indata är för lång. Gränsen gäller in- och utdata **tillsammans**.

**Varför:** Eneo registrerades med fasta 32768 in / 4096 ut för alla modeller,
"medvetet försiktigt" eftersom listan inte sa något. De faktiska gränserna
2026-10-12 var 131072 (gemma4-26b-moe, qwen3-6-35b-moe), 196608 (qwen3-8-27b)
och 40960 (qwen3-embedding-8b). Eneo trunkerade alltså till en fjärdedel av vad
modellerna klarar.

**Så använder du det:** gissa inte, fråga. `verktyg/konfigurera-eneo.py --visa`
gör det och visar vad som skulle registreras; `--skriv` rättar också modeller
som redan finns. Registrera max indata som gränsen minus max utdata. Utbudet och
gränserna ändras — kör om när plattformen byter modeller.

```bash
curl -s "$OPENAI_BASE_URL/chat/completions" -H "Authorization: Bearer $OPENAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"gemma4-26b-moe","max_tokens":1000000000,"messages":[{"role":"user","content":"hej"}]}'
```

Relaterat: [[sspcloud-llm-inferens]]
