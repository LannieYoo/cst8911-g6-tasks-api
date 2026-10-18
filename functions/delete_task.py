import json
import logging
from http import HTTPStatus

import azure.functions as func
from azure.cosmos.exceptions import CosmosResourceNotFoundError

from shared.cosmos import get_container

bp = func.Blueprint()
logger = logging.getLogger(__name__)


@bp.route(route="tasks/{id}", methods=["DELETE"], auth_level=func.AuthLevel.FUNCTION)
def delete_task(req: func.HttpRequest) -> func.HttpResponse:
    """Remove a task, which returns 204 on success or 404 if it does not exist."""
    task_id = req.route_params.get("id")
    if not task_id:
        return func.HttpResponse(
            body=json.dumps({"error": "Task id is required"}),
            status_code=HTTPStatus.BAD_REQUEST,
            mimetype="application/json",
        )

    container = get_container()
    try:
        # The container uses /id as its partition key. No preliminary read is needed.
        container.delete_item(item=task_id, partition_key=task_id)
    except CosmosResourceNotFoundError:
        logger.info("Task %s was not found for deletion", task_id)
        return func.HttpResponse(
            body=json.dumps({"error": "Task not found"}),
            status_code=HTTPStatus.NOT_FOUND,
            mimetype="application/json",
        )

    logger.info("Task %s deleted", task_id)
    return func.HttpResponse(status_code=HTTPStatus.NO_CONTENT)
