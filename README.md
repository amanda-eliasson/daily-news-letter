# Daily Newsletter

## Deploy email sender
### Prerequsisite 
AWS account setup and AWS cli installed
#### Environment variables
- `AWS_ACCOUNT_NBR`=Your aws account id
- `AWS_PROFILE`=Your aws profile name

## Deploy
2. `cd infra` && `./create-update-stack.sh news-letter-ecr-stack stack-template.yaml $AWS_PROFILE`
3. `cd ../` && run `./build-and-push-docker.sh`
4. `cd infra` && `./create-update-stack.sh news-letter-lambda-stack stack-template-lambda.yaml $AWS_PROFILE $ECR_REPOSITORY_URL` (Disclaimer: You cannot build lambda if no container is pushed to the ecr, ecr repository URL is created in step 2)

### For lambda function
The following variables are necessary for the lambda function to run, add them to the lambda function in the aws conosle
- `SENDER_EMAIL`=gmail to send email from
- `SENDER_PASSWORD`=gmail email password
- `EMAIL_RECIPIENTS`=list of recipient emails
 

