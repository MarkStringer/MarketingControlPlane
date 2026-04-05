#!/usr/bin/env bash
set -euo pipefail

OPENAI_API_KEY="$(pass show api/openai)" \
ANTHROPIC_API_KEY="$(pass show api/anthropic 2>/dev/null || true)" \
  .venv/bin/python scripts/suggest_reading.py --repo-root . "$@"
