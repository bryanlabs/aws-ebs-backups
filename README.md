# ebs-backups for EC2

# HOW IT WORKS  

### Deploy the Cloudformation, and all EC2 instances will be backed up.  

[![Launch Stack](https://cdn.rawgit.com/buildkite/cloudformation-launch-stack-button-svg/master/launch-stack.svg)](https://console.aws.amazon.com/cloudformation/home#/stacks/new?stackName=ebs-backups&templateURL=https://bryanlabs-public.s3.amazonaws.com/bryanlabs.net_files/blog/ebs-backups/ebs-backups.yml)  
[View Source](https://github.com/bryanlabs/aws-ebs-backups/blob/master/ebs-backups.yml)

### Opting Out

The default behavior is to backup all instances. To exclude an instance from being backed up, add the following tag to the instance.

```shell
aws ec2 create-tags \
    --resources i-1234567890abcdef0 --tags Key=Backup,Value=False
```

### Changing Default Retention
The default behavior is to retain backups for 14 days. To change the default behavior, update the CFT parameter with a new value.
To change the individual behavior of a single instance add the following tag.

```shell
aws ec2 create-tags \
    --resources i-1234567890abcdef0 --tags Key=Retention,Value=3
```
