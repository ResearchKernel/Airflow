import boto3

ec2 = boto3.client('ec2')
volume = ec2.Volume('id')
response = ec2.attach_volume(
    Device='/dev/sdf',
    InstanceId='string',
    VolumeId='string',
    DryRun=True | False
)
