# Kostnad och drift

Vad något kostar att köra, och vad det kostar att fortsätta köra. Det andra
underskattas systematiskt.

## De fyra kostnaderna

| | Vad | Syns när |
|---|---|---|
| **Anrop** | Tokens in och ut | Direkt, i fakturan |
| **Infrastruktur** | Databaser, index, tjänster som ska stå uppe | Månadsvis |
| **Människor** | Bygga, förvalta, utvärdera, granska | Aldrig, om ingen räknar |
| **Granskning** | Tiden att kontrollera det AI:n producerat | Aldrig, men den är ofta störst |

De två sista är de som avgör om något är värt att göra, och de två som saknas i de
flesta kalkyler.

## Tokens

Det som driver kostnaden är sällan svaren — det är **kontexten**. Hela
konversationen skickas om vid varje tur, och verktygsresultat, uppladdade dokument
och inladdad kunskap ligger kvar i den.

Praktiska konsekvenser:

- Långa sessioner blir dyra på ett sätt som inte syns i en demo
- Ett verktyg som returnerar för mycket kostar vid varje efterföljande tur, inte bara
  en gång
- Att lägga hela minnesbanken i kontexten kostar vid varje anrop — se
  [index före innehåll](../../minnesbank/arbetssatt/index-fore-innehall.md)
- **Svensk text kostar fler tokens än engelsk** för samma innehåll. Det är värt att
  känna till när man jämför med kalkyler och riktmärken som nästan alltid bygger på
  engelska.

Mät tidigt. Storleksordningen räcker — men "vi vet inte" duger inte in i en pilot.

## Infrastruktur

I labbet är det gratis i praktiken; tjänsterna startas från Onyxias katalog och
körs på delade resurser. Det gör det lätt att glömma att varje tjänst är något som
ska förvaltas i skarpt läge.

Regeln: **varje tjänst du startar är en sak någon ska hålla igång.** Ett vektorindex,
en grafdatabas och en spårningstjänst är tre saker att uppgradera, säkerhetskopiera
och felsöka. Är nyttan värd det?

Det är ett argument för att börja enkelt. En katalog med textfiler i git har
driftkostnad noll.

## Människor

Den största posten, och den som aldrig står i kalkylen.

- Bygga: engångskostnad, oftast överskattad
- **Utvärdera:** löpande, oftast helt bortglömd. Utan den vet vi inte om kvaliteten
  hållit i sig
- Förvalta: uppdateringar, modellbyten, ändrade underlag
- Lära andra: om bara en person kan köra det är det inte en lösning

## Granskningskostnaden

Om AI:n producerar något som en människa måste kontrollera är kontrolltiden en del av
kostnaden.

Det leder till en obekväm slutsats som är värd att ta på allvar: **en lösning som är
80 % rätt kan vara dyrare än ingen lösning alls**, för att granskaren måste läsa allt
lika noga ändå — men nu utan att ha byggt upp förståelsen genom att göra arbetet
själv.

Frågan att ställa är inte "hur ofta har den rätt" utan **"hur snabbt kan någon avgöra
om den har rätt?"**. Det är därför källhänvisningar och synliga mellansteg är
kostnadsposter, inte finess.

## Vad vi bör mäta i varje experiment

Skriv ner det i experimentfilen — det tar en minut och gör experimenten jämförbara:

- Ungefärlig tokenförbrukning för en typisk uppgift
- Hur lång tid det tog att sätta upp
- Hur lång tid en granskning tog, jämfört med att göra uppgiften för hand
- Vad som skulle behöva stå uppe för att någon annan skulle kunna använda det

Sista punkten är den som förvandlar ett experiment till ett underlag för beslut.

## Vad vi ännu inte vet

- Vad kostar plattformens egen inferens jämfört med en extern leverantör, räknat på
  våra faktiska användningsfall?
- Hur skalar granskningskostnaden när fler använder samma lösning — går den ner när
  förtroendet byggs, eller upp när volymen ökar?
- Vad kostar det att förvalta en minnesbank som faktiskt hålls aktuell?
