import os
import boto3
import jinja2
import logging
import cfnresponse

from botocore.exceptions import ClientError


CONTACT_FLOW = 'contact-flow.template.json'
CONTACT_FLOW_NAME = '0000 BankID Authentication'

AUTH_ARN = os.environ['AUTH_ARN']
INSTANCE_ID = os.environ['INSTANCE_ID']
CONNECT_REGION = os.environ['CONNECT_REGION']

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Supports Amazon Connect Instances from any region
client = boto3.client('connect', region_name=CONNECT_REGION)


def lambda_handler(event, context):
    logger.info('Creating contact flow.')
    logger.info({ 'event': event })

    queue_arn = fetch_sample_basic_queue_arn()
    content = update_template(queue_arn)

    try:
        # Gracefully handle re-deployments
        contact_flow = fetch_contact_flow()
        if contact_flow:
            # Contact Flow was already created
            resp_data = update_contact_flow(content, contact_flow)
        else:
            # Contact Flow does not exist
            resp_data = create_contact_flow(content)

        logger.debug({ 'responseData': resp_data })
        cfnresponse.send(event, context, cfnresponse.SUCCESS, resp_data)

    except ClientError as e:
        error = e.response['Error']
        logger.error({ 'Error': error })
        cfnresponse.send(event, context, cfnresponse.FAILED, error)


def create_contact_flow(content):
    resp = client.create_contact_flow(
        InstanceId=INSTANCE_ID,
        Name=CONTACT_FLOW_NAME,
        Type='CONTACT_FLOW',
        Description='Verifies the callers identity with BankID integration.',
        Content=content
    )

    logger.info('Contact Flow created.')
    return {
        'Arn': resp['ContactFlowArn']
    }

def update_contact_flow(content, contact_flow):
    client.update_contact_flow_content(
        InstanceId=INSTANCE_ID,
        ContactFlowId=contact_flow['Id'],
        Content=content
    )

    logger.info('Contact Flow updated.')
    return {
        'Arn': contact_flow['Arn']
    }


def fetch_sample_basic_queue_arn():
    # All Amazon Connect instances have a Sample Basic Queue
    # This function collects the Arn for the Sample Basic Queue
    # Which will be used in the contact flow to connect the caller
    # to an agent.
    logger.info('Fetching Sample Basic Queue Arn')
    paginator = client.get_paginator('list_queues')
    response_iterator = paginator.paginate(
        InstanceId=INSTANCE_ID,
        QueueTypes=['STANDARD']
    )

    for resp in response_iterator:
        logger.debug({ 'response': resp })
        for i in resp['QueueSummaryList']:
            if i['Name'] == 'Sample BasicQueue':
                logger.info({ 'Arn': i['Arn'] })
                return i['Arn']


def fetch_contact_flow():
    # Gracefully handle duplication errors during re-deployment
    # This function collects the info for the Contact Flow
    # So that the contact flow can be updated instead of created
    logger.info('Fetching Contact Flow ID')
    paginator = client.get_paginator('list_contact_flows')
    response_iterator = paginator.paginate(
        InstanceId=INSTANCE_ID,
        ContactFlowTypes=['CONTACT_FLOW']
    )

    for resp in response_iterator:
        logger.debug({ 'response': resp })
        for i in resp['ContactFlowSummaryList']:
            if i['Name'] == CONTACT_FLOW_NAME:
                logger.info({ 'ContactFlow': i })
                return i


def update_template(queue_arn):
    # The contact flow template needs updated with the account
    # specific ARNs for the Sample Working Queue and Lambda Function
    logger.info('Updating content with account specific Arns.')
    env = jinja2.Environment(loader=jinja2.FileSystemLoader("./"))
    temp = env.get_template(CONTACT_FLOW)

    return temp.render(
        LAMBDA_FUNCTION_ARN=AUTH_ARN,
        SAMPLE_QUEUE_ARN=queue_arn
    )
