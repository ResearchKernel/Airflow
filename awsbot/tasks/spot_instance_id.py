import subprocess
# import os
# command = "aws ec2 describe-instances --filters Name=instance-lifecycle,Values=spot --query 'Reservations[*].Instances[*].[InstanceId]'"
# respose = os.system(command)
# print("ID is:", respose)

import boto3

client = boto3.client('ec2')

custom_filter = [{
    'Name': 'instance-lifecycle',
    'Values': ['spot']}]

response = client.describe_instances(Filters=custom_filter)
print(response)
print(response["Reservations"][0]["Instances"][0]["InstanceId"])
