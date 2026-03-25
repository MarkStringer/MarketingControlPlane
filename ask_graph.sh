#!/usr/bin/env bash
set -euo pipefail

OPENAI_API_KEY="$(pass show api/openai)" .venv/bin/python scripts/ask_graph.py --repo-root . --interactive
