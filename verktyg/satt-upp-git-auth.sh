#!/usr/bin/env bash
# Sätter upp git- och GitHub-autentisering i en färsk Onyxia-tjänst.
#
# Onyxia lägger din personliga access-token i miljövariabeln
# GIT_PERSONAL_ACCESS_TOKEN och bakar dessutom in den i remote-URL:en. Det
# fungerar, men innebär att token ligger i klartext i .git/config och följer med
# i varje `git remote -v`. Det här skriptet flyttar den till gh:s credential
# helper i stället och rensar URL:en.
#
# Kör: ./verktyg/satt-upp-git-auth.sh
set -euo pipefail

command -v gh >/dev/null || { echo "gh saknas. Se docs/60-miljo/verktygslada.md"; exit 1; }

# 1. Logga in gh
if gh auth status >/dev/null 2>&1; then
  echo "gh är redan inloggad som $(gh api user --jq .login)"
else
  if [ -n "${GIT_PERSONAL_ACCESS_TOKEN:-}" ]; then
    echo "Loggar in gh med token från miljön (GIT_PERSONAL_ACCESS_TOKEN)."
    printf '%s' "$GIT_PERSONAL_ACCESS_TOKEN" \
      | gh auth login --hostname github.com --git-protocol https --with-token
  else
    echo "Ingen token i miljön. Kör en interaktiv inloggning:"
    echo "  gh auth login --hostname github.com --git-protocol https"
    exit 1
  fi
fi

# 2. Låt gh sköta git-autentiseringen
git config --global --unset-all credential.helper 2>/dev/null || true
gh auth setup-git

# 3. Ta bort inbäddad token ur remote-URL:en
if git rev-parse --git-dir >/dev/null 2>&1; then
  URL=$(git remote get-url origin 2>/dev/null || true)
  if [ -n "$URL" ] && [[ "$URL" == *"@github.com"* ]]; then
    REN="https://github.com/${URL#*@github.com/}"
    git remote set-url origin "$REN"
    echo "Rensade remote-URL:en: $REN"
  fi
fi

# 4. Identitet på commits
git config --global user.name  "${GIT_USER_NAME:-$(git config --global user.name)}"
git config --global user.email "${GIT_USER_MAIL:-$(git config --global user.email)}"

echo
echo "Klart:"
echo "  konto   $(gh api user --jq .login)"
echo "  namn    $(git config --global user.name)"
echo "  e-post  $(git config --global user.email)"
echo "  remote  $(git remote get-url origin 2>/dev/null || echo '-')"
echo
echo "Testa:  git fetch origin && git push --dry-run origin \$(git branch --show-current)"
