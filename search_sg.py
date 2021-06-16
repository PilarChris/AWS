#!/usr/bin/python3

import boto3
import threading
import os
import boto3.session
from botocore.exceptions import ClientError

aws_accounts = ['aws_account1', 'aws_account2', 'aws_account3']

sgs = ['sg-0000000001', 'sg-0000000002', 'sg-0000000003']
counter = 0

for account in aws_accounts:
	session = boto3.session.Session(profile_name=account)
	print('\033[93m' + 'Checking account: ' + session.profile_name + '\033[0m')
	ec2 = session.client('ec2')
	aws_regions = ec2.describe_regions()
	for region in aws_regions['Regions']:
		aws_region_name = region['RegionName']
		ec2 = session.client('ec2', region_name=aws_region_name)
		for sg in sgs:
			try:
			    response = ec2.describe_security_groups(GroupIds=[sg])
			    print('\x1b[6;30;42m' + sg + ' found in ' + session.region_name + ' under ' + session.profile_name + ' account ' + '\x1b[0m')
			    counter = 0
			except Exception as error:
			    counter += 1
			    continue
			finally:
				if len(sgs) == counter:
					print('Security Groups not found in ' + aws_region_name)
					counter = 0
					pass
				else:
					pass
