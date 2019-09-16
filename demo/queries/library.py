from sqlalchemy import func
from demo.sqlalchemy.model import People


def raw_query(session):
    stmt = """
    select * from people
    where last_name in (
        select last_name
        from people
        group by last_name
        having count(*) > 1
    )
     """
    return session.execute(stmt)


def sqlalchemy_query(session):
    count_query = session.query(People.last_name) \
                         .having(func.count(People.last_name) > 1) \
                         .group_by(People.last_name) \
                         .as_scalar()

    return session.query(People) \
                  .filter(People.last_name.in_(count_query)) \
                  .all()
