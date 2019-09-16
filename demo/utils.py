import json
from contextlib import contextmanager


@contextmanager
def session_scope(session):
    try:
        yield session
    except:
        session.rollback()
        raise
    finally:
        session.close()


def json_response(code, payload):
    return {
        "statusCode": code,
        "headers": {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Credentials': True
        },
        "body": json.dumps(payload)
    }
