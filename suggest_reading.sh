#!/usr/bin/env bash
set -euo pipefail

set -a && source .env && set +a
.venv/bin/python scripts/suggest_reading.py --repo-root . "$@"
