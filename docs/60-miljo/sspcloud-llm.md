# Plattformens LLM-inferens

SSP Cloud kör en egen inferenstjänst med öppna modeller. Som användare kan du ta ut
en API-nyckel och använda den både inifrån labbmiljön och externt.

Det är en viktig pusselbit i det här arbetet: den gör att vi kan experimentera med
riktiga modellanrop utan att blanda in externa leverantörer, och den ger oss ett
konkret exempel på hur en plattformsburen AI-tjänst kan se ut.

## Vad det är

Tjänsten ligger på **<https://llm.lab.sspcloud.fr>**. Gränssnittet är Open WebUI
(samma produkt som vi installerar lokalt i [openwebui.md](openwebui.md), version 0.11.0
när det här skrevs) med öppna modeller bakom.

Att det är Open WebUI är praktiskt: API:et är OpenAI-kompatibelt, vilket innebär att
i princip allt vi bygger kan peka mot det utan anpassning.

## Hämta en API-nyckel

I gränssnittet: **profilmenyn → Settings → Account → API keys → Create new key**.

Nyckeln är personlig och knuten till ditt konto. Behandla den som ett lösenord:

- Lägg den i `.env` (gitignorerad) eller i Vault — aldrig i repot
- Dela den inte med kollegor, de tar ut en egen
- Har den läckt: ta bort den i gränssnittet och skapa en ny

## Använda den

Bas-URL är `https://llm.lab.sspcloud.fr/api` och anrop följer OpenAI-formatet.

```bash
# i .env
SSPCLOUD_LLM_BASE_URL=https://llm.lab.sspcloud.fr/api
SSPCLOUD_LLM_API_KEY=<din-nyckel>
```

Lista modeller:

```bash
curl -s "$SSPCLOUD_LLM_BASE_URL/models" \
  -H "Authorization: Bearer $SSPCLOUD_LLM_API_KEY" | jq -r '.data[].id'
```

Ett anrop:

```bash
curl -s "$SSPCLOUD_LLM_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $SSPCLOUD_LLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model":"<modell-id>","messages":[{"role":"user","content":"Hej!"}]}' \
  | jq -r '.choices[0].message.content'
```

Från Python med OpenAI-biblioteket:

```python
import os
from openai import OpenAI

klient = OpenAI(
    base_url=os.environ["SSPCLOUD_LLM_BASE_URL"],
    api_key=os.environ["SSPCLOUD_LLM_API_KEY"],
)
svar = klient.chat.completions.create(
    model="<modell-id>",
    messages=[{"role": "user", "content": "Hej!"}],
)
print(svar.choices[0].message.content)
```

Kör `curl .../models` innan du hårdkodar ett modellnamn — utbudet ändras.

## Koppla in den i din egen Open WebUI

Din lokala instans kan använda plattformens modeller som backend. I `.env`:

```bash
ENABLE_OPENAI_API=True
OPENAI_API_BASE_URL=https://llm.lab.sspcloud.fr/api
OPENAI_API_KEY=<din-nyckel>
```

Poängen med att köra en egen instans blir då tydligare: det är inte modellerna du
experimenterar med, det är **upplägget** — verktyg, minnesbank, kunskapskällor,
systemprompt, flera användare. Modellerna kommer utifrån.

## Vad det betyder för valen vi ska göra

Att plattformen tillhandahåller inferens ändrar kalkylen på ett par sätt som är värda
att ha med sig:

**Modellvalet blir en plattformsfråga, inte en projektfråga.** Vilka modeller som
finns bestäms centralt. Bygger vi något som förutsätter en specifik modells beteende
har vi skapat ett beroende vi inte styr över — se
[50-fran-poc-till-produktion/checklista.md](../50-fran-poc-till-produktion/checklista.md).

**Öppna modeller är inte automatiskt sämre — de är annorlunda.** Kvaliteten varierar
mer mellan uppgiftstyper. Det gör det viktigare att utvärdera per användningsfall än
att förlita sig på en allmän ranking.

**Det finns ett tydligt före/efter att jämföra mot.** Samma användningsfall mot
plattformens modeller respektive mot en extern leverantör är ett av de mest
informativa experiment vi kan göra — inte bara tekniskt, utan för att kunna svara på
vad skillnaden faktiskt är värd.

## Relaterat

- [ai-verktyg-i-imagen.md](ai-verktyg-i-imagen.md) — Onyxia kan koppla in inferensen
  automatiskt i utvecklingsverktygen när tjänsten startar
- [openwebui.md](openwebui.md) — din egen instans
- [../20-tekniker/agentupplagg.md](../20-tekniker/agentupplagg.md) — agenter som kan
  peka mot en OpenAI-kompatibel endpoint
