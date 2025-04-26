#!/bin/bash

# Variables
STACK_NAME=$1  # Your stack name
TEMPLATE_FILE=$2 # Path to your CloudFormation template
AWS_PROFILE=$3 # Your AWS profile
PARAMETERS=$4 # ECR-repository-url

if [ -n "$4" ]; then
    PARAMETERS="ParameterKey=ECRRepositoryURL,ParameterValue=$4"
else
    PARAMETERS=""
fi

# Check if the stack exists
stack_status=$(aws cloudformation describe-stacks --stack-name $STACK_NAME --query "Stacks[0].StackStatus" --output text --profile $AWS_PROFILE 2>/dev/null)

if [[ $? -eq 0 ]]; then
    echo "Stack exists with status: $stack_status"

    if [[ "$stack_status" == "ROLLBACK_COMPLETE" || "$stack_status" == "ROLLBACK_FAILED" ]]; then
        echo "Deleting failed stack..."
        aws cloudformation delete-stack --stack-name $STACK_NAME --profile $AWS_PROFILE
        echo "Waiting for stack deletion to complete..."
        aws cloudformation wait stack-delete-complete --stack-name $STACK_NAME --profile $AWS_PROFILE
        echo "Deleted failed stack. Creating new stack..."
        aws cloudformation create-stack --stack-name $STACK_NAME --template-body file://$TEMPLATE_FILE --profile $AWS_PROFILE --parameters $PARAMETERS --capabilities CAPABILITY_NAMED_IAM
    else
        echo "Updating stack..."
        aws cloudformation update-stack --stack-name $STACK_NAME --template-body file://$TEMPLATE_FILE --profile $AWS_PROFILE  --parameters $PARAMETERS --capabilities CAPABILITY_NAMED_IAM
        echo "Waiting for stack update to complete..."
        aws cloudformation wait stack-update-complete --stack-name $STACK_NAME --profile $AWS_PROFILE
    fi
else
    echo "Stack does not exist. Creating stack..."
    aws cloudformation create-stack --stack-name $STACK_NAME --template-body file://$TEMPLATE_FILE --profile $AWS_PROFILE --region us-east-1  --parameters $PARAMETERS --capabilities CAPABILITY_NAMED_IAM
    echo "Waiting for stack creation to complete..."
    aws cloudformation wait stack-create-complete --stack-name $STACK_NAME --profile $AWS_PROFILE
fi

echo "Operation complete."
