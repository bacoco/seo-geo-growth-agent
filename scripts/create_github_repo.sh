#!/usr/bin/env bash
set -euo pipefail

: "${GITHUB_TOKEN:?Set GITHUB_TOKEN in your shell, not in repository files}"
: "${GITHUB_OWNER:?Set GITHUB_OWNER to your GitHub user or organization}"
: "${GITHUB_REPO:=seo-geo-growth-agent}"
: "${GITHUB_PRIVATE:=false}"

payload=$(python3 - <<'PY'
import json, os
print(json.dumps({
    "name": os.environ.get("GITHUB_REPO", "seo-geo-growth-agent"),
    "private": os.environ.get("GITHUB_PRIVATE", "false").lower() == "true",
    "description": "Agent-ready SEO + GEO skill for search growth, AI-search visibility, crawler policy, measurement, and agent UX.",
    "has_issues": True,
    "has_projects": False,
    "has_wiki": False,
}))
PY
)

# User repos use /user/repos. Organization repos use /orgs/{org}/repos.
status=$(curl -sS -o /tmp/github_repo_create_response.json -w "%{http_code}" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/repos \
  -d "$payload")

if [[ "$status" == "201" ]]; then
  echo "Created user repository: ${GITHUB_OWNER}/${GITHUB_REPO}"
  exit 0
fi

# If creating under an org, try org endpoint.
status=$(curl -sS -o /tmp/github_repo_create_response.json -w "%{http_code}" \
  -H "Authorization: Bearer ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  "https://api.github.com/orgs/${GITHUB_OWNER}/repos" \
  -d "$payload")

if [[ "$status" == "201" ]]; then
  echo "Created organization repository: ${GITHUB_OWNER}/${GITHUB_REPO}"
  exit 0
fi

echo "GitHub API returned HTTP $status" >&2
cat /tmp/github_repo_create_response.json >&2
exit 1
