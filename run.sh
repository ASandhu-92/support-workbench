#!/usr/bin/env bash
# Run a workbench script with the Stripe sandbox key decrypted from a SOPS-encrypted env file.
# The key lives only in this process's environment; nothing is written to disk or printed.
# Usage: WORKBENCH_SECRETS_FILE=secrets/stripe.enc.env ./run.sh run_all.py [args]
set -euo pipefail
cd "$(dirname "$0")"
: "${WORKBENCH_SECRETS_FILE:?set WORKBENCH_SECRETS_FILE to the SOPS-encrypted env file}"
set -a
eval "$(sops -d "$WORKBENCH_SECRETS_FILE" | grep '^STRIPE_TEST_SECRET_KEY=')"
set +a
exec "${PYTHON:-.venv/bin/python}" "$@"
