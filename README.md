# CST8911 Midterm Project - Group 6 - Tasks API

Scenario 1: a REST API on Azure Functions that stores data in Azure Cosmos DB.
The Function App uses a System-Assigned Managed Identity to access Cosmos DB,
so there is no connection string or key in the code. A Virtual Machine is used
to test the API. The VM reads the function key from Azure Key Vault.

## Architecture

```
VM (Ubuntu, Managed Identity) --reads key--> Key Vault
        |
        | curl / Postman + x-functions-key
        v
Function App (Python, Consumption plan, Managed Identity)
        |
        | DefaultAzureCredential (no key)
        v
Cosmos DB (NoSQL, serverless) - database appdb - container tasks
```

All resources are in one resource group in Canada Central.

## Data

One list called `tasks`. One document looks like this:

```json
{
  "id": "uuid",
  "title": "text",
  "status": "todo | doing | done",
  "owner": "text",
  "createdAt": "2026-10-15T14:00:00+00:00"
}
```

Cosmos DB: database `appdb`, container `tasks`, partition key `/id`.

## Endpoints

All routes start with `/api`. Auth level is `function`, so every request needs the header `x-functions-key`.

| Method | Route | Owner | Success | Error |
|---|---|---|---|---|
| POST | `/api/tasks` | Lannie | 201 + the new task | 400 if `title` or `owner` is missing |
| GET | `/api/tasks` | Member 1 | 200 + array (optional `?status=`) | - |
| GET | `/api/tasks/{id}` | Member 2 | 200 + the task | 404 |
| PUT | `/api/tasks/{id}` | Member 3 | 200 + the updated task | 404, 400 if `status` is not valid |
| DELETE | `/api/tasks/{id}` | Member 4 | 204 (no body) | 404 |

## Project structure

```
function_app.py          registers all blueprints
shared/cosmos.py         returns the Cosmos DB container (Managed Identity)
functions/create_task.py POST /api/tasks
functions/               one file per function, one function per member
tests/run_tests.sh       curl tests (key comes from an environment variable)
data/tasks-sample.json   sample data
requirements.txt
host.json
```

## How to add your function

1. Make a branch: `git checkout -b feature/get-tasks`
2. Add one file in `functions/`, for example `functions/get_tasks.py`.
   Create a `bp = func.Blueprint()` and use `get_container()` from `shared/cosmos.py`.
3. Register it in `function_app.py` with one line: `app.register_functions(your_bp)`.
4. Push the branch and open a pull request. Lannie merges it and it deploys to Azure.
5. Test with your own key: `export BASE=... KEY=...` then `bash tests/run_tests.sh` or Postman.

Please do not put any key, connection string or subscription ID in the code or in a commit.

## Settings used by the Function App

| Name | Value |
|---|---|
| `COSMOS_ENDPOINT` | `https://cst8911-g6-cosmos.documents.azure.com:443/` |
| `COSMOS_DATABASE` | `appdb` |
| `COSMOS_CONTAINER` | `tasks` |

## Team

| Name | Function |
|---|---|
| Hye Ran Yoo | POST, Azure setup, Key Vault, VM, tests |
| Member 1 | GET list, README |
| Member 2 | GET one |
| Member 3 | PUT, report |
| Member 4 | DELETE, final check and submission |
