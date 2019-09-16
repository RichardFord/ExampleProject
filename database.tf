variable "aws_profile" { }
variable "aws_region" {}
variable "db_master_user" {}
variable "db_master_password" {}
variable "vpc_id" {}

provider "aws" {
  profile    = var.aws_profile
  region     = var.aws_region
}

resource "aws_security_group" "default" {
  name = "example-project-rds-sg-${terraform.workspace}"
  vpc_id = var.vpc_id

  ingress {
    from_port = 3306
    to_port = 3306
    protocol = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port = 0
    to_port = 0
    protocol = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

resource "aws_db_instance" "dbinstance" {
  allocated_storage    = 20
  storage_type         = "gp2"
  engine               = "mysql"
  engine_version       = "5.7"
  instance_class       = "db.t2.micro"
  name                 = "ExampleProject"
  username             = var.db_master_user
  password             = var.db_master_password
  parameter_group_name = "default.mysql5.7"
  iam_database_authentication_enabled = true
  final_snapshot_identifier = false
  publicly_accessible = true
  identifier = "example-project-${terraform.workspace}"
  skip_final_snapshot = true
  vpc_security_group_ids   = [aws_security_group.default.id]
}

resource "aws_ssm_parameter" "InstanceId" {
  name  = "ExampleProjectDbInstanceId-${terraform.workspace}"
  type  = "String"
  value = aws_db_instance.dbinstance.resource_id
  overwrite = true
}

resource "aws_ssm_parameter" "Endpoint" {
  name  = "ExampleProjectDbEndpoint-${terraform.workspace}"
  type  = "String"
  value = aws_db_instance.dbinstance.endpoint
  overwrite = true
}

resource "aws_ssm_parameter" "rds_sg" {
  name  = "ExampleProjectDbSg-${terraform.workspace}"
  type  = "String"
  value = aws_security_group.default.id
  overwrite = true
}