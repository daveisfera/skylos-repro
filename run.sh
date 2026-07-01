#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

SKYLOS_VERSION=4.5.0

docker run --rm \
  -v "${PWD}":/usr/src/app:z,cached \
  -w /usr/src/app \
  "ghcr.io/duriantaco/skylos:${SKYLOS_VERSION}" \
  . -c 80
