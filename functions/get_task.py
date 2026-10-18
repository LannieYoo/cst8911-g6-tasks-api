import json
import logging

import azure.functions as func
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from shared.cosmos import get_container

bp = func.Blueprint()


def json_response(data, status_code):
    return func.HttpResponse(
        json.dumps(data),
        status_code=status_code,
        mimetype="application/json",
    )


@bp.route(route="tasks/{id}", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
def get_task(req: func.HttpRequest) -> func.HttpResponse:
    """GET /api/tasks/{id} - return one task."""
    task_id = req.route_params.get("id")
    logging.info("GET /api/tasks/%s", task_id)

    container = get_container()
    try:
        # Partition key is /id, so the partition key value is the id itself
        task = container.read_item(item=task_id, partition_key=task_id)
    except CosmosResourceNotFoundError:
        return json_response({"error": "Task not found"}, 404)

    return json_response(task, 200)