# Kodagenter

AI-agenter som arbetar mot en kodbas: läser filer, gör ändringar, kör tester, och
itererar tills något fungerar.

Det här är den teknik som ligger närmast vårt eget dagliga arbete, och därför den
lättaste att bilda sig en egen uppfattning om. Den är också den där skillnaden mellan
demo och verklighet är som mest lärorik.

## Vad det löser

Skillnaden mot en chattbot som föreslår kod är att agenten **kör** — den ser
felmeddelandet, rättar, kör igen. Det tar bort den långsammaste delen av
kod-med-AI-slingan, som är att människan agerar budbärare mellan modellen och
terminalen.

## Vad som finns

**I miljön redan:** `opencode` och Continue är förinstallerade i Onyxias image, och
konfigureras automatiskt om AI-assistenten slås på vid start. Se
[../60-miljo/ai-verktyg-i-imagen.md](../60-miljo/ai-verktyg-i-imagen.md). Börja där —
det kostar ingenting att prova.

**Övriga:** Claude Code, Aider, Cursor med flera. De skiljer sig mindre åt i vad de
kan än i hur de arbetar — hur mycket de frågar innan de agerar, hur de hanterar
kontext i stora kodbaser, och hur väl de går att styra med projektspecifika
instruktioner.

## Vad de är bra på

Erfarenheterna i branschen är någorlunda samstämmiga:

- **Väl avgränsade uppgifter i en kodbas de kan läsa.** "Lägg till felhantering i
  den här modulen enligt mönstret i grannmodulen."
- **Mekaniskt arbete över många filer.** Omdöpningar, mönsterbyten, uppdaterade
  anrop efter en API-ändring.
- **Utforskning.** "Var hanteras X?" i en kodbas ingen kan utantill.
- **Testskrivning**, särskilt för kod som redan fungerar.
- **Kod i språk man inte behärskar men kan läsa.**

## Vad de är dåliga på

- **Uppgifter där problemet inte är klart formulerat.** Agenten producerar något som
  ser färdigt ut och som löser fel problem — vilket är dyrare än inget svar.
- **Arkitekturval.** Den optimerar lokalt. Den ser inte att hela ansatsen är fel.
- **Kodbaser utan tester.** Utan något som säger till när något gått sönder itererar
  den mot "det körde" i stället för "det blev rätt".
- **Stora ändringar i ett svep.** Kvaliteten faller med storleken på ändringen, och
  granskningskostnaden stiger.
- **Att veta när den ska sluta.** Den fortsätter gärna och gör mer än du bad om.

## Det som avgör om det blir bra

Mönstret som återkommer: **agenten är ungefär så bra som återkopplingen den får.**

En kodbas med snabba tester, tydlig struktur och skrivna konventioner ger bra
resultat. En utan ger något som ser rätt ut. Det är samma sak som gäller för en ny
kollega — men agenten säger inte till när den är osäker.

Praktiskt betyder det:

- **Små, granskningsbara ändringar.** En PR du kan läsa igenom.
- **Låt den köra testerna.** Om det inte finns tester, be den skriva dem först.
- **Skriv ner konventionerna** där agenten hittar dem — `AGENTS.md` eller
  `CLAUDE.md` i repot. Se [../../AGENTS.md](../../AGENTS.md).
- **Läs diffen.** Alltid. Att godkänna oläst kod är att flytta ansvaret ingenstans.

## Vad det kostar

Tokens, och mer än man tror — agenter läser mycket och itererar.

Men den verkliga kostnaden är **granskningstid**. Kod som produceras snabbare än den
granskas hjälper inte. Det är också det som gör att vinsten är svår att mäta: det
går fortare att skriva och långsammare att lita på.

## Testa i labbet

Det här repot är ett rimligt övningsobjekt — det är litet, publikt och ingenting går
sönder på riktigt.

Ett bra första experiment: låt en agent lägga till ett nytt användningsfall eller en
teknikbeskrivning enligt mallarna, och se hur väl den följer konventionerna i
[AGENTS.md](../../AGENTS.md). Det säger något om hur väl skrivna konventioner
faktiskt styr — vilket är samma fråga som ställs i [skills.md](skills.md).

## Vad vi har provat

| Experiment | Vad vi lärde oss |
|---|---|
| — | *(inget än)* |

## Vad vi ännu inte vet

- Hur mycket bättre blir resultatet av att peka mot en starkare modell, jämfört med
  att skriva bättre konventioner i repot?
- Fungerar de mot [plattformens öppna modeller](../60-miljo/sspcloud-llm.md), eller
  förutsätter de i praktiken en specifik leverantör?
- Vad händer med kodkvaliteten över tid i ett repo där mycket skrivs av agenter?
- Hur granskar man kod man inte skrivit, i den takt den produceras?

## Vidare läsning

- [agentupplagg.md](agentupplagg.md)
- [skills.md](skills.md)
- [../60-miljo/ai-verktyg-i-imagen.md](../60-miljo/ai-verktyg-i-imagen.md)
