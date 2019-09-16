import os
from urllib.request import urlretrieve
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

if not os.environ.get('UNIT_TEST', False):

    db_host, port = os.environ.get('RDS_ENDPOINT').split(":")
    db_user = os.environ.get('DB_USER')
    region = os.environ.get('AWS_REGION')
    database_name = os.environ.get('DATABASE_NAME')

    rds = boto3.client('rds')
    db_password_token = rds.generate_db_auth_token(db_host, port, db_user, Region=region)

    """
    In the real world we'd store certs in layer to ensure consistency across services and mitigate avoidable container
    startup penalty times, s3 connectivity issues, etc.
    """

    cert_url = 'https://s3.amazonaws.com/rds-downloads/rds-combined-ca-bundle.pem'
    cert_path = '/tmp/rds-combined-ca-bundle.pem'
    urlretrieve(cert_url, cert_path)

    connect_args = {
        'user': db_user,
        'password': db_password_token,
        'host': db_host,
        'database': database_name,
        'charset': 'utf8',
        'ssl_ca': cert_path
    }

    rds_uri = "mysql+mysqlconnector://{user}:{password}@{db_host}/{database}"
    engine = create_engine(rds_uri, connect_args=connect_args)
    rds_session = Session(bind=engine)
