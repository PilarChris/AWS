#!/bin/bash
#set -x
domain=""
sgsubdomain=""
profile="$1"
declare -a efsMtdelete
declare -a efsDelete
declare -a sgDelete
for ns in namespace1 namespace2 namespace3
do
  efsids=$(aws --profile="$profile" efs describe-file-systems --query 'FileSystems[?Name==`'$ns$domain'`].FileSystemId[]' --output text)
  if [ -z "$efsids" ]
  then
    printf "not found\n" 
  else 
    printf "$efsids\n" && efsDelete+="$efsids "
    efsmtids=$(aws --profile="$profile" efs describe-mount-targets --file-system-id "$efsids" --query 'MountTargets[*].MountTargetId[]' --output text)
    efsMtdelete+="$efsmtids "
    sgids=$(aws --profile=$profile  ec2 describe-security-groups --filters "Name=group-name,Values='$ns$sgsubdomain'" --query "SecurityGroups[*].GroupId[]" --output text)
    sgDelete+="$sgids "
  fi
done
#printf ${efsMtdelete[*]}

for mt in ${efsMtdelete[*]}
do
  deletemt=$(aws --profile="$profile" efs delete-mount-target --mount-target-id "$mt")
done

printf "giving some time for mount target deletion..."
sleep 20;

for id in ${efsDelete[*]}
do
  deleteefs=$(aws --profile="$profile" efs delete-file-system --file-system-id "$id")
done

for sgid in ${sgDelete[*]}
do
  deletesg=$(aws --profile="$profile" ec2 delete-security-group --group-id $sgid)
done



