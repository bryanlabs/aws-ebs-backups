import boto3
import datetime

ec = boto3.client('ec2')


def lambda_handler(event, context):
    """lambda_handler will execute the function in AWS Lambda."""
    account_id = context.invoked_function_arn.split(":")[4]
    account_ids = [account_id]

    delete_on = datetime.date.today().strftime('%Y-%m-%d')
    filters = [
        {'Name': 'tag-key', 'Values': ['DeleteOn']},
        {'Name': 'tag-value', 'Values': [delete_on]},
    ]
    snapshot_response = ec.describe_snapshots(OwnerIds=account_ids, Filters=filters)

    for snap in snapshot_response['Snapshots']:
        print(f"Deleting snapshot {snap['SnapshotId']}.")
        ec.delete_snapshot(SnapshotId=snap['SnapshotId'])


if __name__ == '__main__':
    lambda_handler(None, None)
