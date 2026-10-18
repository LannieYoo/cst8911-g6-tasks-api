import json
import logging

import azure.functions as func
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from shared.cosmos import get_container

bp = func.Blueprint()

VALID_STATUS = ["todo", "doing", "done"]
UPDATABLE_FIELDS = ("title", "status", "owner")


def json_response(data, status_code):
    return func.HttpResponse(
        json.dumps(data),
        status_code=status_code,
        mimetype="application/json",
    )


@bp.route(route="tasks/{id}", methods=["PUT"], auth_level=func.AuthLevel.FUNCTION)
def update_task(req: func.HttpRequest) -> func.HttpResponse:
    """PUT /api/tasks/{id} - update one task."""
    task_id = req.route_params.get("id")
    logging.info("PUT /api/tasks/%s", task_id)

    try:
        body = req.get_json()
    except ValueError:
        return json_response({"error": "Request body must be JSON"}, 400)

    if not isinstance(body, dict):
        return json_response({"error": "Request body must be a JSON object"}, 400)

    if "status" in body and body["status"] not in VALID_STATUS:
        return json_response({"error": "status must be todo, doing or done"}, 400)

    container = get_container()
    try:
        task = container.read_item(item=task_id, partition_key=task_id)
    except CosmosResourceNotFoundError:
        return json_response({"error": "Task not found"}, 404)

    # Only these fields can change. id and createdAt stay the same.
    for field in UPDATABLE_FIELDS:
        if field in body:
            task[field] = body[field]

    container.replace_item(item=task_id, body=task)
    logging.info("Updated task %s", task_id)

    return json_response(task, 200)