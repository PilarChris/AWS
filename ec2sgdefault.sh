
#!/bin/bash

for region in `aws ec2 describe-regions --query 'Regions[*].RegionName' --output text`
do
	echo "\n '$region':"
	aws --region $region ec2 describe-instances --filters Name=instance.group-name,Values=default --query 'Reservations[*].Instances[*].[InstanceId]' --output text
done
