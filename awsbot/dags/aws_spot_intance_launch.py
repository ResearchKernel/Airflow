import boto3
from datetime import datetime, timedelta
from tzlocal import get_localzone
from pytz import utc
import uuid
import argparse
import logging

FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.WARNING, format=FORMAT)
logger = logging.getLogger(__name__)


now_utc = datetime.now(get_localzone()).astimezone(utc)
valid_from = now_utc + timedelta(days=14)
valid_to = valid_from + timedelta(seconds=1)

client = boto3.client('ec2')

def launch_spot(client, SecurityGroups, SpotPrice, InstanceCount, Type, SecurityGroupIds, ImageId, InstanceType, SubnetId, KeyName, SnapshotId, VolumeSize, UserData):
    client = client
    response = client.request_spot_instances(
        SpotPrice=SpotPrice,
        InstanceCount=InstanceCount,
        Type=Type,
        ValidFrom=valid_from,
        ValidUntil=valid_to,
        LaunchSpecification={
            "SecurityGroupsIds": [
                SecurityGroupIds
            ],
            "SecurityGroups": [
                SecurityGroups
            ],
            "ImageId": ImageId,
            "InstanceType": InstanceType,
            "SubnetId": SubnetId,
            "KeyName": KeyName,
            "EbsOptimized": True,
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/sda1",
                    "Ebs": {
                        "DeleteOnTermination": True,
                        "VolumeType": "gp2",
                        "VolumeSize": VolumeSize,
                        "SnapshotId": SnapshotId
                    }
                }
            ],

            
            "UserData": UserData
        }
    )
    return response

request = launch_spot()


