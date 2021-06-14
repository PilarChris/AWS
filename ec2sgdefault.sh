#!/bin/bash

for region in `aws ec2 describe-regions --query 'Regions[*].RegionName' --output text`
do
	ec2names=$(aws --region $region ec2 describe-instances --filters Name=instance.group-name,Values=default --query 'Reservations[*].Instances[*].[Tags[?Key == `name`].Value,Tags[?Key == `Name`].Value]' --output text)
	[  -z "$ec2names" ] && : || printf "$region: \n$ec2names\n"| uniq
done
