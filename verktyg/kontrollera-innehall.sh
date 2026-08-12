#!/usr/bin/env bash
# Letar efter sådant som inte hör hemma i ett publikt repo.
# Ett skyddsnät — inte en godkännandestämpel. Läs alltid din egen diff.
#
#   verktyg/kontrollera-innehall.sh          # kontrollera det som är stagat
#   verktyg/kontrollera-innehall.sh --allt   # kontrollera alla spårade filer
set -uo pipefail
cd "$(git rev-parse --show-toplevel)" || exit 1

if [ "${1:-}" = "--allt" ]; then
  FILER=$(git ls-files)
  echo "Kontrollerar alla spårade filer."
else
  FILER=$(git diff --cached --name-only --diff-filter=ACM)
  echo "Kontrollerar stagade filer. (--allt för hela repot)"
fi
[ -z "$FILER" ] && { echo "Inget att kontrollera."; exit 0; }

TRAFFAR=0
larm() { printf '\033[31m  ! %s\033[0m\n    %s\n' "$1" "$2"; TRAFFAR=$((TRAFFAR+1)); }

sok() { # sok <beskrivning> <regex> [-i]
  local beskrivning=$1 regex=$2 rad
  while IFS= read -r rad; do
    [ -n "$rad" ] && larm "$beskrivning" "$rad"
  done < <(echo "$FILER" | tr '\n' '\0' \
    | xargs -0 -r grep -nIE ${3:-} --exclude='kontrollera-innehall.sh' "$regex" 2>/dev/null \
    | cut -c1-160)
}

echo
sok "Möjlig nyckel eller token" \
  '(gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{20,}|xox[baprs]-|AKIA[0-9A-Z]{16}|-----BEGIN [A-Z ]*PRIVATE KEY-----|eyJ[A-Za-z0-9_-]{20,}\.[A-Za-z0-9_-]{20,}\.)'
sok "Tilldelad hemlighet med värde" \
  '^[^#]*(password|passwd|secret|api[_-]?key|access[_-]?token|client[_-]?secret)[[:space:]]*[:=][[:space:]]*["'"'"']?[A-Za-z0-9/_+-]{12,}' -i
# Fångar både user:pass@host och den form Onyxia använder: <token>@host
sok "Inbäddade uppgifter i URL" \
  'https?://[^/[:space:]"]+@[A-Za-z0-9.-]+'
sok "Intern adress eller IP" \
  '(\b10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\b|\b192\.168\.[0-9]{1,3}\.[0-9]{1,3}\b|[a-z0-9-]+\.(internal|intra|local|lan)\b)'
sok "E-postadress" \
  '[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'

# Filtyper som nästan aldrig hör hemma här
while IFS= read -r f; do
  case "$f" in
    *.csv|*.xlsx|*.xls|*.parquet|*.db|*.sqlite3|*.pem|*.key|*.p12|*.pfx|*.pdf|*.docx|*.pptx)
      larm "Filtyp som sällan hör hemma i repot" "$f" ;;
  esac
  # Stora filer är ofta oavsiktliga exporter
  if [ -f "$f" ] && [ "$(stat -c%s "$f" 2>/dev/null || echo 0)" -gt 1048576 ]; then
    larm "Fil större än 1 MB" "$f"
  fi
done <<< "$FILER"

echo
if [ "$TRAFFAR" -eq 0 ]; then
  printf '\033[32mInga träffar.\033[0m Läs ändå igenom din diff innan du pushar:\n  git diff --cached\n\n'
  exit 0
else
  printf '\033[31m%d träff(ar).\033[0m Alla är inte fel — e-postadresser i en git-config-\n' "$TRAFFAR"
  printf 'exempel är ofarliga, en riktig kollegas adress är det inte. Bedöm varje träff.\n'
  printf 'Se RIKTLINJER-INNEHALL.md.\n\n'
  exit 1
fi
