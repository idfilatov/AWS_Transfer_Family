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
 create bucket for temporary stack files storing
 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk destroy`     delete this stack and all created infrastructure
 * `cdk docs`        open CDK documentation

## How to use
 * ### What's inside `config.py`
   * `bucket_name` - name of your S3 bucket
   * `class GroupNames` - fixed list of possible groups  
     If you want to add another Group, you should manually add

