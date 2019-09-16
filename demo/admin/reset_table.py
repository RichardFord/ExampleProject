from demo.sqlalchemy.model import Base, People
from demo.sqlalchemy.insert_names import insert_names
from demo.utils import session_scope, json_response
from demo import engine, rds_session


def handler(event, context):
    with session_scope(rds_session) as session:
        if not engine.dialect.has_table(engine, 'people'):
            Base.metadata.create_all(engine)
            message = 'Table created'
        else:
            session.query(People).delete()
            message = 'Table reset'
        insert_names(session)
        session.commit()
        return json_response(200, {"message": message})
