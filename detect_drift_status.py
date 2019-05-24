import boto3
import sys
import time
from prettytable import PrettyTable



client = boto3.client('cloudformation')
stack_status_table = PrettyTable()
stack_status_table.field_names = ["Stack Name", "Drift Status"]
# statuses = ['ROLLBACK_COMPLETE', 'CREATE_COMPLETE', 'UPDATE_COMPLETE', 'UPDATE_ROLLBACK_COMPLETE']
statuses = ['UPDATE_ROLLBACK_COMPLETE']



def detect_stack_drift():
    global detection_id
    detection_id  = client.detect_stack_drift( StackName = stack )
    time.sleep(5)

def describe_stack_drift_detection_status():
    global detection_status
    detection_status = client.describe_stack_drift_detection_status(
        StackDriftDetectionId = detection_id['StackDriftDetectionId']
    )
    time.sleep(5)

def print_table_output_into_file():
    table_index = stack_status_table.get_string()
    with open('drift_status_report.txt','w') as file:
        file.write(table_index)

def ___init___():
    global stack
    paginator = client.get_paginator('list_stacks')
    iterator = paginator.paginate(StackStatusFilter=statuses)
    for page in iterator:
        stack = page['StackSummaries']
        for output in stack:
            # print output['StackName']
            stack = output['StackName']
            detect_stack_drift()
            describe_stack_drift_detection_status()
            while True:
                if detection_status['DetectionStatus'] == 'DETECTION_IN_PROGRESS':
                    describe_stack_drift_detection_status()
                else:
                    stack_status_table.add_row([stack, detection_status['StackDriftStatus']])
                    print ('Status Check is COMPLETED: ' + '"'+ stack + '"' )
                    break





print ('Drift status check for all stacks has been STARTED...' + '\r\n')
___init___()
print_table_output_into_file()
print ('\r\n' + 'Drift status check has been COMPLETED successfully  !!!')
print ('\r\n' + 'Generating report...' + '\r\n')
print (stack_status_table)
print ('\r\n' + 'The report has been generated succesfully !')