CREATE USER 'lambdaUser' IDENTIFIED WITH AWSAuthenticationPlugin as 'RDS';
GRANT ALL PRIVILEGES ON ExampleProject.* TO 'lambdaUser'@'%' REQUIRE SSL;
FLUSH PRIVILEGES;