#!/usr/bin/env bash
# Print one "{path}<TAB>{secret|large}" line for each changed path that needs the owner's decision.
# Run from the repository root; candidates are staged, unstaged, and untracked paths.
set -euo pipefail
{ git ls-files -mo --exclude-standard -z; git diff --cached --name-only -z; } | sort -zu |
  while IFS= read -r -d '' path; do
    case "${path##*/}" in
      .env | .env.* | credentials* | *secret* | *.pem | *.key)
        printf '%s\tsecret\n' "$path"
        ;;
    esac
    if [ -f "$path" ] && [ "$(stat -c %s -- "$path")" -gt 5000000 ]; then
      printf '%s\tlarge\n' "$path"
    fi
  done
