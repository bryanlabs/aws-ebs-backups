import boto3
import os
import collections
import datetime

DefaultBackupRetentionDays = int(os.environ.get("DefaultBackupRetentionDays"))

ec = boto3.client('ec2')


def lambda_handler(event, context):
    """lambda_handler will execute the function in AWS Lambda."""
    reservations = ec.describe_instances(
    ).get(
        'Reservations', []
    )

    allinstances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])
    print(f"Found {len(allinstances)} to consider for backing up")

    backup_instances = []
    to_tag = collections.defaultdict(list)
    for instance in allinstances:

        tags = instance["Tags"]
        backups = [tag.get('Value') for tag in tags if tag.get('Key') == 'Backup']
        backup = backups[0] if backups else None
        if backup != 'False':
            backup_instances.append(instance)

    for instance in backup_instances:
        print(f"Backin up {instance['InstanceId']}")

        try:
            retention_days = [
                int(t.get('Value')) for t in instance['Tags']
                if t['Key'] == 'Retention'][0]
        except IndexError:
            retention_days = DefaultBackupRetentionDays

        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None:
                continue
            vol_id = dev['Ebs']['VolumeId']
            print(f"Found EBS Volume {vol_id} on instance {instance['InstanceId']}")

            snap = ec.create_snapshot(
                Description='Created By ebs-backups-SnapshotCreationFunction',
                VolumeId=vol_id,
            )

            to_tag[retention_days].append(snap['SnapshotId'])

            print(f"Retaining snapshot {snap['SnapshotId']} of volume {vol_id }from instance {instance['InstanceId']} for {retention_days} days")

    for retention_days in list(to_tag.keys()):
        delete_date = datetime.date.today() + datetime.timedelta(days=retention_days)
        delete_fmt = delete_date.strftime('%Y-%m-%d')
        print(f"Will delete {len(to_tag[retention_days])} snapshots on {delete_fmt}")
        ec.create_tags(
            Resources=to_tag[retention_days],
            Tags=[
                {'Key': 'DeleteOn', 'Value': delete_fmt},
                {'Key': 'CreatedBy', 'Value': 'ebs-backups-SnapshotCreationFunction'},
            ]
        )


if __name__ == '__main__':
    lambda_handler(None, None)
