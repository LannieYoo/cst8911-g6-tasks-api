import json
import logging

import azure.functions as func

from shared.cosmos import get_container

bp = func.Blueprint()


def json_response(data, status_code):
    return func.HttpResponse(
        json.dumps(data),
        status_code=status_code,
        mimetype="application/json",
    )


@bp.route(route="tasks", methods=["GET"], auth_level=func.AuthLevel.FUNCTION)
def get_tasks(req: func.HttpRequest) -> func.HttpResponse:
    """GET /api/tasks - list all tasks, or only one status with ?status=."""
    logging.info("GET /api/tasks")

    status = req.params.get("status")

    # Only our own fields, so Cosmos DB system fields (_rid, _etag, ...) are not returned.
    query = "SELECT c.id, c.title, c.status, c.owner, c.createdAt FROM c"
    parameters = []
    if status:
        # A parameter, not string formatting, so the input cannot change the query.
        query += " WHERE c.status = @status"
        parameters.append({"name": "@status", "value": status})
    query += " ORDER BY c.createdAt"

    container = get_container()
    tasks = list(
        container.query_items(
            query=query,
            parameters=parameters,
            enable_cross_partition_query=True,
        )
    )
    logging.info("Found %d tasks", len(tasks))

    return json_response(tasks, 200)
