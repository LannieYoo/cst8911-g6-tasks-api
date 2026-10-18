import json
import logging

import azure.functions as func
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from shared.cosmos import get_container

bp = func.Blueprint()


@bp.route(route="tasks/{id}", methods=["DELETE"], auth_level=func.AuthLevel.FUNCTION)
def delete_task(req: func.HttpRequest) -> func.HttpResponse:
    """DELETE /api/tasks/{id} - delete one task."""
    task_id = req.route_params.get("id")
    logging.info("DELETE /api/tasks/%s", task_id)

    container = get_container()
    try:
        # Partition key is /id, so the partition key value is the id itself
        container.delete_item(item=task_id, partition_key=task_id)
    except CosmosResourceNotFoundError:
        return func.HttpResponse(
            json.dumps({"error": "Task not found"}),
            status_code=404,
            mimetype="application/json",
        )

    logging.info("Deleted task %s", task_id)
    return func.HttpResponse(status_code=204)
