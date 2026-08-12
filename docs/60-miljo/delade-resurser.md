# Dela resurser med kollegor

Att dela är inte en detalj i det här arbetet — det är själva frågan. Om varje person
bygger upp sitt eget minne, sina egna verktyg och sina egna erfarenheter får vi
ingen effekt av att vara flera. Det här dokumentet beskriver vilka delningsmekanismer
miljön faktiskt erbjuder och vad de passar till.

## Fyra sätt att dela, med olika egenskaper

| Mekanism | Vad som delas | Passar för | Begränsning |
|---|---|---|---|
| **Git-repo (det här)** | Text, kod, dokumentation | Kunskap som tål att vara publik | Publikt — inga interna detaljer |
| **Onyxia-projekt** | Namnrymd, S3-bucket, hemligheter, inställningar | Gemensamma tjänster och större datamängder | Skapas av instansadministratör |
| **S3-bucket / prefix** | Filer | Data, index, modeller, större minnesmängder | Behörigheter styrs i MinIO, inte av Onyxia |
| **Vault** | Hemligheter | Nycklar som flera behöver | Bara hemligheter, inget innehåll |

Poängen med tabellen är att de inte konkurrerar. En delad minnesbank kommer troligen
att använda flera: texten i git, vektorindexet i S3, nycklarna i Vault.

## Onyxia-projekt

Onyxia har ett projektbegrepp för grupper av användare. Är du med i ett projekt får
du en väljare i sidhuvudet för att växla mellan ditt personliga utrymme och
projektets.

Alla i ett projekt delar:

- **Kubernetes-namnrymden** — du ser allas tjänster under "My Services", inte bara
  dina egna
- **S3-bucket** (eller ett prefix i en bucket)
- **Hemligheter** i Vault
- **Projektinställningar** — ändrar en person något gäller det för alla

Det sista är värt att ta på allvar: en delad namnrymd innebär att någon annan kan
stoppa din tjänst, och att era resurskvoter är gemensamma. Det är rätt egenskap för
ett labb där ni jobbar tillsammans, fel egenskap om ni bara vill dela filer.

Projekt skapas av instansens administratörer på begäran —
[Onyxias dokumentation](https://docs.onyxia.sh/admin-doc/setting-up-group-projects.md)
beskriver det.

## S3

Onyxia proxar inte S3. Filutforskaren hämtar tillfälliga STS-uppgifter åt dig utifrån
din inloggning, och pratar sedan direkt med MinIO. Det får två konsekvenser som är
lätta att snubbla på:

**Åtkomsträttigheter styrs i MinIO, inte i Onyxia.** Onyxia visar bara det du redan
har rätt till. Vill du ändra vem som kommer åt vad är det en fråga för dem som
förvaltar S3-instansen.

**Uppgifterna är tidsbegränsade och roteras.** `AWS_ACCESS_KEY_ID` med flera finns i
miljön i en körande tjänst, men de går ut. Skriv aldrig in dem i kod eller
konfiguration — läs dem från miljövariablerna varje gång.

```bash
mc ls s3/                       # aliaset s3 är förkonfigurerat
mc cp fil.parquet s3/<bucket>/  # eller använd AWS_*-variablerna från valfritt SDK
```

### Dela ut en mapp

Det går att dela ut en katalog så att den blir läsbar för andra — även för vem som
helst — men då **read only**. Det är rätt mekanism för att publicera ett dataset,
ett färdigbyggt index eller en modell som andra ska kunna hämta.

Det är fel mekanism för något som flera ska kunna skriva till. För det behövs ett
projekt med gemensam bucket.

### Rådet om att inte ladda ner

Onyxias egen rekommendation är att läsa data direkt från S3 in i minnet i stället för
att först ladda ner den till containern. Det är bra vana av flera skäl: containern är
förgänglig, kopior blir inaktuella, och nedladdad data hamnar lätt i ett git-repo av
misstag.

## Vault

Key–value v2, nåbart via hemlighetsutforskaren eller `VAULT_ADDR` + `VAULT_TOKEN` i
en körande tjänst. Hemligheter kan monteras in i en tjänst när den startar, om
Helm-charten stödjer det.

Det är här nycklar hör hemma — inte i repot, inte i en notebook-cell, inte i en
`config.yaml` som ska städas bort sen.

## Vad vi väljer för minnesbanken

Just nu ligger [minnesbanken](../../minnesbank/) i git. Det är rätt val medan den är
liten:

- versionshanterad, granskningsbar via pull request
- läsbar för både människor och AI-verktyg utan särskild infrastruktur
- fungerar utan att någon behöver sätta upp något

Det slutar vara rätt val när minnesbanken blir för stor för att indexeras som text,
eller när den behöver innehålla sådant som inte kan vara publikt. Då blir det
aktuellt med ett Onyxia-projekt med delad S3 och ett sök- eller grafindex — se
[../20-tekniker/grafminne.md](../20-tekniker/grafminne.md).

Att veta *när* den gränsen passeras är ett av de mer värdefulla resultat vi kan få
ut av det här labbet. Det är en fråga alla som bygger en kunskapsbas kommer att ställa.
