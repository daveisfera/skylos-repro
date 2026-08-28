#!/usr/bin/env bash
# Isolated from ../run.sh. A skill tree plus a 1s grep budget is enough to
# trigger SKY-ANALYSIS-INCOMPLETE and withhold unused_billing_helper.
set -euo pipefail

cd "$(dirname "$0")"

SKYLOS_VERSION=4.35.0-python3.11
IMAGE="ghcr.io/duriantaco/skylos:${SKYLOS_VERSION}"

echo "=== exclude .agents — unused_billing_helper is reported ==="
docker run --rm \
  -v "${PWD}":/usr/src/app:z,cached \
  -w /usr/src/app \
  "$IMAGE" \
  . -c 80 --exclude-folder .agents --format concise || true

echo
echo "=== include .agents, SKYLOS_GREP_BUDGET=1 — helper is withheld ==="
docker run --rm \
  -e SKYLOS_GREP_BUDGET=1 \
  -v "${PWD}":/usr/src/app:z,cached \
  -w /usr/src/app \
  "$IMAGE" \
  . -c 80 --format concise || true
