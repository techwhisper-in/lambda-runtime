import sys
import time
import boto3
def lambda_access(role_arn,reg): # get_tags_all function define
    rolearn=role_arn
    acc_id=str(role_arn.split(":")[4])
    awsaccount = sts.assume_role(
        RoleArn=rolearn,
        RoleSessionName='Account_Session'+acc_id
    )
    access_key = awsaccount['Credentials']['AccessKeyId']
    secret_key = awsaccount['Credentials']['SecretAccessKey']
    session_token = awsaccount['Credentials']['SessionToken']
    function = boto3.client('lambda',aws_access_key_id=access_key, aws_secret_access_key=secret_key, aws_session_token=session_token, region_name=reg)
    return function
def change_runtime_all(function):
    print("Changing Lambda Runtime: ")
    paginator = function.get_paginator('list_functions')
    for page in paginator.paginate():
        for j in range(len(page['Functions'])):
            y=str(page['Functions'][j]['FunctionName'])
            arn=str(page['Functions'][j]['FunctionArn'])
            try:
                response = function.list_tags(Resource=arn)
            except Exception as e:
                print(e)
                time.sleep(0.3)
                response = function.list_tags(Resource=arn)
            print(response)
def change_runtime(function,i):
    print(f"Changing Lambda Runtime: {i}")
    response = function.list_tags(Resource=i)
    print(response)

if __name__=="__main__":
    sts=boto3.client('sts')
    # Takes the first argument after the script name
    role_arn=sys.argv[1]
    reg=sys.argv[2]
    lambda_function=sys.argv[3]
    print(f"{role_arn}\n{reg}\n{lambda_function}")
    #time.sleep(30)
    print("after sleep")
    account_access=lambda_access(role_arn,reg)
    lambda_function_list=lambda_function.split(",")
    if len(lambda_function_list)==1 and str(lambda_function_list[0]).upper()=='ALL':
        change_runtime_all(account_access)
    for i in lambda_function_list:
        if i.upper()!='ALL':
            print("\n")
            change_runtime(account_access,i)
                





        
