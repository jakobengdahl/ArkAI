# Styrning och risk

Det här dokumentet beskriver **vilka frågor som behöver besvaras** och var de brukar
gå snett. Det är inte juridisk vägledning och ersätter inte de ordinarie processerna
för informationssäkerhet, dataskydd och arkitekturstyrning.

Poängen är att de här frågorna är billigast att ställa tidigt. Ställs de först vid
införandet blir svaret ofta att lösningen måste byggas om.

## De frågor som faktiskt avgör

### Vem ansvarar för besluten?

En AI-lösning som tar fram underlag flyttar inte ansvaret för beslutet. Men den
flyttar **var uppmärksamheten läggs** — och det räcker för att ändra utfallet.

Det är väl belagt att människor godkänner maskinförslag mer okritiskt ju oftare
förslagen visat sig rätt. Det är inte slarv, det är hur uppmärksamhet fungerar. En
lösning som är rätt 95 % av gångerna får granskaren att sluta granska lagom till de
5 % som betyder något.

Det ska hanteras i utformningen, inte i en instruktion om att vara uppmärksam:

- gör osäkerheten synlig i det enskilda fallet, inte som en generell brasklapp
- kräv aktivt ställningstagande där det spelar roll, inte ett bekräftelseklick
- mät om granskarna faktiskt hittar de fel som planteras

### Vad händer med underlaget?

För varje lösning:

- Vad skickas iväg, och vart?
- Sparas det? Var, hur länge, vem kommer åt det?
- Används det till att träna något?
- Vad har lovats — och var står det?

I labbet är [plattformens egen inferens](../60-miljo/sspcloud-llm.md) utgångspunkten
just för att den flyttar de här frågorna till plattformsnivå.

### Går det att förklara i efterhand?

När någon frågar "varför blev det så här?" — går det att svara?

Det kräver att anropen sparas: vad frågades, vilken kontext lades in, vad svarade
modellen, vilken modellversion. Langfuse finns i Onyxias katalog och gör det.

Sätt upp det **innan** piloten. Det går inte att rekonstruera i efterhand, och det är
alltid i efterhand frågan kommer.

### Vad händer när modellen byts?

Modeller byts, utgår och uppdateras. Ett byte kan ändra beteendet på sätt som inte
syns förrän någon råkar på det.

Därför: regressionstester mot kända fall, som körs vid varje modellbyte. Utan dem
har vi en lösning som fungerar tills någon annan uppdaterar något.

Det här är extra relevant här eftersom modellutbudet bestäms på plattformsnivå — vi
styr det inte själva.

## Risker som är specifika för det vi håller på med

### Minnesbanken kan bli fel

En felaktig minnespost är sämre än ingen post, för den ser lika trovärdig ut och
sprids till alla som använder minnesbanken. Ett personligt minne som blir fel drabbar
en person; ett delat minne drabbar alla.

Det är därför [minnesbanken](../../minnesbank/) har PR-granskning som regel. Att
någon annan läser är hela skillnaden mot ett personligt minne — och den enda spärren
mot att en AI-assistent skriver in något felaktigt som sedan blir sanning.

### Agenter har bredare åtkomst än man tror

En agent med skalåtkomst har åtkomst till allt du har. I den här miljön ligger
git-token, S3-uppgifter, `VAULT_TOKEN` och LLM-nycklar i miljövariabler och i
hemkatalogen — se
[minnesbanken](../../minnesbank/verktyg/api-nycklar-i-hemkatalogen.md).

I labbet är det hanterbart. Det slutar vara hanterbart i samma sekund som en agent
får åtkomst till något som betyder något.

### Kunskapen sitter hos några få

Ironin i det här arbetet: vi försöker lösa att kunskap sitter i huvudet på ett fåtal
personer, med verktyg som få behärskar.

Motmedel är att skriva ner arbetssätten (det här repot), och att låta fler än en
person köra varje experiment. Om bara en person kan starta något är det inte en
lösning, det är ett beroende.

### Vi mäter fel sak

Det är lätt att mäta "hur bra svarade modellen" och svårt att mäta "blev arbetet
bättre". Om det tar längre tid att kontrollera svaret än att göra jobbet själv har vi
flyttat arbete och lagt till en risk — även när svaren är bra.

Mät på arbetet, inte på modellen.

## Vad vi bör ta reda på

Öppna frågor som är för stora för ett experiment men som behöver besvaras:

- Vilka regelverk träffar en AI-lösning i vår typ av verksamhet, och vad kräver de
  konkret för de användningsfall vi har?
- Vad krävs för att koppla åtkomsten till användarens behörigheter i stället för till
  en teknisk användare? Det är den enskilt vanligaste blockeraren mot produktion.
- Hur ser ett rimligt utvärderingsförfarande ut som inte tar mer tid än lösningen
  sparar?
- Vem äger AI-lösningar i förvaltningen — och vad händer om ingen gör det?

## Vidare läsning

- [checklista.md](checklista.md)
- [kostnad-och-drift.md](kostnad-och-drift.md)
- [../00-oversikt/mognadstrappa.md](../00-oversikt/mognadstrappa.md)
