#!/usr/bin/python3
# This is small script to check replication status of secret in AWS Secrets Manager
# just run it with argument of desired account according to your configured profiles in aws credentials

import boto3
import sys

if len(sys.argv) != 2:
    print("Please provide an argument with a proper account configured in AWS Credentials")
    sys.exit(1)

account = sys.argv[1]
session = boto3.session.Session(profile_name=account)
sm_client = session.client('secretsmanager')

secrets = sm_client.get_paginator(
    'list_secrets').paginate().build_full_result().get('SecretList')
secret_arns = [secret['ARN'] for secret in secrets]

for arn in secret_arns:
    secret_info = sm_client.describe_secret(
        SecretId=arn
    )
    if 'ReplicationStatus' in secret_info:
        for status in secret_info['ReplicationStatus']:
            if status['Status'] != 'InSync':
                print(
                    'Secret ' + secret_info['Name'] + " " + secret_info['ARN'] + ' in ' + status['Region'] + ' has status ' + status['Status'])
