# Git och autentisering i labbmiljön

## Snabbversionen

```bash
./verktyg/satt-upp-git-auth.sh
```

Kör det en gång i varje ny Onyxia-tjänst. Resten av dokumentet förklarar varför.

## Fallgropen: token i klartext i remote-URL:en

När Onyxia klonar ditt repo åt dig bakar den in din personliga access-token direkt i
remote-URL:en. Kontrollera själv:

```console
$ git remote -v
origin  https://github_pat_11ABC...XYZ@github.com/dittkonto/dittrepo.git (fetch)
```

Det fungerar, men det innebär att:

- token ligger i klartext i `.git/config`
- den syns i varje `git remote -v`
- den kommer med i skärmdumpar, felmeddelanden och klistrade terminalutdrag
- den läcker om du delar `.git`-katalogen eller kopierar repot någonstans

Samma token ligger dessutom i miljövariabeln `GIT_PERSONAL_ACCESS_TOKEN`, vilket
betyder att den syns i `env` — och därmed för allt som kör i podden.

**Det här är inte ett fel i Onyxia**, det är en medveten avvägning för att klonandet
ska fungera automatiskt. Men i en miljö där vi kör AI-agenter som läser filer och kör
kommandon är det värt att städa bort.

## Lösningen: låt gh sköta autentiseringen

GitHub CLI kan agera credential helper åt git. Token hamnar då i
`~/.config/gh/hosts.yml` i stället för i repot, och remote-URL:en blir ren.

```bash
# 1. Logga in gh med token från miljön
printf '%s' "$GIT_PERSONAL_ACCESS_TOKEN" \
  | gh auth login --hostname github.com --git-protocol https --with-token

# 2. Låt gh sköta git-autentiseringen
git config --global --unset-all credential.helper   # Onyxia sätter 'cache'
gh auth setup-git

# 3. Rensa remote-URL:en
git remote set-url origin https://github.com/dittkonto/dittrepo.git
```

Verifiera:

```bash
gh auth status
git remote -v            # ska inte innehålla något @-tecken före github.com
git fetch origin
git push --dry-run origin main
```

## Vad tokenen behöver kunna

För arbetet i det här repot räcker en fine-grained token med:

| Behörighet | Nivå | Varför |
|---|---|---|
| Contents | Read and write | klona, pusha |
| Pull requests | Read and write | `gh pr create` |
| Metadata | Read | krävs alltid |

Begränsa den till de repon du faktiskt jobbar med. Sätt ett utgångsdatum.
Behöver du inte `workflow`-behörighet — ta inte den.

## Att jobba med pull requests

```bash
git switch -c exp/mitt-experiment
# ... jobba ...
./verktyg/kontrollera-innehall.sh
git add -A && git commit -m "Experiment: kort beskrivning"
git push -u origin exp/mitt-experiment
gh pr create --fill
gh pr view --web        # öppnar i webbläsaren
```

Merge:

```bash
gh pr merge --squash --delete-branch
```

`--squash` som standard. Experimentgrenar har ofta commit-historik som inte tillför
något (`"fix"`, `"fix igen"`) och som bara gör `main` svårläst.

## Om en token läckt

Ordningen spelar roll:

1. **Spärra token först.** GitHub → Settings → Developer settings → Personal access
   tokens → *Revoke*. Gör det innan du städar något annat. En spärrad token är
   ofarlig oavsett var den ligger.
2. Skapa en ny token och kör om `./verktyg/satt-upp-git-auth.sh`.
3. Städa upp där den låg — men utgå från att den redan är komprometterad.
   Att ta bort en fil ur ett publikt repo tar inte bort den ur historiken eller ur
   GitHubs cacher.

## Hemligheter i labbet

Lägg dem i **Vault** (`VAULT_ADDR` är satt i miljön) eller i en `.env` som är
gitignorerad. Inte i repot, inte i notebook-celler, inte i en `config.yaml` du
"tar bort sen".

```bash
git check-ignore -v .env    # bekräfta att den ignoreras
```
