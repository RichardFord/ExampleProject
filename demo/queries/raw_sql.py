from demo.queries.library import raw_query
from demo.utils import session_scope, json_response
from demo import rds_session


def handler(event, context):
    with session_scope(rds_session) as session:
        results = raw_query(session)
        return json_response(200, {
            "people": [{"id": person[0], "first_name": person[1], "last_name": person[2]} for person in results]
        })
