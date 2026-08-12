# Riktlinjer för innehåll

**Det här repot är publikt på GitHub.** Allt som pushas hit är läsbart för vem som
helst, för alltid — även om det tas bort igen ligger det kvar i git-historiken och i
GitHubs cacher.

Riktlinjerna nedan är inte byråkrati. De är förutsättningen för att vi ska kunna
jobba öppet och snabbt utan att behöva stanna och fundera vid varje commit.

## Grundregeln

> Vi publicerar **mönster och lärdomar**, inte **vår verksamhet**.

Ett bra test: skulle den här texten vara begriplig och användbar för en arkitekt på
en helt annan myndighet eller ett annat företag? Om ja — den är rätt formulerad.
Om den bara går att förstå med intern kontext, skriv om den eller lägg den internt.

## Får inte finnas här

- Namn på kollegor, chefer, leverantörskontakter eller andra personer
- Namn på interna system, projekt, upphandlingar eller register
- Skärmdumpar, loggar, exportfiler eller diagram som inte uttryckligen rensats
- Riktiga data av något slag — personuppgifter, statistik före publicering, testdata
  som härletts från verkliga register
- Nycklar, tokens, lösenord, endpoints, interna URL:er, IP-adresser, kubeconfig
- Interna bedömningar av leverantörer, kostnader eller organisatoriska frågor
- Sådant som rör säkerhetsskydd eller informationsklassning

## Får finnas här

- Beskrivningar av användningsfall i avidentifierad form
  ("ett register med ~2 miljoner poster och kvartalsvis uppdatering", inte namnet)
- Utvärderingar av tekniker, produkter och arbetssätt
- Kod vi själva skrivit för labbet
- Konfiguration med platshållare (`<din-token>`, `.env.example`)
- Slutsatser, checklistor, mallar, mätningar från labbmiljön

## Avidentifiering i praktiken

| I stället för | Skriv |
|---|---|
| namnet på ett system | "ett handläggningsstöd", "ett källsystem för X" |
| namnet på en enhet | "en enhet på ~20 personer" |
| ett riktigt dokument | ett konstruerat exempel med samma struktur |
| en riktig personroll | "beställaren", "verksamhetsexperten" |

Är du osäker: skriv utkastet lokalt i `lokalt/` (gitignorerad) och lyft bara ut den
generella lärdomen.

## Om något ändå hamnar här

1. Berätta direkt för repoägaren — göm det inte.
2. Om det är en nyckel eller token: **spärra/rotera den först**, innan något annat.
3. Att ta bort filen räcker inte. Historiken måste skrivas om, eller repot ersättas.
   Utgå från att det som legat publikt är komprometterat.

## Innan du pushar

```bash
./verktyg/kontrollera-innehall.sh    # enkel sökning efter vanliga misstag
git diff --cached                    # läs igenom det du faktiskt commitar
```

Skriptet är ett skyddsnät, inte en godkännandestämpel. Ansvaret ligger på dig som
commitar.
