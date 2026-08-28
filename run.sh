#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

SKYLOS_VERSION=4.35.0-python3.11

docker run --rm \
  -v "${PWD}":/usr/src/app:z,cached \
  -w /usr/src/app \
  "ghcr.io/duriantaco/skylos:${SKYLOS_VERSION}" \
  . -c 80 --exclude-folder grep_budget_withhold --format concise
