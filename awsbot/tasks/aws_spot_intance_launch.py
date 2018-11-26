import boto3
from datetime import datetime, timedelta
from tzlocal import get_localzone
from pytz import utc
import uuid
import argparse
import logging

'''
Logger
'''
FORMAT = "[%(levelname)s %(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
logging.basicConfig(level=logging.WARNING, format=FORMAT)
logger = logging.getLogger(__name__)

# Time Duration for EC2
now_utc = datetime.now(get_localzone()).astimezone(utc)
valid_from = now_utc + timedelta(days=14)
valid_to = valid_from + timedelta(seconds=1)

#Boto3 client 
client = boto3.client('ec2')
SpotPrice = "0.0052"
InstanceCount = 1
ImageId = "ami-97785bed"
InstanceType = "t2.micro"
SubnetId = "subnet-c8202695"
KeyName = "developement-fullstack"
SnapshotId = "snap-0fae6f7252388fc12"
VolumeSize = 8


def launch_spot(client, SpotPrice, InstanceCount, ImageId, InstanceType, SubnetId, KeyName, SnapshotId, VolumeSize):
    client = client
    response = client.request_spot_instances(
        SpotPrice=SpotPrice,
        InstanceCount=InstanceCount,
        ValidFrom=valid_from,
        ValidUntil=valid_to,
        LaunchSpecification={
            "ImageId": ImageId,
            "InstanceType": InstanceType,
            "SubnetId": SubnetId,
            "KeyName": KeyName,
            "BlockDeviceMappings": [
                {
                    "DeviceName": "/dev/xvda",
                    "Ebs": {
                        "DeleteOnTermination": True,
                        "VolumeType": "gp2",
                        "VolumeSize": VolumeSize,
                        "SnapshotId": SnapshotId
                    }
                }
            ],    
        },
    )
    return response


request = launch_spot(client, SpotPrice, InstanceCount,ImageId, InstanceType, SubnetId, KeyName, SnapshotId, VolumeSize)

print(request)