# Labbet

En experimentyta för att ta reda på vad AI faktiskt kan göra i vårt arbete — och
vad som krävs för att ta något hela vägen från demo till drift.

Den här sidan är startsidan i [labbpanelen](60-miljo/panelen.md). Blocken nedan är
tomma när du läser filen på GitHub och fyllda när du läser den i panelen.

## Kör igång en uppsättning

Varje uppsättning är en kombination av tjänster som är tänkta att fungera ihop.
Panelen installerar det som saknas, startar i rätt ordning och skriver den delade
MCP-konfigurationen. Du kan trycka igen — det som redan kör lämnas i fred.

<!-- panel:uppsattningar -->

## Vad kör just nu

<!-- panel:status -->

## Enskilda tjänster

<!-- panel:tjanster -->

## Åtgärder

Sådant som inte är en tjänst men som är bra att kunna köra om. Kör du en
uppsättning ovan görs det här automatiskt.

<!-- panel:atgarder -->

## Vad vi försöker ta reda på

1. **Vilka användningsfall** i vårt arbete tjänar på AI — och vilka gör det inte?
2. **Vilka AI-tekniker** finns, och vad är de faktiskt bra på?
3. **Hur matchar man rätt teknik mot rätt användningsfall?**
4. **Vad krävs för att gå från PoC till produktion** — styrning, drift, kostnad, risk?

Fråga 3 och 4 är de svåra. Fråga 1 och 2 är förarbetet.

Vi jobbar i [två spår](00-oversikt/vision-och-mal.md#två-spår): sådant vi själva
ansvarar för, som kan gå hela vägen, och utblickar mot verksamhet andra ansvarar för,
där resultatet är ett underlag att ta vidare tillsammans med dem. Vad styrningen
kräver i respektive: [förutsättningar](00-oversikt/forutsattningar.md).

Ny här? [Läsordningen](README.md) tar dig igenom repot. Har du en halvtimme och vill
göra något: kör uppsättningen *Eneo som plattform* ovan och läs
[eneo.md](60-miljo/eneo.md) medan den installeras — den tar en plattform hela vägen
till något som liknar drift, och det är där de svåra frågorna sitter.

## Miljön

<!-- panel:miljo -->

### Tjänster i din namnrymd

Det här kör redan, oberoende av den här podden. Somligt ligger bakom inloggning.

<!-- panel:namnrymd -->

### Vad du har igång, och vad det kostar

Allt nedan lever kvar när den här podden stoppas — det är poängen med att köra
saker i namnrymden, och samtidigt det som gör att kvoten tar slut om ingen städar.
Tjänster som labbet självt deployat står med i kolumnen *Del av* och tas bort med
**Ta bort** på tjänstens kort ovan.

<!-- panel:kvot -->

## När du hittat något

Ett experiment ska sluta med ett skrivet svar — även när svaret är "det här funkade
inte". Lärdomen som nästa person behöver *innan* de börjar hör hemma i
[minnesbanken](../minnesbank/MINNE.md), inte bara i experimentfilen.

Se [BIDRA.md](../BIDRA.md) för hur du lägger till något.
