#!/usr/bin/python3

import boto3
import threading
import os
import boto3.session
import argparse
from botocore.exceptions import ClientError

aws_accounts = ['aws_account1', 'aws_account2', 'aws_account3']

cleaup_candidates = []
all_groups = []
groups_in_use = []
default_sgs = []
validated_for_delete = []

for account in aws_accounts:
	session = boto3.session.Session(profile_name=account)
	print('\033[93m' + 'Checking account: ' + session.profile_name + '\033[0m')
	ec2 = session.client('ec2')
	aws_regions = ec2.describe_regions()
	for region in aws_regions['Regions']:
		aws_region_name = region['RegionName']
		ec2 = session.client('ec2', region_name=aws_region_name)
		elb = session.client('elb', region_name=aws_region_name)
		alb = session.client('elbv2', region_name=aws_region_name)
		rds = session.client('rds', region_name=aws_region_name)
		security_groups_dict = ec2.describe_security_groups()
		security_groups = security_groups_dict['SecurityGroups']
		#security groups used by ec2
		instances_dict = ec2.describe_instances()
		reservations = instances_dict['Reservations']
		network_interface_count = 0
		for i in reservations:
			for j in i['Instances']:
				for k in j['SecurityGroups']:
					if k['GroupId'] not in groups_in_use:
						groups_in_use.append(k['GroupId'])
		#security groups used by network interfaces
		eni_dict = ec2.describe_network_interfaces()
		for i in eni_dict['NetworkInterfaces']:
			for j in i['Groups']:
				if j['GroupId'] not in groups_in_use:
					groups_in_use.append(j['GroupId'])
		#secuirty groups used by ELB
		elb_dict = elb.describe_load_balancers()
		for i in elb_dict['LoadBalancerDescriptions']:
			for j in i['SecurityGroups']:
				if j not in groups_in_use:
					groups_in_use.append(j)
		#security groups used ny ALB
		alb_dict = alb.describe_load_balancers()
		for i in alb_dict['LoadBalancers']:
			if i['Type']=='network':
				continue
			for j in i['SecurityGroups']:
				if j not in groups_in_use:
					groups_in_use.append(j)
		#security groups used by RDS
		rds_dict = rds.describe_db_instances()
		for i in rds_dict['DBInstances']:
			for j in i['VpcSecurityGroups']:
				if j['VpcSecurityGroupId'] not in groups_in_use:
					groups_in_use.append(j['VpcSecurityGroupId'])
		for sg in security_groups:
			all_groups.append(sg['GroupId'])
			try:
				if sg['GroupName'] == 'default':
					print('\x1b[6;30;42m' + 'found ' + sg['GroupId'] + ' named default in ' + aws_region_name + '\x1b[0m')
					default_sgs.append(sg['GroupId'])
					#groups_in_use.append(sg['GroupId'])
					continue
				else:
					continue
			except:
					continue

for a in default_sgs:
	if a not in groups_in_use:
		validated_for_delete.append(a)
	else:
		print('\033[31m' + a + ' is in use !!' + '\033[0m')
for checked in validated_for_delete:
	print('\033[92m' + checked + ' looks safe to remove' + '\033[0m')
