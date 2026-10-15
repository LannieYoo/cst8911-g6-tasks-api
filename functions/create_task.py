import json
import logging
import uuid
from datetime import datetime, timezone

import azure.functions as func

from shared.cosmos import get_container

bp = func.Blueprint()

VALID_STATUS = ["todo", "doing", "done"]


def json_response(data, status_code):
    return func.HttpResponse(
        json.dumps(data),
        status_code=status_code,
        mimetype="application/json",
    )


@bp.route(route="tasks", methods=["POST"], auth_level=func.AuthLevel.FUNCTION)
def create_task(req: func.HttpRequest) -> func.HttpResponse:
    """POST /api/tasks - create one task."""
    logging.info("POST /api/tasks")

    try:
        body = req.get_json()
    except ValueError:
        return json_response({"error": "Request body must be JSON"}, 400)

    title = body.get("title")
    owner = body.get("owner")
    status = body.get("status", "todo")

    if not title or not owner:
        return json_response({"error": "title and owner are required"}, 400)
    if status not in VALID_STATUS:
        return json_response({"error": "status must be todo, doing or done"}, 400)

    task = {
        "id": str(uuid.uuid4()),
        "title": title,
        "status": status,
        "owner": owner,
        "createdAt": datetime.now(timezone.utc).isoformat(),
    }

    container = get_container()
    container.create_item(task)
    logging.info("Created task %s", task["id"])

    return json_response(task, 201)
