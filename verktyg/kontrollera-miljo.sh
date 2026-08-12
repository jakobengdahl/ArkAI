#!/usr/bin/env bash
# Visar vad som finns och vad som saknas i den aktuella labbmiljön.
# Ändrar ingenting. Kör den när du precis startat en ny tjänst i Onyxia.
set -uo pipefail

ok()   { printf '  \033[32m✓\033[0m %-22s %s\n' "$1" "${2:-}"; }
nej()  { printf '  \033[31m✗\033[0m %-22s %s\n' "$1" "${2:-}"; }
info() { printf '  \033[34mi\033[0m %-22s %s\n' "$1" "${2:-}"; }

kolla() { # kolla <namn> <kommando> [versionsflagga]
  local namn=$1 cmd=$2 flagga=${3:---version}
  if command -v "$cmd" >/dev/null 2>&1; then
    ok "$namn" "$("$cmd" "$flagga" 2>&1 | head -1 | cut -c1-60)"
  else
    nej "$namn" "saknas"
  fi
}

echo
echo "Verktyg"
kolla "git"        git
kolla "gh (GitHub CLI)" gh
kolla "python"     python3
kolla "uv"         uv
kolla "node"       node
kolla "npm"        npm
kolla "jq"         jq
kolla "kubectl"    kubectl version --client=true
kolla "helm"       helm version
kolla "mc (MinIO)" mc

echo
echo "Autentisering"
if command -v gh >/dev/null 2>&1 && gh auth status >/dev/null 2>&1; then
  ok "gh inloggad" "$(gh api user --jq .login 2>/dev/null)"
else
  nej "gh inloggad" "kör: verktyg/satt-upp-git-auth.sh"
fi
if git config --get-regexp '^credential\..*github.*\.helper' >/dev/null 2>&1; then
  ok "git credential helper" "gh sköter autentiseringen"
else
  nej "git credential helper" "kör: gh auth setup-git"
fi
if git remote get-url origin 2>/dev/null | grep -q '@github.com'; then
  nej "git remote" "TOKEN LIGGER I KLARTEXT I REMOTE-URL:EN — se docs/60-miljo/git-och-auth.md"
else
  ok "git remote" "$(git remote get-url origin 2>/dev/null || echo 'ingen remote')"
fi

echo
echo "Onyxia / Kubernetes"
info "namnrymd" "${KUBERNETES_NAMESPACE:-okänd}"
info "pod" "${HOSTNAME:-okänd}"
if kubectl auth can-i create deployments >/dev/null 2>&1; then
  ok "k8s-rättigheter" "kan skapa deployments"
else
  info "k8s-rättigheter" "läsbegränsad — starta tjänster via Onyxias katalog i stället"
fi
[ -n "${AWS_S3_ENDPOINT:-}" ] && ok "S3/MinIO" "$AWS_S3_ENDPOINT" || info "S3/MinIO" "ej konfigurerad"
[ -n "${VAULT_ADDR:-}" ] && ok "Vault" "$VAULT_ADDR (mount: ${VAULT_MOUNT:-?})" || info "Vault" "ej konfigurerad"

echo
echo "Resurser"
info "CPU" "$(nproc) kärnor"
info "Minne" "$(free -g | awk '/^Mem:/ {print $2" GB totalt, "$7" GB tillgängligt"}')"
info "Disk" "$(df -h /home/onyxia | awk 'NR==2 {print $4" ledigt"}')"

echo
echo "Tjänster i den här podden"
port_upptagen() { timeout 1 bash -c "exec 3<>/dev/tcp/127.0.0.1/$1" 2>/dev/null; }
for p in 8080 8081 3000 7474 6333 11434; do
  if port_upptagen "$p"; then
    case $p in
      8080) ok "port $p" "code-server (VS Code) — använd inte till annat" ;;
      8081) ok "port $p" "Open WebUI (om du startat det)" ;;
      11434) ok "port $p" "Ollama" ;;
      *) ok "port $p" "något lyssnar" ;;
    esac
  fi
done

echo
echo "Saknas något? Se docs/60-miljo/verktygslada.md"
echo
