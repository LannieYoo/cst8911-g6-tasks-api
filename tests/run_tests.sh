#!/bin/bash
# Test the tasks API from the command line.
#
# Usage:
#   export BASE=https://cst8911-g6-api.azurewebsites.net
#   export KEY=<function key>      # never write the key in this file
#   bash tests/run_tests.sh
#
# On the VM the key is read from Key Vault before this script runs.

set -e

: "${BASE:?Set BASE to the Function App URL}"
: "${KEY:?Set KEY to a function key}"

echo "=== POST /api/tasks (expect 201) ==="
curl -s -i -X POST "$BASE/api/tasks" \
  -H "x-functions-key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Write the report", "owner": "Lannie"}'
echo
echo

echo "=== POST /api/tasks without owner (expect 400) ==="
curl -s -i -X POST "$BASE/api/tasks" \
  -H "x-functions-key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "No owner"}'
echo
echo

echo "=== GET /api/tasks (expect 200 + array) ==="
curl -s -i "$BASE/api/tasks"   -H "x-functions-key: $KEY"
echo
echo

echo "=== GET /api/tasks?status=todo (expect 200, only todo tasks) ==="
curl -s -i "$BASE/api/tasks?status=todo"   -H "x-functions-key: $KEY"
echo
echo

echo "=== GET /api/tasks without key (expect 401) ==="
curl -s -i "$BASE/api/tasks"
echo
echo

# GET one, PUT and DELETE are added here when those functions are merged.
