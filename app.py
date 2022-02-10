from aws_cdk import core

from aws_transfer_family.aws_transfer_family_stack import AwsTransferFamilyStack


app = core.App()
AwsTransferFamilyStack(app, "AwsTransferFamilyStack")

app.synth()
