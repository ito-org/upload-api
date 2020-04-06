from flask import url_for
from uuid import uuid4, UUID
from app.persistence.db import DBConnection
import json
from flask.testing import FlaskClient
from flask import Response
from datetime import datetime
import os


def test_insert(client: FlaskClient):
    dbConn = DBConnection(os.environ.get("MONGO_URI"))
    # TODO: actually test that case is inserted
    prev_count: int = dbConn.count_cases()
    n: int = 10
    cases: list = dbConn.generate_random_cases(n)
    res: Response = client.post(
        url_for("v0.cases.report"),
        data=json.dumps([case.__dict__ for case in cases], cls=CaseEncoder),
        content_type="application/json",
    )
    assert res.status_code == 201
    assert dbConn.count_cases() == (prev_count + n)


# copied from https://stackoverflow.com/a/48159596/9926795
class CaseEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)
