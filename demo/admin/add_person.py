import json
from demo.sqlalchemy.model import People
from demo.utils import session_scope, json_response
from demo import rds_session


def handler(event, context):
    with session_scope(rds_session) as session:
        body = json.loads(event['body'])
        first_name = body.get('firstname')
        last_name = body.get('lastname')
        person = People(first_name=first_name, last_name=last_name)
        session.add(person)
        session.commit()
        return json_response(200, {"message": "New Person {} {} added.".format(first_name, last_name)})
