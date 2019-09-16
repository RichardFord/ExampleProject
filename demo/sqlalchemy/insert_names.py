from demo.sqlalchemy.model import People


def insert_names(session):
    names = [
        People(first_name='Greg', last_name='Evans'),
        People(first_name='Sally', last_name='Evans'),
        People(first_name='Michael', last_name='Smith'),
        People(first_name='Sarah', last_name='Johnson'),
        People(first_name='Simon', last_name='Johnson'),
        People(first_name='Kate', last_name='Barton'),
        People(first_name='John', last_name='Cooper'),
    ]
    for row in names:
        session.add(row)
    session.commit()
