# Chattbot plus verktyg

En chattbot som kan anropa funktioner — söka i ett register, läsa en fil, köra en
beräkning, anropa ett API — i stället för att bara svara utifrån vad modellen råkar
minnas.

För de flesta av våra användningsfall är det här den mest realistiska formen. Inte
den mest avancerade, men den som människor faktiskt använder.

## Vad det löser

En modell utan verktyg kan bara producera text utifrån sin träningsdata och det som
står i kontexten. Den vet inte vad som står i vårt register, vad statusen är just nu,
eller vad som gäller efter senaste ändringen. Den kommer ändå att svara — det är
problemet.

Med verktyg flyttas svaret från "vad modellen minns" till "vad systemet vet". Det
är skillnaden mellan något som låter rätt och något som är rätt.

## Hur det fungerar

Modellen får en lista över tillgängliga funktioner med beskrivningar. Under samtalet
kan den välja att anropa en; resultatet läggs i kontexten och den fortsätter svara.

Tre saker avgör om det blir bra, och ingen av dem handlar om modellen:

**Beskrivningen av verktyget.** Det är allt modellen har att gå på. Vagt beskrivna
funktioner anropas inte, eller anropas i fel läge.

**Storleken på svaret.** Verktygsresultat äter kontext. En funktion som returnerar
hela tabellen förstör sessionen. Låt den sammanfatta eller paginera.

**Vad som händer när verktyget fel.** Ett felmeddelande modellen inte förstår leder
till att den gissar vidare som om ingenting hänt. Skriv felmeddelanden för
läsaren — som här är en modell.

## Koppla in verktyg

| Väg | När |
|---|---|
| **MCP** | Standardvägen. Skriv en gång, använd från flera klienter. Se [mcp.md](mcp.md). |
| **Open WebUI-verktyg** | Python-funktioner direkt i gränssnittet. Snabbast att prova, bundet till Open WebUI. |
| **CLI via en agent** | Låt agenten köra befintliga kommandon. Nästan ingen utvecklingstid — men bredare åtkomst än du kanske tror. |
| **Direkt i API-anropet** | Full kontroll, egen applikation. |

CLI-vägen är underskattad. Har vi redan ett kommandoradsverktyg som gör något är det
ofta snabbare att låta en agent köra det än att bygga en integration. Men en agent
med skalåtkomst har åtkomst till allt du har — se avsnittet om säkerhet i
[agentupplagg.md](agentupplagg.md).

## När det passar

- Uppgifter där svaret finns i ett system, inte i modellen
- Där användaren ska ha kvar kontrollen och kunna följa med i vad som händer
- När underlaget behöver hämtas färskt varje gång
- Som första steg för nästan alla våra användningsfall — det är enklare att gå från
  chattbot till agent än tvärtom

## När det inte passar

- **Uppgifter som ska köras utan att någon tittar på.** Då är det en agent eller ett
  schemalagt jobb, inte en chatt.
- **Där svaret måste vara rätt varje gång.** Verktyg minskar hallucinationer men tar
  inte bort dem. Modellen kan fortfarande tolka ett korrekt verktygssvar fel.
- **Där verktyget kan göra skada.** Ett verktyg som ändrar något behöver ett
  medvetet godkännandesteg, inte bara en bra prompt.
- **Där användaren inte kan bedöma svaret.** Om det tar längre tid att kontrollera
  än att göra jobbet själv har vi flyttat arbete, inte tagit bort det. Det här är
  den vanligaste orsaken till att en pilot inte går vidare.

## Vad det kostar

Att bygga: mindre än man tror. Att bygga så att det används rätt: mer än man tror.

Löpande kostnad är främst tokens — varje verktygsanrop lägger sitt resultat i
kontexten och hela konversationen skickas om vid varje tur. Långa sessioner med
stora verktygssvar blir dyra på ett sätt som inte syns förrän det skalar.

## Testa i labbet

[Open WebUI](../60-miljo/openwebui.md) är uppsatt för det här. Peka den mot
[plattformens inferens](../60-miljo/sspcloud-llm.md), koppla in ett verktyg, kör ett
riktigt användningsfall.

Prova samma uppgift med och utan verktyget. Skillnaden är ofta mindre dramatisk än
man tror på enkla frågor, och mycket större på frågor där modellen annars skulle
gissa — och det är just den skillnaden som är värd att kunna visa.

## Vad vi har provat

| Experiment | Vad vi lärde oss |
|---|---|
| — | *(inget än)* |

## Vad vi ännu inte vet

- Hur märker användaren skillnad på ett svar som bygger på ett verktygsanrop och ett
  som modellen hittat på? Ska det synas i gränssnittet?
- Hur många verktyg klarar en modell innan den börjar välja fel?
- Vad krävs för att koppla verktygen till användarens behörigheter i stället för
  till en teknisk användare?

Den sista är den fråga som avgör om något kan gå mot produktion hos oss.
