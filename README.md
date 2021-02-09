# AWS

#### AWS CLI stuff

- `aws ec2 describe-availability-zones --region ap-northeast-1` = check available AZ's in region
- `aws ec2 describe-availability-zones --region us-east-1 --query "sort_by(AvailabilityZones, &ZoneId)[].{RegionName:RegionName,ZoneName:ZoneName,ZoneId:ZoneId}" --output table --color off` = check available AZ's in region with clearer output
- `aws service-quotas list-service-quotas --service-code vpc` = list available quota
- `aws service-quotas get-service-quota --service-code vpc --quota-code L-0FFFFFFF` = get service quota
