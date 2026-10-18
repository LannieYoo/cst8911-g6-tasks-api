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

# GET one
echo "=== Create a task for GET/PUT tests ==="
RESPONSE=$(curl -s -X POST "$BASE/api/tasks" \
  -H "x-functions-key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"title": "Task for GET/PUT", "owner": "Tao"}')
TASK_ID=$(echo "$RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['id'])")
echo "Created $TASK_ID"
echo

echo "=== GET /api/tasks/{id} (expect 200) ==="
curl -s -i "$BASE/api/tasks/$TASK_ID" -H "x-functions-key: $KEY"
echo
echo

echo "=== GET /api/tasks/not-a-real-id (expect 404) ==="
curl -s -i "$BASE/api/tasks/not-a-real-id" -H "x-functions-key: $KEY"
echo
echo

# PUT One

echo "=== PUT /api/tasks/{id} valid status (expect 200) ==="
curl -s -i -X PUT "$BASE/api/tasks/$TASK_ID" \
  -H "x-functions-key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "doing"}'
echo
echo

echo "=== PUT /api/tasks/{id} invalid status (expect 400) ==="
curl -s -i -X PUT "$BASE/api/tasks/$TASK_ID" \
  -H "x-functions-key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "finished"}'
echo
echo

echo "=== PUT /api/tasks/not-a-real-id (expect 404) ==="
curl -s -i -X PUT "$BASE/api/tasks/not-a-real-id" \
  -H "x-functions-key: $KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "done"}'
echo

# DELETE

echo "=== DELETE /api/tasks/{id} (expect 204) ==="
curl -s -i -X DELETE "$BASE/api/tasks/$TASK_ID" -H "x-functions-key: $KEY"
echo
echo

echo "=== GET the deleted task (expect 404) ==="
curl -s -i "$BASE/api/tasks/$TASK_ID" -H "x-functions-key: $KEY"
echo
echo

echo "=== DELETE /api/tasks/not-a-real-id (expect 404) ==="
curl -s -i -X DELETE "$BASE/api/tasks/not-a-real-id" -H "x-functions-key: $KEY"
echo
