import sys
import time
import boto3
# Takes the first argument after the script name
input_arg = sys.argv[1]
print(f"Received argument: {input_arg}")
time.sleep(30)
print("after sleep")
