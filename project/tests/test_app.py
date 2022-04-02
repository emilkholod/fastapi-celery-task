import json


def test_route_tasks(test_app):
    response = test_app.get("/tasks")
    assert response.status_code == 200


def test_route_get_task(test_app):
    response = test_app.get("/tasks/123")
    assert response.status_code == 404


def test_route_create_task(test_app):
    response = test_app.post("/tasks/create", data=json.dumps({"args": [1, 2, 3]}))
    assert response.status_code == 201
    content = response.json()
    task_id = content["task_id"]
    assert task_id

    response = test_app.get("tasks/{}".format(task_id))
    content = response.json()
    assert content == {"id": task_id, "status": "PENDING", "result": None}
    assert response.status_code == 200

    while content["status"] == "PENDING":
        response = test_app.get("tasks/{}".format(task_id))
        content = response.json()
    assert content["id"] == task_id
    assert content["status"] == "SUCCESS"
    assert content["result"]["task_result"] == 6
    assert content["result"]["finished_time"] is not False