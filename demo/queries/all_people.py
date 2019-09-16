from demo.sqlalchemy.model import People
from demo.utils import session_scope, json_response
from demo import rds_session


def handler(event, context):
    with session_scope(rds_session) as session:
        people = session.query(People).all()
        return json_response(200, {"people": [person.response for person in people]})
