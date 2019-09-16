from demo.queries.library import sqlalchemy_query
from demo.utils import session_scope, json_response
from demo import rds_session


def handler(event, context):
    with session_scope(rds_session) as session:
        query = sqlalchemy_query(session)
        return json_response(200, {"people": [person.response for person in query]})
