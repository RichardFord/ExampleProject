### A simple serverless project including:

* Terraform for throwing together a database and associated parameterstore values for reference.
* Basic SQL Alchemy model
* SQL Alchemy & Raw queries for SQL challenge
* Token based authentication for AWS RDS
* Simple request validation schema checking for required properties, alpha characters only and name lengths (max 32, min 1)
* SQL for enabling RDS token based authentication and enforcement of SSL
* IAM role for RDS token access for lambda
* Script for building deployment package which hooks into serverless.yml

Couple of things worth noting

* Opted for non VPC design purely because it saves me the hassle of either setting up VPC endpoints or NAT Gateway for AWS service access.
* Never ever in a million years want to store credentials as ENV vars, so AWS services 100% required.
* Draw back is that you have an exposed database on clear net, not always possible/desirable depending on project requirements, but ok if exclusively token based auth.
* VPC based lambda entails container startup penalty which we don't have in this case, just the initial RDS token access ~150-200ms.
* Draw back with RDS token authentication is the limit of 250 requests per second, even worse for SSM at 100.
* Best option is of course secrets manager which can handle 1000 requests/sec and AWS will up the limit if you ask
* In the real world I'd never build a deployment containing all 3rd party libraries as with lots of func's you soon eat into the 76GB storage limit with multiple services and 100's of endpoints, makes deployment times slow too
* Would always use layers to bundle up shared libraries which can become part of an independent CI/CD pipeline.
* Would never in the real world pull SSL certs at container startup, would bundle that into a layer. 

Obviously this is really stripped down project with no authentication integration, logging, x-ray tracing, strategy for keeping containers warm, etc etc but seems like a decent way creating something that in essence touches on all of my skillsets in some small way.

### Endpoints

* GET - https://XXX.execute-api.eu-west-2.amazonaws.com/dev/queries/listPeople (json output all of People in the People table)
* GET - https://XXX.execute-api.eu-west-2.amazonaws.com/dev/queries/raw (SQL challenge result using raw SQL)
* GET - https://XXX.execute-api.eu-west-2.amazonaws.com/dev/queries/sqlalchemy (SQL challenge result using SQL Alchemy ORM)
* POST - https://XXX.execute-api.eu-west-2.amazonaws.com/dev/addPerson (Add a new person to validate SQL challenge)
* GET - https://XXX.execute-api.eu-west-2.amazonaws.com/dev/admin/reset (Wipes the People table and re-populates with base datat)

### Add Person curl command

This will work on Mac and Linux. Can't help you with Windows unfortunately!

```
curl --header "Content-Type: application/json" \
  --request POST \
  --data '{"firstname":"John","lastname":"Smith"}' \
  https://XXX.execute-api.eu-west-2.amazonaws.com/dev/addPerson | json_pp
```

