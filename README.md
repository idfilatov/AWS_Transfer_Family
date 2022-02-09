# Cool name
## Cool descriptions what it does
## Before you start

Requirements for working with AWS CDK:

 * AWS CLI
 * Node.js 14.x
 * python 3

Install CDK with command
```
npm install -g aws-cdk
```

In the root project directory:
 * Create virtual python enviroment
   ```
   > python -m venv .venv
   ```
 * Activate envoroment
   ```
   > source .venv/bin/activate
   ```
 * Install enviroment dependencies
   ```
   > pip install -r requirements.txt
   ```


To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands
**Don't forget set up AWS Credentials and preferred region**


 * `cdk bootstrap aws://account_id/region` **(use only before first deploy in region)**  
 It creates bucket for temporary stack files storing
 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk destroy`     delete this stack and all created infrastructure
 * `cdk docs`        open CDK documentation

## How to use
 * ### What's inside [config.py](aws_transfer_family/config.py) :
   * `bucket_name` - name of your S3 bucket
   * `class GroupNames` - fixed list of possible groups
   * `members` - description of storage clients
     

 * ### If you want to add another `NewGroup` :
   * Add new record into `class GroupNames`
   * If necessary, define new IAM Policy Statements in [policy_statements.py](aws_transfer_family/policy_statements.py)
   * Add creation of new IAM Role for this `NewGroup` ([like this](https://github.com/Wag-ON/AWS_Transfer_Family/blob/9e528cfef5d791d9e0318e59a0bc2c9b937c990c/aws_transfer_family/aws_transfer_family_stack.py#L52))

